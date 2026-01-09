"""
API de generación de música con IA
"""
import os
import uuid
from datetime import datetime
from typing import Optional
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.core.database import get_db
from app.models.user import User
from app.models.music_generation import MusicGeneration, EstadoMusicGeneration
from app.api.auth import get_current_user
from app.services.music_service import music_service
from app.core.config import settings

router = APIRouter(prefix="/music", tags=["Music"])


# ============ SCHEMAS ============

class MusicGenerationRequest(BaseModel):
    """Request para generar música"""
    titulo: str = Field(..., min_length=1, max_length=200)
    descripcion: str = Field(..., min_length=10, max_length=2000)
    duracion_segundos: int = Field(default=30, ge=15, le=120)
    es_instrumental: bool = False
    genero: Optional[str] = None
    mood: Optional[str] = None


class MusicGenerationResponse(BaseModel):
    """Response de generación de música"""
    exito: bool
    mensaje: str
    generacion_id: Optional[int] = None
    audio_url: Optional[str] = None
    prompt_usado: Optional[str] = None
    mood: Optional[str] = None
    genre: Optional[str] = None
    lyrics_theme: Optional[str] = None
    creditos_restantes: Optional[int] = None
    tiempo_ms: Optional[int] = None


class MusicHistoryItem(BaseModel):
    """Item del historial de música"""
    id: int
    titulo: str
    descripcion: Optional[str]
    duracion_segundos: int
    es_instrumental: bool
    genero: Optional[str]
    mood: Optional[str]
    audio_url: Optional[str]
    estado: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============ ESTILOS DE MÚSICA ============

MUSIC_STYLES = {
    "jingle_comercial": {
        "nombre": "Jingle Comercial",
        "descripcion": "Música pegajosa para anuncios y comerciales",
        "icono": "🎵",
        "prompt_hint": "catchy commercial jingle"
    },
    "latin_pop": {
        "nombre": "Latin Pop",
        "descripcion": "Pop latino con ritmos bailables",
        "icono": "💃",
        "prompt_hint": "latin pop upbeat"
    },
    "reggaeton": {
        "nombre": "Reggaeton",
        "descripcion": "Ritmos urbanos latinos",
        "icono": "🔥",
        "prompt_hint": "reggaeton urban beat"
    },
    "electronica": {
        "nombre": "Electrónica",
        "descripcion": "Música electrónica y EDM",
        "icono": "⚡",
        "prompt_hint": "electronic EDM energetic"
    },
    "acustico": {
        "nombre": "Acústico",
        "descripcion": "Sonido orgánico con guitarra",
        "icono": "🎸",
        "prompt_hint": "acoustic guitar warm"
    },
    "hip_hop": {
        "nombre": "Hip Hop",
        "descripcion": "Beats de hip hop y rap",
        "icono": "🎤",
        "prompt_hint": "hip hop rap beat"
    },
    "cinematic": {
        "nombre": "Cinemático",
        "descripcion": "Música épica para videos",
        "icono": "🎬",
        "prompt_hint": "cinematic epic orchestral"
    },
    "lofi": {
        "nombre": "Lo-Fi",
        "descripcion": "Chill beats relajantes",
        "icono": "☕",
        "prompt_hint": "lofi chill relaxed beats"
    }
}


# ============ ENDPOINTS ============

@router.get("/estilos")
async def obtener_estilos():
    """Obtiene los estilos de música disponibles"""
    return [
        {
            "id": key,
            "nombre": style["nombre"],
            "descripcion": style["descripcion"],
            "icono": style["icono"]
        }
        for key, style in MUSIC_STYLES.items()
    ]


