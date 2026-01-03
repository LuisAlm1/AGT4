"""
Rutas de pagos con Stripe
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request
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
async def listar_paquetes():
    """
    Lista todos los paquetes de créditos disponibles.
    """
    paquetes = stripe_service.obtener_paquetes()
    return [
        PaqueteResponse(
            id=p["id"],
            creditos=p["creditos"],
            precio_mxn=p["precio_mxn"],
            nombre=p["nombre"],
            descripcion=p["descripcion"],
            popular=p.get("popular", False),
            mejor_valor=p.get("mejor_valor", False)
        )
        for p in paquetes
    ]


@router.post("/checkout", response_model=CheckoutResponse)
async def crear_checkout(
    datos: CheckoutRequest,
    usuario: User = Depends(obtener_usuario_actual),
    db: AsyncSession = Depends(get_db)
):
    """
    Crea una sesión de checkout de Stripe para comprar créditos.

    Retorna la URL de Stripe Checkout donde el usuario debe ser redirigido.
    """
    paquete = stripe_service.obtener_paquete(datos.paquete_id)
    if not paquete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Paquete no encontrado"
        )

    try:
        # Actualizar stripe_customer_id si es necesario
        if not usuario.stripe_customer_id:
            customer_id = await stripe_service.crear_o_obtener_customer(usuario)
            usuario.stripe_customer_id = customer_id
            await db.commit()

        # Crear sesión de checkout
        resultado = await stripe_service.crear_checkout_session(
            user=usuario,
            paquete_id=datos.paquete_id,
            success_url=f"{settings.BASE_URL}/pago-exitoso?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.BASE_URL}/creditos"
        )

        # Crear registro de transacción pendiente
        transaccion = Transaction(
            user_id=usuario.id,
            stripe_checkout_session_id=resultado["session_id"],
            creditos=paquete["creditos"],
            monto_mxn=paquete["precio_mxn"],
            estado=EstadoTransaccion.PENDIENTE.value,
            descripcion=f"Compra: {paquete['nombre']}"
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
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
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
