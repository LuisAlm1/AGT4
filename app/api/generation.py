"""
Rutas de generación de imágenes
"""
import os
import base64
import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.core.database import get_db
from app.core.security import obtener_usuario_actual
from app.core.config import settings
from app.models.user import User
from app.models.generation import Generation, EstadoGeneracion
from app.services.viral_styles import obtener_todos_estilos, obtener_estilo, obtener_categorias
from app.services.generation import generation_service, guardar_imagen
from app.api.schemas import (
    CategoriaResponse,
    EstiloResponse,
    ImagenesEstilosResponse,
    GeneracionCompletaResponse,
    GeneracionResponse,
    HistorialResponse
)
from pathlib import Path

router = APIRouter(prefix="/generacion", tags=["Generación"])


@router.get("/categorias", response_model=list[CategoriaResponse])
async def listar_categorias():
    """
    Lista todas las categorías de giro de negocio disponibles.
    """
    return [
        CategoriaResponse(
            id=c["id"],
            nombre=c["nombre"],
            icono=c["icono"],
            descripcion=c["descripcion"]
        )
        for c in obtener_categorias()
    ]


@router.get("/estilos", response_model=list[EstiloResponse])
async def listar_estilos(categoria: Optional[str] = None):
    """
    Lista todos los estilos virales disponibles.
    Opcionalmente filtra por categoría de giro.
    """
    estilos = obtener_todos_estilos(categoria)
    return [
        EstiloResponse(
            id=e["id"],
            nombre=e["nombre"],
            descripcion=e["descripcion"],
            icono=e["icono"],
            preview_color=e["preview_color"],
            imagen_ejemplo=e.get("imagen_ejemplo"),
            categorias=e.get("categorias")
        )
        for e in estilos
    ]


@router.get("/estilos/imagenes-dinamicas", response_model=ImagenesEstilosResponse)
async def obtener_imagenes_dinamicas(db: AsyncSession = Depends(get_db)):
    """
    Obtiene la última imagen generada para cada estilo.
    Endpoint público (no requiere autenticación) para mostrar previews dinámicos.
    """
    from sqlalchemy import func
    from app.services.viral_styles import VIRAL_STYLES

    imagenes = {}

    # Para cada estilo, buscar la última generación completada
    for estilo_id in VIRAL_STYLES.keys():
        result = await db.execute(
            select(Generation)
            .where(
                Generation.estilo == estilo_id,
                Generation.estado == EstadoGeneracion.COMPLETADA.value,
                Generation.imagen_generada_path.isnot(None)
            )
            .order_by(desc(Generation.completed_at))
            .limit(1)
        )
        generacion = result.scalar_one_or_none()

        if generacion and generacion.imagen_generada_path:
            imagenes[estilo_id] = f"/viralpost/imagenes/{Path(generacion.imagen_generada_path).name}"

    return ImagenesEstilosResponse(imagenes=imagenes)


@router.get("/estilo/{estilo_id}", response_model=EstiloResponse)
async def obtener_detalle_estilo(estilo_id: str):
    """
    Obtiene detalles de un estilo específico.
    """
    estilo = obtener_estilo(estilo_id)
    if not estilo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estilo no encontrado"
        )
    return EstiloResponse(
        id=estilo["id"],
        nombre=estilo["nombre"],
        descripcion=estilo["descripcion"],
        icono=estilo["icono"],
        preview_color=estilo["preview_color"],
        imagen_ejemplo=estilo.get("imagen_ejemplo")
    )


