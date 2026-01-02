"""
Configuración central de ViralPost AI
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Configuración de la aplicación"""

    # Aplicación
    APP_NAME: str = "ViralPost AI"
    APP_DESCRIPTION: str = "Genera imágenes virales para tus redes sociales"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str = "cambiar-en-produccion-clave-secreta-muy-larga"

    # Servidor
    HOST: str = "127.0.0.1"
    PORT: int = 5001  # Puerto diferente a CosmicMind (5000)

    # Base de datos
    DATABASE_URL: str = "sqlite+aiosqlite:///./viralpost.db"

    # JWT
    JWT_SECRET_KEY: str = "jwt-secret-key-cambiar-en-produccion"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24 * 7  # 7 días

    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""

    # OpenAI (para generación de prompts)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"

    # Google Gemini (para generación de imágenes)
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash-exp"

    # Dominio
    DOMAIN: str = "agathoscreative.com"
    BASE_URL: str = "https://agathoscreative.com/viralpost"

    # Directorios
    UPLOAD_DIR: str = "/var/www/agathoscreative/viralpost/uploads"
    GENERATED_DIR: str = "/var/www/agathoscreative/viralpost/generated"

    # ===========================================
    # SISTEMA DE CRÉDITOS Y PRECIOS
    # ===========================================

    # Costos de API (aproximados en USD)
    OPENAI_COST_PER_REQUEST: float = 0.02      # ~$0.02 por prompt con GPT-4
    GEMINI_COST_PER_IMAGE: float = 0.03        # ~$0.03 por imagen generada
    TOTAL_COST_PER_GENERATION: float = 0.05    # Costo total por generación

    # Margen de ganancia (3x el costo)
    PROFIT_MARGIN: float = 3.0

    # Precio por crédito en USD (costo * margen)
    CREDIT_PRICE_USD: float = 0.15  # $0.05 * 3 = $0.15 por crédito

    # Tasa de cambio MXN/USD (aproximada)
    MXN_USD_RATE: float = 17.50

    # Paquetes de créditos disponibles (en MXN)
    # Precio = créditos * CREDIT_PRICE_USD * MXN_USD_RATE
    CREDIT_PACKAGES: list = [
        {"credits": 10, "price_mxn": 30, "stripe_price_id": "price_10_creditos"},
        {"credits": 25, "price_mxn": 70, "stripe_price_id": "price_25_creditos", "popular": True},
        {"credits": 50, "price_mxn": 130, "stripe_price_id": "price_50_creditos"},
        {"credits": 100, "price_mxn": 250, "stripe_price_id": "price_100_creditos", "best_value": True},
    ]

    # Créditos gratis al registrarse
    FREE_CREDITS_ON_SIGNUP: int = 3

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    """Obtiene configuración cacheada"""
    return Settings()


settings = get_settings()
