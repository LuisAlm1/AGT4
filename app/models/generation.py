"""
Modelo de Generación de Imágenes
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class EstiloViral(str, enum.Enum):
    """Estilos virales disponibles"""
    MACRO_EXPLOSION = "macro_explosion"
    LIQUID_METAL = "liquid_metal"
    NEON_NOIR = "neon_noir"
    BOTANICAL_LUXURY = "botanical_luxury"
    ZERO_GRAVITY = "zero_gravity"
    MINIATURE_WORLD = "miniature_world"
    FROZEN_TIME = "frozen_time"
    DARK_LUXURY = "dark_luxury"


class EstadoGeneracion(str, enum.Enum):
    """Estados de la generación"""
    PENDIENTE = "pendiente"
    PROCESANDO = "procesando"
    COMPLETADA = "completada"
    ERROR = "error"


class Generation(Base):
    """Modelo de generación de imagen"""
    __tablename__ = "generations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Datos de entrada
    nombre_producto = Column(String(200), nullable=False)
    descripcion_producto = Column(Text, nullable=True)
    marca = Column(String(100), nullable=True)
    estilo = Column(String(50), nullable=False)

    # Archivos
    imagen_producto_path = Column(String(500), nullable=True)
    logo_path = Column(String(500), nullable=True)
    imagen_generada_path = Column(String(500), nullable=True)

    # Contenido generado
    prompt_generado = Column(Text, nullable=True)
    copy_facebook = Column(Text, nullable=True)
    hashtags_facebook = Column(JSON, nullable=True)
    copy_instagram = Column(Text, nullable=True)
    hashtags_instagram = Column(JSON, nullable=True)

    # Estado
    estado = Column(String(20), default=EstadoGeneracion.PENDIENTE.value)
    error_mensaje = Column(Text, nullable=True)

    # Metadata
    creditos_usados = Column(Integer, default=1)
    tiempo_procesamiento_ms = Column(Integer, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relaciones
    user = relationship("User", back_populates="generaciones")
