"""
Modelo de Transacciones (pagos de créditos)
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class EstadoTransaccion(str, enum.Enum):
    """Estados de la transacción"""
    PENDIENTE = "pendiente"
    COMPLETADA = "completada"
    FALLIDA = "fallida"
    REEMBOLSADA = "reembolsada"


class Transaction(Base):
    """Modelo de transacción de pago"""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Stripe
    stripe_payment_intent_id = Column(String(100), unique=True, nullable=True)
    stripe_checkout_session_id = Column(String(100), unique=True, nullable=True)

    # Detalles
    creditos = Column(Integer, nullable=False)
    monto_mxn = Column(Float, nullable=False)
    monto_usd = Column(Float, nullable=True)

    # Estado
    estado = Column(String(20), default=EstadoTransaccion.PENDIENTE.value)

    # Metadata
    descripcion = Column(String(200), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relaciones
    user = relationship("User", back_populates="transacciones")
