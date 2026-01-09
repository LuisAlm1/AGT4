"""
API de Administración - Estadísticas y métricas
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.models.transaction import Transaction, EstadoTransaccion
from app.models.generation import Generation, EstadoGeneracion
from app.models.music_generation import MusicGeneration, EstadoMusicGeneration

router = APIRouter(prefix="/admin", tags=["Admin"])

# Password de admin desde configuración
ADMIN_PASSWORD = settings.ADMIN_PASSWORD


def verificar_admin(password: str = Query(..., description="Password de admin")):
    """Verifica el password de admin"""
    if password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password incorrecto"
        )
    return True


@router.get("/stats")
async def obtener_estadisticas(
    _: bool = Depends(verificar_admin),
    db: AsyncSession = Depends(get_db)
):
    """Obtiene estadísticas generales del sistema"""

    # Fechas para cálculos
    ahora = datetime.utcnow()
    hace_7_dias = ahora - timedelta(days=7)
    hace_30_dias = ahora - timedelta(days=30)
    inicio_hoy = ahora.replace(hour=0, minute=0, second=0, microsecond=0)

    # ========== USUARIOS ==========
    # Total usuarios
    total_usuarios = await db.scalar(select(func.count(User.id)))

    # Usuarios últimos 7 días
    usuarios_7_dias = await db.scalar(
        select(func.count(User.id)).where(User.created_at >= hace_7_dias)
    )

    # Usuarios hoy
    usuarios_hoy = await db.scalar(
        select(func.count(User.id)).where(User.created_at >= inicio_hoy)
    )

    # ========== TRANSACCIONES ==========
    # Total transacciones completadas
    total_transacciones = await db.scalar(
        select(func.count(Transaction.id)).where(
            Transaction.estado == EstadoTransaccion.COMPLETADA.value
        )
    )

    # Ingresos totales MXN
    ingresos_totales = await db.scalar(
        select(func.sum(Transaction.monto_mxn)).where(
            Transaction.estado == EstadoTransaccion.COMPLETADA.value
        )
    ) or 0

    # Ingresos últimos 30 días
    ingresos_30_dias = await db.scalar(
        select(func.sum(Transaction.monto_mxn)).where(
            and_(
                Transaction.estado == EstadoTransaccion.COMPLETADA.value,
                Transaction.created_at >= hace_30_dias
            )
        )
    ) or 0

    # Ingresos últimos 7 días
    ingresos_7_dias = await db.scalar(
        select(func.sum(Transaction.monto_mxn)).where(
            and_(
                Transaction.estado == EstadoTransaccion.COMPLETADA.value,
                Transaction.created_at >= hace_7_dias
            )
        )
    ) or 0

    # Ingresos hoy
    ingresos_hoy = await db.scalar(
        select(func.sum(Transaction.monto_mxn)).where(
            and_(
                Transaction.estado == EstadoTransaccion.COMPLETADA.value,
                Transaction.created_at >= inicio_hoy
            )
        )
    ) or 0

    # Total créditos vendidos
    creditos_vendidos = await db.scalar(
        select(func.sum(Transaction.creditos)).where(
            Transaction.estado == EstadoTransaccion.COMPLETADA.value
        )
    ) or 0

    # ========== GENERACIONES ==========
    # Total generaciones
    total_generaciones = await db.scalar(select(func.count(Generation.id)))

    # Generaciones completadas
    generaciones_completadas = await db.scalar(
        select(func.count(Generation.id)).where(
            Generation.estado == EstadoGeneracion.COMPLETADA.value
        )
    )

    # Generaciones últimos 7 días
    generaciones_7_dias = await db.scalar(
        select(func.count(Generation.id)).where(Generation.created_at >= hace_7_dias)
    )

    # Generaciones hoy
    generaciones_hoy = await db.scalar(
        select(func.count(Generation.id)).where(Generation.created_at >= inicio_hoy)
    )

    # ========== MÚSICA (SOUNDAI) ==========
    # Total canciones generadas
    total_musica = await db.scalar(select(func.count(MusicGeneration.id)))

    # Canciones completadas
    musica_completadas = await db.scalar(
        select(func.count(MusicGeneration.id)).where(
            MusicGeneration.estado == EstadoMusicGeneration.COMPLETADA.value
        )
    )

    # Canciones últimos 7 días
    musica_7_dias = await db.scalar(
        select(func.count(MusicGeneration.id)).where(MusicGeneration.created_at >= hace_7_dias)
    )

    # Canciones hoy
    musica_hoy = await db.scalar(
        select(func.count(MusicGeneration.id)).where(MusicGeneration.created_at >= inicio_hoy)
    )

    # Estilos de música populares
    estilos_musica_query = await db.execute(
        select(
            MusicGeneration.genero,
            func.count(MusicGeneration.id).label('count')
        )
        .where(MusicGeneration.genero.isnot(None))
        .group_by(MusicGeneration.genero)
        .order_by(func.count(MusicGeneration.id).desc())
        .limit(10)
    )
    estilos_musica = [
        {"estilo": e.genero or "Sin género", "count": e.count}
        for e in estilos_musica_query.all()
    ]

    # Canciones recientes
    musica_reciente_query = await db.execute(
        select(MusicGeneration, User.email)
        .join(User, MusicGeneration.user_id == User.id)
        .order_by(MusicGeneration.created_at.desc())
        .limit(10)
    )
    musica_reciente = [
        {
            "id": m.MusicGeneration.id,
            "email": m.email,
            "titulo": m.MusicGeneration.titulo,
            "genero": m.MusicGeneration.genero or "Auto",
            "estado": m.MusicGeneration.estado,
            "fecha": m.MusicGeneration.created_at.isoformat() if m.MusicGeneration.created_at else None
        }
        for m in musica_reciente_query.all()
    ]

    # ========== TOP USUARIOS ==========
    # Usuarios con más créditos usados
    top_usuarios_query = await db.execute(
        select(User.email, User.nombre, User.creditos_usados, User.creditos)
        .order_by(User.creditos_usados.desc())
        .limit(10)
    )
    top_usuarios = [
        {
            "email": u.email,
            "nombre": u.nombre or "Sin nombre",
            "creditos_usados": u.creditos_usados,
            "creditos_disponibles": u.creditos
        }
        for u in top_usuarios_query.all()
    ]

    # ========== ESTILOS POPULARES ==========
    estilos_query = await db.execute(
        select(
            Generation.estilo,
            func.count(Generation.id).label('count')
        )
        .group_by(Generation.estilo)
        .order_by(func.count(Generation.id).desc())
    )
    estilos_populares = [
        {"estilo": e.estilo, "count": e.count}
        for e in estilos_query.all()
    ]

    # ========== TRANSACCIONES RECIENTES ==========
    transacciones_recientes_query = await db.execute(
        select(Transaction, User.email)
        .join(User, Transaction.user_id == User.id)
        .where(Transaction.estado == EstadoTransaccion.COMPLETADA.value)
        .order_by(Transaction.created_at.desc())
        .limit(10)
    )
    transacciones_recientes = [
        {
            "id": t.Transaction.id,
            "email": t.email,
            "creditos": t.Transaction.creditos,
            "monto_mxn": t.Transaction.monto_mxn,
            "fecha": t.Transaction.created_at.isoformat() if t.Transaction.created_at else None
        }
        for t in transacciones_recientes_query.all()
    ]

    return {
        "usuarios": {
            "total": total_usuarios or 0,
            "ultimos_7_dias": usuarios_7_dias or 0,
            "hoy": usuarios_hoy or 0
        },
        "ingresos": {
            "total_mxn": round(ingresos_totales, 2),
            "ultimos_30_dias_mxn": round(ingresos_30_dias, 2),
            "ultimos_7_dias_mxn": round(ingresos_7_dias, 2),
            "hoy_mxn": round(ingresos_hoy, 2),
            "total_transacciones": total_transacciones or 0,
            "creditos_vendidos": creditos_vendidos or 0
        },
        "generaciones": {
            "total": total_generaciones or 0,
            "completadas": generaciones_completadas or 0,
            "ultimos_7_dias": generaciones_7_dias or 0,
            "hoy": generaciones_hoy or 0,
            "tasa_exito": round((generaciones_completadas or 0) / max(total_generaciones or 1, 1) * 100, 1)
        },
        "musica": {
            "total": total_musica or 0,
            "completadas": musica_completadas or 0,
            "ultimos_7_dias": musica_7_dias or 0,
            "hoy": musica_hoy or 0,
            "tasa_exito": round((musica_completadas or 0) / max(total_musica or 1, 1) * 100, 1)
        },
        "top_usuarios": top_usuarios,
        "estilos_populares": estilos_populares,
        "estilos_musica": estilos_musica,
        "musica_reciente": musica_reciente,
        "transacciones_recientes": transacciones_recientes,
        "generado_en": ahora.isoformat()
    }


@router.get("/usuarios")
async def listar_usuarios(
    _: bool = Depends(verificar_admin),
    db: AsyncSession = Depends(get_db),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(20, ge=1, le=100)
):
    """Lista todos los usuarios con paginación"""

    offset = (pagina - 1) * por_pagina

    # Total
    total = await db.scalar(select(func.count(User.id)))

    # Usuarios
    usuarios_query = await db.execute(
        select(User)
        .order_by(User.created_at.desc())
        .offset(offset)
        .limit(por_pagina)
    )
    usuarios = usuarios_query.scalars().all()

    return {
        "total": total,
        "pagina": pagina,
        "por_pagina": por_pagina,
        "usuarios": [
            {
                "id": u.id,
                "email": u.email,
                "nombre": u.nombre,
                "creditos": u.creditos,
                "creditos_usados": u.creditos_usados,
                "google_id": bool(u.google_id),
                "is_active": u.is_active,
                "created_at": u.created_at.isoformat() if u.created_at else None
            }
            for u in usuarios
        ]
    }
