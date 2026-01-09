"""
Modelo de Generación de Música con IA
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class EstadoMusicGeneration(str, enum.Enum):
    """Estados de la generación de música"""
    PENDIENTE = "pendiente"
    GENERANDO_PROMPT = "generando_prompt"
    GENERANDO_MUSICA = "generando_musica"
    COMPLETADA = "completada"
    ERROR = "error"


class MusicGeneration(Base):
    """Modelo de generación de música"""
    __tablename__ = "music_generations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Datos de entrada
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)  # Brief del producto/servicio
    duracion_segundos = Column(Integer, default=30)
    es_instrumental = Column(Boolean, default=False)

    # Configuración de estilo
    genero = Column(String(100), nullable=True)
    mood = Column(String(100), nullable=True)
    idioma_letra = Column(String(50), default="es-MX")  # Español mexicano por defecto

    # Prompts generados
    prompt_openai = Column(Text, nullable=True)  # Prompt enviado a OpenAI
    prompt_musicgpt = Column(Text, nullable=True)  # Prompt final para MusicGPT
    music_style = Column(String(200), nullable=True)

    # Archivos generados
    audio_path = Column(String(500), nullable=True)
    audio_url = Column(String(500), nullable=True)  # URL temporal de MusicGPT

    # IDs externos
    musicgpt_conversion_id = Column(String(100), nullable=True)

    # Estado
    estado = Column(String(30), default=EstadoMusicGeneration.PENDIENTE.value)
    error_mensaje = Column(Text, nullable=True)

    # Metadata
    creditos_usados = Column(Integer, default=1)
    tiempo_procesamiento_ms = Column(Integer, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relaciones
    user = relationship("User", back_populates="music_generaciones")
