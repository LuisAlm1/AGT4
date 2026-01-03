"""
Servicio de pagos con Stripe
"""
import stripe
from typing import Optional
from app.core.config import settings
from app.models.user import User

# Configurar Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    """Servicio para manejar pagos con Stripe"""

    # Paquetes de créditos disponibles
    # Costo por generación:
    # - Nano Banana Pro (imagen): $0.24 USD
    # - GPT-4o (prompts/copy): ~$0.03 USD
    # - Total costo: ~$0.27 USD
    # - Con margen 3x: ~$0.81 USD
    # - En MXN (~17.5): ~$14.18 MXN/crédito
    PAQUETES = [
        {
            "id": "pack_10",
            "creditos": 10,
            "precio_mxn": 150,
            "precio_centavos": 15000,
            "nombre": "10 Créditos",
            "descripcion": "Paquete básico - 10 generaciones"
        },
        {
            "id": "pack_25",
            "creditos": 25,
            "precio_mxn": 350,
            "precio_centavos": 35000,
            "nombre": "25 Créditos",
            "descripcion": "Paquete popular - 25 generaciones",
            "popular": True
        },
        {
            "id": "pack_50",
            "creditos": 50,
            "precio_mxn": 680,
            "precio_centavos": 68000,
            "nombre": "50 Créditos",
            "descripcion": "Paquete profesional - 50 generaciones"
        },
        {
            "id": "pack_100",
            "creditos": 100,
            "precio_mxn": 1290,
            "precio_centavos": 129000,
            "nombre": "100 Créditos",
            "descripcion": "Mejor valor - 100 generaciones",
            "mejor_valor": True
        }
    ]

    def obtener_paquetes(self) -> list:
        """Retorna los paquetes disponibles"""
        return self.PAQUETES

    def obtener_paquete(self, paquete_id: str) -> Optional[dict]:
        """Obtiene un paquete por ID"""
        for paquete in self.PAQUETES:
            if paquete["id"] == paquete_id:
                return paquete
        return None

    async def crear_o_obtener_customer(self, user: User) -> str:
        """
        Crea o obtiene el Stripe Customer ID para un usuario.
        Maneja el caso de cambio entre test/live mode creando un nuevo customer si es necesario.
        """
        if user.stripe_customer_id:
            # Verificar si el customer existe en el modo actual (test/live)
            try:
                stripe.Customer.retrieve(user.stripe_customer_id)
                return user.stripe_customer_id
            except stripe.error.InvalidRequestError:
                # El customer no existe en este modo (probablemente cambió de test a live)
                # Crear uno nuevo
                pass

        # Crear nuevo customer
        customer = stripe.Customer.create(
            email=user.email,
            name=user.nombre or user.email,
            metadata={
                "user_id": str(user.id)
            }
        )

        return customer.id

    async def crear_checkout_session(
        self,
        user: User,
        paquete_id: str,
        success_url: str,
        cancel_url: str
    ) -> dict:
        """
        Crea una sesión de checkout de Stripe

        Retorna:
        {
            "checkout_url": str,
            "session_id": str
        }
        """
        paquete = self.obtener_paquete(paquete_id)
        if not paquete:
            raise ValueError(f"Paquete no encontrado: {paquete_id}")

        customer_id = await self.crear_o_obtener_customer(user)

        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=["card", "oxxo"],
            line_items=[
                {
                    "price_data": {
                        "currency": "mxn",
                        "unit_amount": paquete["precio_centavos"],
                        "product_data": {
                            "name": paquete["nombre"],
                            "description": paquete["descripcion"],
                        },
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                "user_id": str(user.id),
                "paquete_id": paquete_id,
                "creditos": str(paquete["creditos"])
            },
            locale="es-419",  # Español latinoamericano
            payment_method_options={
                "oxxo": {
                    "expires_after_days": 3  # El voucher expira en 3 días
                }
            }
        )

        return {
            "checkout_url": session.url,
            "session_id": session.id
        }

    def verificar_webhook(self, payload: bytes, signature: str) -> dict:
        """
        Verifica y parsea un webhook de Stripe

        Retorna el evento verificado
        """
        try:
            event = stripe.Webhook.construct_event(
                payload,
                signature,
                settings.STRIPE_WEBHOOK_SECRET
            )
            return event
        except stripe.error.SignatureVerificationError:
            raise ValueError("Firma de webhook inválida")

    def procesar_checkout_completado(self, session: dict) -> dict:
        """
        Procesa un evento checkout.session.completed

        Retorna:
        {
            "user_id": int,
            "creditos": int,
            "monto_mxn": float,
            "session_id": str
        }
        """
        metadata = session.get("metadata", {})

        return {
            "user_id": int(metadata.get("user_id", 0)),
            "creditos": int(metadata.get("creditos", 0)),
            "monto_mxn": session.get("amount_total", 0) / 100,
            "session_id": session.get("id", ""),
            "paquete_id": metadata.get("paquete_id", "")
        }


# Instancia global
stripe_service = StripeService()
