"""
Rutas de autenticación
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from authlib.integrations.starlette_client import OAuth
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

# Configurar OAuth
oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
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


# ============ GOOGLE OAUTH ============

@router.get("/google/login")
async def google_login(request: Request):
    """
    Inicia el flujo de login con Google.
    Redirige al usuario a la página de autenticación de Google.
    Acepta ?redirect= para saber a dónde redirigir después del login.
    """
    redirect_uri = f"{settings.BASE_URL}/api/auth/google/callback"

    # Guardar la URL de redirección en la sesión
    final_redirect = request.query_params.get('redirect', '/viralpost/app')
    request.session['oauth_redirect'] = final_redirect

    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Callback de Google OAuth.
    Procesa la respuesta de Google y crea/autentica al usuario.
    """
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')

        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo obtener información del usuario de Google"
            )

        google_id = user_info.get('sub')
        email = user_info.get('email')
        nombre = user_info.get('name')
        avatar_url = user_info.get('picture')

        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Google no proporcionó un email válido"
            )

        # Buscar usuario existente por google_id o email
        result = await db.execute(
            select(User).where(
                or_(User.google_id == google_id, User.email == email.lower())
            )
        )
        usuario = result.scalar_one_or_none()

        if usuario:
            # Usuario existente - actualizar google_id si no lo tiene
            if not usuario.google_id:
                usuario.google_id = google_id
                usuario.avatar_url = avatar_url
                await db.commit()
        else:
            # Crear nuevo usuario
            usuario = User(
                email=email.lower(),
                google_id=google_id,
                nombre=nombre,
                avatar_url=avatar_url,
                creditos=settings.FREE_CREDITS_ON_SIGNUP,
                is_active=True,
                is_verified=True  # Google ya verificó el email
            )
            db.add(usuario)
            await db.commit()
            await db.refresh(usuario)

        # Crear token JWT
        access_token = crear_token_acceso({"sub": usuario.id})

        # Obtener URL de redirección de la sesión
        final_redirect = request.session.pop('oauth_redirect', '/viralpost/app')

        # Redirigir al frontend con el token
        redirect_url = f"{final_redirect}?token={access_token}"
        return RedirectResponse(url=redirect_url)

    except Exception as e:
        # Obtener redirect de la sesión para el error también
        final_redirect = request.session.pop('oauth_redirect', '/viralpost/app')
        # En caso de error, redirigir al login con mensaje de error
        return RedirectResponse(url=f"/viralpost/login?error=google_auth_failed&redirect={final_redirect}")