@router.post("/crear", response_model=GeneracionCompletaResponse)
async def crear_generacion(
    estilo_id: str = Form(...),
    nombre_producto: str = Form(...),
    descripcion_producto: Optional[str] = Form(None),
    marca: Optional[str] = Form(None),
    imagen_producto: UploadFile = File(...),
    logo: Optional[UploadFile] = File(None),
    usuario: User = Depends(obtener_usuario_actual),
    db: AsyncSession = Depends(get_db)
):
    """
    Genera una imagen viral y copy para redes sociales.

    Requiere:
    - 1 crédito
    - Imagen del producto (obligatoria)
    - Logo (opcional)

    Retorna:
    - Imagen generada en base64
    - Copy para Facebook e Instagram
    - Hashtags sugeridos
    """
    # Verificar créditos
    if not usuario.tiene_creditos(1):
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="No tienes suficientes créditos. Compra más para continuar."
        )

    # Validar estilo
    estilo = obtener_estilo(estilo_id)
    if not estilo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Estilo no válido"
        )

    # Validar tipo de archivo
    tipos_permitidos = ["image/jpeg", "image/png", "image/webp"]
    if imagen_producto.content_type not in tipos_permitidos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de imagen no permitido. Usa JPG, PNG o WebP."
        )

    try:
        # Leer imagen del producto
        imagen_bytes = await imagen_producto.read()
        imagen_b64 = base64.b64encode(imagen_bytes).decode("ascii")
        imagen_mime = imagen_producto.content_type

        # Leer logo si existe
        logo_b64 = None
        logo_mime = "image/png"
        if logo:
            if logo.content_type not in tipos_permitidos:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Tipo de logo no permitido. Usa JPG, PNG o WebP."
                )
            logo_bytes = await logo.read()
            logo_b64 = base64.b64encode(logo_bytes).decode("ascii")
            logo_mime = logo.content_type

        # Crear registro de generación
        generacion = Generation(
            user_id=usuario.id,
            nombre_producto=nombre_producto,
            descripcion_producto=descripcion_producto,
            marca=marca,
            estilo=estilo_id,
            estado=EstadoGeneracion.PROCESANDO.value
        )
        db.add(generacion)
        await db.commit()
        await db.refresh(generacion)

        # Usar crédito
        usuario.usar_credito()
        await db.commit()

        # Generar contenido
        resultado = await generation_service.generar_contenido_completo(
            estilo_id=estilo_id,
            nombre_producto=nombre_producto,
            descripcion_producto=descripcion_producto or "",
            marca=marca or "",
            imagen_producto_b64=imagen_b64,
            logo_b64=logo_b64,
            imagen_mime=imagen_mime,
            logo_mime=logo_mime
        )

        if resultado.get("exito"):
            # Guardar imagen generada
            nombre_archivo = f"{generacion.id}_{uuid.uuid4().hex[:8]}.png"
            ruta_imagen = guardar_imagen(resultado["imagen_b64"], nombre_archivo)

            # Actualizar generación
            generacion.estado = EstadoGeneracion.COMPLETADA.value
            generacion.imagen_generada_path = ruta_imagen
            generacion.prompt_generado = resultado.get("prompt_usado")
            generacion.copy_facebook = resultado.get("copy_facebook")
            generacion.hashtags_facebook = resultado.get("hashtags_facebook")
            generacion.copy_instagram = resultado.get("copy_instagram")
            generacion.hashtags_instagram = resultado.get("hashtags_instagram")
            generacion.tiempo_procesamiento_ms = resultado.get("tiempo_ms")
            generacion.completed_at = datetime.utcnow()

            await db.commit()

            return GeneracionCompletaResponse(
                exito=True,
                mensaje="¡Imagen generada exitosamente!",
                generacion_id=generacion.id,
                imagen_base64=resultado["imagen_b64"],
                copy_facebook=resultado.get("copy_facebook"),
                hashtags_facebook=resultado.get("hashtags_facebook"),
                copy_instagram=resultado.get("copy_instagram"),
                hashtags_instagram=resultado.get("hashtags_instagram"),
                creditos_restantes=usuario.creditos,
                tiempo_ms=resultado.get("tiempo_ms")
            )
        else:
            # Error en generación - devolver crédito
            usuario.creditos += 1
            usuario.creditos_usados -= 1
            generacion.estado = EstadoGeneracion.ERROR.value
            generacion.error_mensaje = resultado.get("error", "Error desconocido")
            await db.commit()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al generar: {resultado.get('error')}"
            )

    except HTTPException:
        raise
    except Exception as e:
        # Error inesperado - devolver crédito
        usuario.creditos += 1
        usuario.creditos_usados -= 1
        generacion.estado = EstadoGeneracion.ERROR.value
        generacion.error_mensaje = str(e)
        await db.commit()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado: {str(e)}"
        )


@router.get("/historial", response_model=HistorialResponse)
async def obtener_historial(
    pagina: int = 1,
    por_pagina: int = 10,
    usuario: User = Depends(obtener_usuario_actual),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtiene el historial de generaciones del usuario.
    """
    offset = (pagina - 1) * por_pagina

    # Contar total
    count_result = await db.execute(
        select(Generation).where(Generation.user_id == usuario.id)
    )
    total = len(count_result.scalars().all())

    # Obtener página
    result = await db.execute(
        select(Generation)
        .where(Generation.user_id == usuario.id)
        .order_by(desc(Generation.created_at))
        .offset(offset)
        .limit(por_pagina)
    )
    generaciones = result.scalars().all()

    return HistorialResponse(
        total=total,
        pagina=pagina,
        por_pagina=por_pagina,
        generaciones=[
            GeneracionResponse(
                id=g.id,
                estado=g.estado,
                imagen_url=f"/viralpost/imagenes/{Path(g.imagen_generada_path).name}" if g.imagen_generada_path else None,
                copy_facebook=g.copy_facebook,
                hashtags_facebook=g.hashtags_facebook,
                copy_instagram=g.copy_instagram,
                hashtags_instagram=g.hashtags_instagram,
                estilo=g.estilo,
                created_at=g.created_at,
                completed_at=g.completed_at
            )
            for g in generaciones
        ]
    )


@router.get("/{generacion_id}", response_model=GeneracionResponse)
async def obtener_generacion(
    generacion_id: int,
    usuario: User = Depends(obtener_usuario_actual),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtiene los detalles de una generación específica.
    """
    result = await db.execute(
        select(Generation).where(
            Generation.id == generacion_id,
            Generation.user_id == usuario.id
        )
    )
    generacion = result.scalar_one_or_none()

    if not generacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Generación no encontrada"
        )

    return GeneracionResponse(
        id=generacion.id,
        estado=generacion.estado,
        imagen_url=f"/viralpost/imagenes/{Path(generacion.imagen_generada_path).name}" if generacion.imagen_generada_path else None,
        copy_facebook=generacion.copy_facebook,
        hashtags_facebook=generacion.hashtags_facebook,
        copy_instagram=generacion.copy_instagram,
        hashtags_instagram=generacion.hashtags_instagram,
        estilo=generacion.estilo,
        created_at=generacion.created_at,
        completed_at=generacion.completed_at
    )
