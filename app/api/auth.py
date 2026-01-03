"""
Rutas de autenticación
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import (
    hashear_password,
    verificar_password,
    crear_token_acceso,
    obtener_usuario_actual
)
from app.core.config import settings
from app.models.user import User
from app.api.schemas import (
    RegistroRequest,
    LoginRequest,
    TokenResponse,
    UsuarioResponse
)

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/registro", response_model=TokenResponse)
async def registrar_usuario(
    datos: RegistroRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Registra un nuevo usuario.

    - Crea la cuenta
    - Otorga créditos gratis iniciales
    - Retorna token de acceso
    """
    # Verificar si el email ya existe
    result = await db.execute(
        select(User).where(User.email == datos.email.lower())
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este correo ya está registrado"
        )

    # Crear usuario
    usuario = User(
        email=datos.email.lower(),
        hashed_password=hashear_password(datos.password),
        nombre=datos.nombre,
        creditos=settings.FREE_CREDITS_ON_SIGNUP,  # Créditos gratis
        is_active=True,
        is_verified=False
    )

    db.add(usuario)
    await db.commit()
    await db.refresh(usuario)

    # Crear token
    token = crear_token_acceso({"sub": usuario.id})

    return TokenResponse(
        access_token=token,
        usuario=UsuarioResponse.model_validate(usuario)
    )


@router.post("/login", response_model=TokenResponse)
async def iniciar_sesion(
    datos: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Inicia sesión con email y contraseña.

    Retorna token de acceso.
    """
    # Buscar usuario
    result = await db.execute(
        select(User).where(User.email == datos.email.lower())
    )
    usuario = result.scalar_one_or_none()

    if not usuario or not verificar_password(datos.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )

    if not usuario.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tu cuenta está desactivada"
        )

    # Crear token
    token = crear_token_acceso({"sub": usuario.id})

    return TokenResponse(
        access_token=token,
        usuario=UsuarioResponse.model_validate(usuario)
    )


@router.get("/me", response_model=UsuarioResponse)
async def obtener_perfil(
    usuario: User = Depends(obtener_usuario_actual)
):
    """
    Obtiene el perfil del usuario actual.
    """
    return UsuarioResponse.model_validate(usuario)


@router.put("/me", response_model=UsuarioResponse)
async def actualizar_perfil(
    nombre: str,
    usuario: User = Depends(obtener_usuario_actual),
    db: AsyncSession = Depends(get_db)
):
    """
    Actualiza el nombre del usuario.
    """
    usuario.nombre = nombre
    await db.commit()
    await db.refresh(usuario)
    return UsuarioResponse.model_validate(usuario)
