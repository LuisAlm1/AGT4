"""
Rutas de pagos con Stripe
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import obtener_usuario_actual
from app.core.config import settings
from app.models.user import User
from app.models.transaction import Transaction, EstadoTransaccion
from app.services.stripe_service import stripe_service
from app.api.schemas import (
    PaqueteResponse,
    CheckoutRequest,
    CheckoutResponse,
    TransaccionResponse
)

router = APIRouter(prefix="/pagos", tags=["Pagos"])


@router.get("/paquetes", response_model=list[PaqueteResponse])
async def listar_paquetes(
    currency: str = Query(default="MXN", pattern="^(MXN|USD)$", description="Moneda: MXN o USD"),
    lang: str = Query(default="es", pattern="^(es|en)$", description="Idioma: es o en")
):
    """
    Lista todos los paquetes de créditos disponibles.
    Soporta MXN (México) y USD (USA/Internacional).
    """
    paquetes = stripe_service.obtener_paquetes(currency)

    result = []
    for p in paquetes:
        # Traducir nombres si es inglés
        if lang == "en":
            nombre = f"{p['creditos']} Credits"
            descripcion = f"Credit package - {p['creditos']} generations"
        else:
            nombre = p.get("nombre", f"{p['creditos']} Créditos")
            descripcion = p.get("descripcion", f"Paquete de {p['creditos']} generaciones")

        result.append(PaqueteResponse(
            id=p["id"],
            creditos=p["creditos"],
            precio_mxn=p["precio_mxn"],
            precio=p.get("precio", p["precio_mxn"]),
            moneda=p.get("moneda", "MXN"),
            nombre=nombre,
            descripcion=descripcion,
            popular=p.get("popular", False),
            mejor_valor=p.get("mejor_valor", False)
        ))

    return result


@router.post("/checkout", response_model=CheckoutResponse)
async def crear_checkout(
    datos: CheckoutRequest,
    usuario: User = Depends(obtener_usuario_actual),
    db: AsyncSession = Depends(get_db)
):
    """
    Crea una sesión de checkout de Stripe para comprar créditos.
    Soporta pagos en MXN (con OXXO) y USD (solo tarjeta).

    Retorna la URL de Stripe Checkout donde el usuario debe ser redirigido.
    """
    paquete = stripe_service.obtener_paquete(datos.paquete_id, datos.currency)
    if not paquete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Paquete no encontrado" if datos.lang == "es" else "Package not found"
        )

    try:
        # Actualizar stripe_customer_id si es necesario
        if not usuario.stripe_customer_id:
            customer_id = await stripe_service.crear_o_obtener_customer(usuario)
            usuario.stripe_customer_id = customer_id
            await db.commit()

        # Determinar URLs basadas en la app de origen
        from_param = f"&from={datos.from_app}" if datos.from_app == "soundai" else ""
        cancel_from = f"?from={datos.from_app}" if datos.from_app == "soundai" else ""

        # Crear sesión de checkout
        resultado = await stripe_service.crear_checkout_session(
            user=usuario,
            paquete_id=datos.paquete_id,
            success_url=f"{settings.BASE_URL}/pago-exitoso?session_id={{CHECKOUT_SESSION_ID}}{from_param}",
            cancel_url=f"{settings.BASE_URL}/creditos{cancel_from}",
            currency=datos.currency,
            lang=datos.lang
        )

        # Crear registro de transacción pendiente
        # Siempre guardamos el monto en MXN para consistencia en reportes
        transaccion = Transaction(
            user_id=usuario.id,
            stripe_checkout_session_id=resultado["session_id"],
            creditos=paquete["creditos"],
            monto_mxn=paquete["precio_mxn"],  # Siempre en MXN
            estado=EstadoTransaccion.PENDIENTE.value,
            descripcion=f"Compra: {paquete['creditos']} créditos ({datos.currency})"
        )
        db.add(transaccion)
        await db.commit()

        return CheckoutResponse(
            checkout_url=resultado["checkout_url"],
            session_id=resultado["session_id"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear checkout: {str(e)}"
        )


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Webhook de Stripe para procesar pagos completados.

    Este endpoint es llamado por Stripe cuando un pago se completa.
    """
    payload = await request.body()
    signature = request.headers.get("stripe-signature", "")

    try:
        event = stripe_service.verificar_webhook(payload, signature)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Firma inválida"
        )

    # Procesar evento
    event_type = event["type"]
    session = event["data"]["object"]

    # checkout.session.completed - pago con tarjeta completado inmediatamente
    # checkout.session.async_payment_succeeded - pago OXXO confirmado (después de pagar en tienda)
    if event_type in ["checkout.session.completed", "checkout.session.async_payment_succeeded"]:

        # Para checkout.session.completed, verificar si el pago ya está completo
        # (tarjeta = completo inmediatamente, OXXO = pendiente hasta pagar en tienda)
        if event_type == "checkout.session.completed":
            payment_status = session.get("payment_status", "")
            # Si es OXXO, el payment_status será "unpaid" hasta que paguen en tienda
            if payment_status != "paid":
                # Es OXXO - esperar al evento async_payment_succeeded
                return {"received": True, "note": "Esperando pago OXXO"}

        datos = stripe_service.procesar_checkout_completado(session)

        # Buscar transacción
        result = await db.execute(
            select(Transaction).where(
                Transaction.stripe_checkout_session_id == datos["session_id"]
            )
        )
        transaccion = result.scalar_one_or_none()

        if transaccion and transaccion.estado == EstadoTransaccion.PENDIENTE.value:
            # Buscar usuario
            result = await db.execute(
                select(User).where(User.id == datos["user_id"])
            )
            usuario = result.scalar_one_or_none()

            if usuario:
                # Agregar créditos
                usuario.agregar_creditos(datos["creditos"])

                # Actualizar transacción
                transaccion.estado = EstadoTransaccion.COMPLETADA.value
                transaccion.completed_at = datetime.utcnow()

                await db.commit()

    # checkout.session.async_payment_failed - pago OXXO falló (voucher expiró)
    elif event_type == "checkout.session.async_payment_failed":
        datos = stripe_service.procesar_checkout_completado(session)

        # Marcar transacción como fallida
        result = await db.execute(
            select(Transaction).where(
                Transaction.stripe_checkout_session_id == datos["session_id"]
            )
        )
        transaccion = result.scalar_one_or_none()

        if transaccion and transaccion.estado == EstadoTransaccion.PENDIENTE.value:
            transaccion.estado = EstadoTransaccion.FALLIDA.value
            await db.commit()

    return {"received": True}


@router.get("/historial", response_model=list[TransaccionResponse])
async def historial_transacciones(
    usuario: User = Depends(obtener_usuario_actual),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtiene el historial de transacciones del usuario.
    """
    result = await db.execute(
        select(Transaction)
        .where(Transaction.user_id == usuario.id)
        .order_by(Transaction.created_at.desc())
        .limit(50)
    )
    transacciones = result.scalars().all()

    return [
        TransaccionResponse(
            id=t.id,
            creditos=t.creditos,
            monto_mxn=t.monto_mxn,
            estado=t.estado,
            descripcion=t.descripcion,
            created_at=t.created_at
        )
        for t in transacciones
    ]


@router.get("/creditos")
async def obtener_creditos(
    usuario: User = Depends(obtener_usuario_actual)
):
    """
    Obtiene el saldo de créditos del usuario.
    """
    return {
        "creditos": usuario.creditos,
        "creditos_usados": usuario.creditos_usados,
        "total_comprados": usuario.creditos + usuario.creditos_usados
    }
