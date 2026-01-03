"""
Utilidades de seguridad: JWT y hashing de contraseñas
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User


# Contexto para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de seguridad Bearer
security = HTTPBearer()


def verificar_password(password_plano: str, password_hash: str) -> bool:
    """Verifica si la contraseña coincide con el hash"""
    return pwd_context.verify(password_plano, password_hash)


def hashear_password(password: str) -> str:
    """Genera hash de contraseña"""
    return pwd_context.hash(password)


def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un JWT token de acceso"""
    to_encode = data.copy()

    # Asegurar que sub sea string (estándar JWT)
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def verificar_token(token: str) -> Optional[dict]:
    """Verifica y decodifica un JWT token"""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None


async def obtener_usuario_actual(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Dependencia para obtener el usuario actual desde el token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    payload = verificar_token(token)

    if payload is None:
        raise credentials_exception

    # Obtener user_id y convertir a int (JWT puede devolverlo como string)
    user_id_raw = payload.get("sub")
    if user_id_raw is None:
        raise credentials_exception

    try:
        user_id = int(user_id_raw)
    except (ValueError, TypeError):
        raise credentials_exception

    # Buscar usuario en DB
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )

    return user


async def obtener_usuario_opcional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    ),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """Dependencia para obtener usuario si hay token, None si no"""
    if not credentials:
        return None

    try:
        return await obtener_usuario_actual(credentials, db)
    except HTTPException:
        return None
