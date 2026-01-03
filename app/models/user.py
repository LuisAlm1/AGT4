"""
Modelo de Usuario
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    """Modelo de usuario"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    nombre = Column(String(100), nullable=True)

    # Créditos
    creditos = Column(Integer, default=0, nullable=False)
    creditos_usados = Column(Integer, default=0, nullable=False)

    # Estado
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # Stripe
    stripe_customer_id = Column(String(100), nullable=True, unique=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    generaciones = relationship("Generation", back_populates="user")
    transacciones = relationship("Transaction", back_populates="user")

    def tiene_creditos(self, cantidad: int = 1) -> bool:
        """Verifica si el usuario tiene suficientes créditos"""
        return self.creditos >= cantidad

    def usar_credito(self) -> bool:
        """Usa un crédito si está disponible"""
        if self.creditos >= 1:
            self.creditos -= 1
            self.creditos_usados += 1
            return True
        return False

    def agregar_creditos(self, cantidad: int):
        """Agrega créditos al usuario"""
        self.creditos += cantidad
