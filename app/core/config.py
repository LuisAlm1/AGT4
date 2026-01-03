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

    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""

    # OpenAI (para generación de prompts)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"

    # Google Gemini - Nano Banana Pro (para generación de imágenes)
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3-pro-image-preview"  # Nano Banana Pro

    # Dominio
    DOMAIN: str = "agathoscreative.com"
    BASE_URL: str = "https://agathoscreative.com/viralpost"

    # Directorios
    UPLOAD_DIR: str = "/var/www/agathoscreative/viralpost/uploads"
    GENERATED_DIR: str = "/var/www/agathoscreative/viralpost/generated"

    # ===========================================
    # SISTEMA DE CRÉDITOS Y PRECIOS
    # ===========================================

    # Costos de API (en USD) - Actualizados para Nano Banana Pro
    OPENAI_COST_PER_REQUEST: float = 0.03      # ~$0.03 por prompt con GPT-4o
    GEMINI_COST_PER_IMAGE: float = 0.134       # $0.134 por imagen (Nano Banana Pro 1K-2K)
    TOTAL_COST_PER_GENERATION: float = 0.164   # Costo total por generación

    # Margen de ganancia (3x el costo)
    PROFIT_MARGIN: float = 3.0

    # Precio por crédito en USD (costo * margen)
    # $0.164 * 3 = $0.492 ≈ $0.50 por crédito
    CREDIT_PRICE_USD: float = 0.50

    # Tasa de cambio MXN/USD (aproximada)
    MXN_USD_RATE: float = 17.50

    # Paquetes de créditos disponibles (en MXN)
    # Base: $0.50 USD × 17.5 = $8.75 MXN por crédito
    # Con descuentos por volumen
    CREDIT_PACKAGES: list = [
        {"credits": 10, "price_mxn": 90, "stripe_price_id": "price_10_creditos"},        # $9.00/crédito
        {"credits": 25, "price_mxn": 215, "stripe_price_id": "price_25_creditos", "popular": True},  # $8.60/crédito
        {"credits": 50, "price_mxn": 425, "stripe_price_id": "price_50_creditos"},       # $8.50/crédito
        {"credits": 100, "price_mxn": 829, "stripe_price_id": "price_100_creditos", "best_value": True},  # $8.29/crédito
    ]

    # Créditos gratis al registrarse
    FREE_CREDITS_ON_SIGNUP: int = 1

    # Admin Panel
    ADMIN_PASSWORD: str = "viralpost2024admin"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    """Obtiene configuración cacheada"""
    return Settings()


settings = get_settings()