@router.post("/generar", response_model=MusicGenerationResponse)
async def generar_musica(
    request: MusicGenerationRequest,
    db: AsyncSession = Depends(get_db),
    usuario: User = Depends(get_current_user)
):
    """
    Genera una canción con IA.
    Consume 1 crédito.
    """
    # Verificar créditos
    if not usuario.tiene_creditos(1):
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="No tienes suficientes créditos. Compra más para continuar."
        )

    try:
        # Crear registro de generación
        generacion = MusicGeneration(
            user_id=usuario.id,
            titulo=request.titulo,
            descripcion=request.descripcion,
            duracion_segundos=request.duracion_segundos,
            es_instrumental=request.es_instrumental,
            genero=request.genero,
            mood=request.mood,
            estado=EstadoMusicGeneration.GENERANDO_PROMPT.value
        )
        db.add(generacion)
        await db.commit()
        await db.refresh(generacion)

        # Usar crédito
        usuario.usar_credito()
        await db.commit()

        # Generar música
        generacion.estado = EstadoMusicGeneration.GENERANDO_MUSICA.value
        await db.commit()

        resultado = await music_service.generar_cancion_completa(
            titulo=request.titulo,
            descripcion=request.descripcion,
            duracion=request.duracion_segundos,
            genero=request.genero,
            mood=request.mood,
            es_instrumental=request.es_instrumental
        )

        if resultado.get("exito"):
            # Guardar audio localmente
            audio_url = resultado.get("audio_url")
            nombre_archivo = f"music_{generacion.id}_{uuid.uuid4().hex[:8]}.mp3"
            ruta_local = os.path.join(settings.GENERATED_DIR, "music", nombre_archivo)

            # Descargar y guardar
            descargado = await music_service.descargar_audio(audio_url, ruta_local)

            if descargado:
                generacion.audio_path = ruta_local
                generacion.audio_url = f"/viralpost/music/{nombre_archivo}"
            else:
                # Si no se pudo descargar, usar URL directa
                generacion.audio_url = audio_url

            # Actualizar generación
            generacion.estado = EstadoMusicGeneration.COMPLETADA.value
            generacion.prompt_musicgpt = resultado.get("prompt_usado")
            generacion.music_style = resultado.get("music_style")
            generacion.mood = resultado.get("mood")
            generacion.genero = resultado.get("genre")
            generacion.musicgpt_conversion_id = resultado.get("conversion_id")
            generacion.tiempo_procesamiento_ms = resultado.get("tiempo_ms")
            generacion.completed_at = datetime.utcnow()

            await db.commit()

            return MusicGenerationResponse(
                exito=True,
                mensaje="¡Canción generada exitosamente!",
                generacion_id=generacion.id,
                audio_url=generacion.audio_url,
                prompt_usado=resultado.get("prompt_usado"),
                mood=resultado.get("mood"),
                genre=resultado.get("genre"),
                lyrics_theme=resultado.get("lyrics_theme"),
                creditos_restantes=usuario.creditos,
                tiempo_ms=resultado.get("tiempo_ms")
            )
        else:
            # Error en generación - devolver crédito
            usuario.creditos += 1
            usuario.creditos_usados -= 1
            generacion.estado = EstadoMusicGeneration.ERROR.value
            generacion.error_mensaje = resultado.get("error", "Error desconocido")
            await db.commit()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al generar música: {resultado.get('error')}"
            )

    except HTTPException:
        raise
    except Exception as e:
        # Error inesperado - devolver crédito
        usuario.creditos += 1
        usuario.creditos_usados -= 1
        if generacion:
            generacion.estado = EstadoMusicGeneration.ERROR.value
            generacion.error_mensaje = str(e)
        await db.commit()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )


@router.get("/historial")
async def obtener_historial(
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    usuario: User = Depends(get_current_user)
):
    """Obtiene el historial de generaciones de música del usuario"""
    result = await db.execute(
        select(MusicGeneration)
        .where(MusicGeneration.user_id == usuario.id)
        .order_by(desc(MusicGeneration.created_at))
        .limit(limit)
        .offset(offset)
    )
    generaciones = result.scalars().all()

    return {
        "generaciones": [
            {
                "id": g.id,
                "titulo": g.titulo,
                "descripcion": g.descripcion,
                "duracion_segundos": g.duracion_segundos,
                "es_instrumental": g.es_instrumental,
                "genero": g.genero,
                "mood": g.mood,
                "audio_url": g.audio_url,
                "estado": g.estado,
                "created_at": g.created_at.isoformat() if g.created_at else None
            }
            for g in generaciones
        ],
        "total": len(generaciones)
    }


@router.get("/generacion/{generacion_id}")
async def obtener_generacion(
    generacion_id: int,
    db: AsyncSession = Depends(get_db),
    usuario: User = Depends(get_current_user)
):
    """Obtiene los detalles de una generación específica"""
    result = await db.execute(
        select(MusicGeneration)
        .where(
            MusicGeneration.id == generacion_id,
            MusicGeneration.user_id == usuario.id
        )
    )
    generacion = result.scalar_one_or_none()

    if not generacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Generación no encontrada"
        )

    return {
        "id": generacion.id,
        "titulo": generacion.titulo,
        "descripcion": generacion.descripcion,
        "duracion_segundos": generacion.duracion_segundos,
        "es_instrumental": generacion.es_instrumental,
        "genero": generacion.genero,
        "mood": generacion.mood,
        "prompt_musicgpt": generacion.prompt_musicgpt,
        "music_style": generacion.music_style,
        "audio_url": generacion.audio_url,
        "estado": generacion.estado,
        "tiempo_procesamiento_ms": generacion.tiempo_procesamiento_ms,
        "created_at": generacion.created_at.isoformat() if generacion.created_at else None,
        "completed_at": generacion.completed_at.isoformat() if generacion.completed_at else None
    }
