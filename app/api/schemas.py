"""
Esquemas Pydantic para la API
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ============ AUTH ============

class RegistroRequest(BaseModel):
    """Solicitud de registro"""
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    nombre: Optional[str] = Field(None, max_length=100)


class LoginRequest(BaseModel):
    """Solicitud de login"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Respuesta con token"""
    access_token: str
    token_type: str = "bearer"
    usuario: "UsuarioResponse"


class UsuarioResponse(BaseModel):
    """Respuesta de usuario"""
    id: int
    email: str
    nombre: Optional[str]
    creditos: int
    creditos_usados: int
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ============ ESTILOS ============

class EstiloResponse(BaseModel):
    """Respuesta de estilo viral"""
    id: str
    nombre: str
    descripcion: str
    icono: str
    preview_color: str


# ============ GENERACIÓN ============

class GeneracionRequest(BaseModel):
    """Solicitud de generación de imagen"""
    estilo_id: str
    nombre_producto: str = Field(..., min_length=1, max_length=200)
    descripcion_producto: Optional[str] = Field(None, max_length=500)
    marca: Optional[str] = Field(None, max_length=100)


class GeneracionResponse(BaseModel):
    """Respuesta de generación"""
    id: int
    estado: str
    imagen_url: Optional[str]
    copy_facebook: Optional[str]
    hashtags_facebook: Optional[List[str]]
    copy_instagram: Optional[str]
    hashtags_instagram: Optional[List[str]]
    estilo: str
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


class GeneracionCompletaResponse(BaseModel):
    """Respuesta completa de generación con imagen en base64"""
    exito: bool
    mensaje: str
    generacion_id: Optional[int] = None
    imagen_base64: Optional[str] = None
    copy_facebook: Optional[str] = None
    hashtags_facebook: Optional[List[str]] = None
    copy_instagram: Optional[str] = None
    hashtags_instagram: Optional[List[str]] = None
    creditos_restantes: int = 0
    tiempo_ms: Optional[int] = None


# ============ PAGOS ============

class PaqueteResponse(BaseModel):
    """Respuesta de paquete de créditos"""
    id: str
    creditos: int
    precio_mxn: int
    nombre: str
    descripcion: str
    popular: bool = False
    mejor_valor: bool = False


class CheckoutRequest(BaseModel):
    """Solicitud de checkout"""
    paquete_id: str


class CheckoutResponse(BaseModel):
    """Respuesta de checkout"""
    checkout_url: str
    session_id: str


class TransaccionResponse(BaseModel):
    """Respuesta de transacción"""
    id: int
    creditos: int
    monto_mxn: float
    estado: str
    descripcion: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ============ HISTORIAL ============

class HistorialResponse(BaseModel):
    """Respuesta de historial de generaciones"""
    total: int
    pagina: int
    por_pagina: int
    generaciones: List[GeneracionResponse]


# Actualizar referencias forward
TokenResponse.model_rebuild()
