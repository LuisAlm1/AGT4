"""
Servicio de generación de imágenes usando OpenAI (prompts) y Gemini (imágenes)
"""
import os
import json
import base64
import httpx
import asyncio
from datetime import datetime
from typing import Optional, Tuple
from pathlib import Path
import re

from app.core.config import settings
from app.services.viral_styles import construir_prompt_imagen, obtener_estilo


class GenerationService:
    """Servicio para generar imágenes virales"""

    def __init__(self):
        self.openai_key = settings.OPENAI_API_KEY
        self.gemini_key = settings.GEMINI_API_KEY
        self.openai_model = settings.OPENAI_MODEL
        self.gemini_model = settings.GEMINI_MODEL

    async def generar_contenido_completo(
        self,
        estilo_id: str,
        nombre_producto: str,
        descripcion_producto: str,
        marca: str,
        imagen_producto_b64: str,
        logo_b64: Optional[str] = None,
        imagen_mime: str = "image/jpeg",
        logo_mime: str = "image/png"
    ) -> dict:
        """
        Genera imagen y copy completo para redes sociales

        Retorna:
        {
            "imagen_b64": str,
            "copy_facebook": str,
            "hashtags_facebook": list,
            "copy_instagram": str,
            "hashtags_instagram": list,
            "prompt_usado": str,
            "tiempo_ms": int
        }
        """
        inicio = datetime.now()

        try:
            # 1. Generar prompt y copy con OpenAI
            prompt_sistema = construir_prompt_imagen(
                estilo_id=estilo_id,
                nombre_producto=nombre_producto,
                descripcion_producto=descripcion_producto,
                marca=marca,
                tiene_logo=logo_b64 is not None
            )

            contenido_ai = await self._llamar_openai(
                prompt_sistema,
                imagen_producto_b64,
                imagen_mime
            )

            # Parsear respuesta JSON de OpenAI
            datos_generados = self._parsear_respuesta_openai(contenido_ai)

            # 2. Generar imagen con Gemini
            prompt_imagen = datos_generados.get("image_prompt", "")
            if not prompt_imagen:
                raise ValueError("OpenAI no generó un prompt de imagen válido")

            # Agregar contexto del estilo al prompt
            estilo = obtener_estilo(estilo_id)
            prompt_completo = f"""
Create a professional viral product photo with these specifications:

STYLE: {estilo['nombre']} - {estilo['mood']}
CAMERA: {estilo['camera']}
LIGHTING: {estilo['lighting']}
ENVIRONMENT: {estilo['environment']}
VFX: {estilo['vfx']}

PRODUCT DETAILS:
{prompt_imagen}

The product shown in the reference image must be replicated EXACTLY with perfect fidelity to colors, shape, labels and proportions. Create a stunning, scroll-stopping image optimized for social media (1:1 aspect ratio).
"""

            imagen_generada_b64 = await self._llamar_gemini(
                prompt_completo,
                imagen_producto_b64,
                imagen_mime,
                logo_b64,
                logo_mime
            )

            fin = datetime.now()
            tiempo_ms = int((fin - inicio).total_seconds() * 1000)

            return {
                "imagen_b64": imagen_generada_b64,
                "copy_facebook": datos_generados.get("facebook", {}).get("copy", ""),
                "hashtags_facebook": datos_generados.get("facebook", {}).get("hashtags", []),
                "copy_instagram": datos_generados.get("instagram", {}).get("copy", ""),
                "hashtags_instagram": datos_generados.get("instagram", {}).get("hashtags", []),
                "prompt_usado": prompt_imagen,
                "tiempo_ms": tiempo_ms,
                "exito": True
            }

        except Exception as e:
            fin = datetime.now()
            tiempo_ms = int((fin - inicio).total_seconds() * 1000)
            return {
                "exito": False,
                "error": str(e),
                "tiempo_ms": tiempo_ms
            }

    async def _llamar_openai(
        self,
        prompt: str,
        imagen_b64: str,
        mime_type: str = "image/jpeg"
    ) -> str:
        """Llama a OpenAI para generar prompt y copy"""
        url = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.openai_model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{imagen_b64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        return data["choices"][0]["message"]["content"]

    async def _llamar_gemini(
        self,
        prompt: str,
        imagen_producto_b64: str,
        imagen_mime: str,
        logo_b64: Optional[str] = None,
        logo_mime: str = "image/png"
    ) -> str:
        """Llama a Gemini para generar la imagen"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.gemini_model}:generateContent"

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.gemini_key
        }

        # Construir partes del contenido
        parts = [{"text": prompt}]

        # Agregar imagen del producto
        parts.append({
            "inline_data": {
                "mime_type": imagen_mime,
                "data": imagen_producto_b64
            }
        })

        # Agregar logo si existe
        if logo_b64:
            parts.append({
                "inline_data": {
                    "mime_type": logo_mime,
                    "data": logo_b64
                }
            })

        payload = {
            "contents": [{"parts": parts}],
            "generationConfig": {
                "responseModalities": ["TEXT", "IMAGE"]
            }
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        # Extraer imagen de la respuesta
        candidates = data.get("candidates", [])
        if not candidates:
            raise ValueError("Gemini no retornó candidatos")

        parts = candidates[0].get("content", {}).get("parts", [])
        for part in parts:
            inline_data = part.get("inlineData") or part.get("inline_data")
            if inline_data and "data" in inline_data:
                return inline_data["data"]

        raise ValueError("Gemini no generó una imagen")

    def _parsear_respuesta_openai(self, contenido: str) -> dict:
        """Parsea la respuesta JSON de OpenAI"""
        try:
            # Buscar JSON en la respuesta
            json_match = re.search(r'\{[\s\S]*\}', contenido)
            if json_match:
                return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

        # Fallback si no hay JSON válido
        return {
            "image_prompt": contenido[:500],
            "facebook": {"copy": "", "hashtags": []},
            "instagram": {"copy": "", "hashtags": []}
        }


def guardar_imagen(imagen_b64: str, nombre_archivo: str) -> str:
    """Guarda imagen en disco y retorna la ruta"""
    directorio = Path(settings.GENERATED_DIR)
    directorio.mkdir(parents=True, exist_ok=True)

    ruta = directorio / nombre_archivo
    with open(ruta, "wb") as f:
        f.write(base64.b64decode(imagen_b64))

    return str(ruta)


def imagen_a_base64(ruta_archivo: str) -> Tuple[str, str]:
    """Lee imagen de disco y retorna (base64, mime_type)"""
    with open(ruta_archivo, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")

    ext = Path(ruta_archivo).suffix.lower()
    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp"
    }
    mime = mime_types.get(ext, "image/jpeg")

    return data, mime


# Instancia global del servicio
generation_service = GenerationService()
