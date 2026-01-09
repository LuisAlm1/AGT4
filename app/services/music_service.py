"""
Servicio de generación de música con IA usando OpenAI (prompts) y MusicGPT (música)
"""
import os
import json
import httpx
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

from app.core.config import settings


class MusicService:
    """Servicio para generar música con IA"""

    def __init__(self):
        self.openai_key = settings.OPENAI_API_KEY
        self.musicgpt_key = settings.MUSICGPT_API_KEY
        self.musicgpt_url = settings.MUSICGPT_API_URL
        self.openai_model = settings.OPENAI_MODEL

    async def generar_prompt_musical(
        self,
        descripcion: str,
        duracion: int = 30,
        genero: Optional[str] = None,
        mood: Optional[str] = None,
        es_instrumental: bool = False
    ) -> Dict[str, Any]:
        """
        Genera un prompt musical usando OpenAI basado en la descripción del producto/servicio.

        Retorna:
        {
            "music_prompt": str,  # Prompt para MusicGPT (máx 250 chars)
            "music_style": str,   # Estilo musical
            "mood": str,
            "genre": str,
            "lyrics_theme": str
        }
        """
        if not self.openai_key:
            # Fallback si no hay API key
            return {
                "music_prompt": "Catchy pop jingle, female vocals singing in Mexican Spanish, upbeat fun commercial vibe",
                "music_style": "Commercial Jingle, Latin Pop",
                "mood": "energetic",
                "genre": "pop jingle",
                "lyrics_theme": "promoción del producto"
            }

        system_prompt = """Eres un Director Musical experto en publicidad y jingles comerciales.
Analiza el brief y genera un prompt musical CON LETRA EN ESPAÑOL MEXICANO para MusicGPT.

REGLAS:
1. Prompt en INGLÉS (MusicGPT entiende mejor instrucciones en inglés)
2. Incluir: género, mood, tempo, instrumentos
3. CRÍTICO: Especificar "vocals singing in Mexican Spanish"
4. Las lyrics deben ser pegajosas y mencionar el producto/servicio
5. MÁXIMO 250 CARACTERES el prompt (esto es MUY IMPORTANTE, MusicGPT falla si es más largo)

OUTPUT JSON:
{
    "music_prompt": "Prompt CORTO de max 250 caracteres con 'vocals singing in Mexican Spanish'",
    "music_style": "Estilo para MusicGPT (ej: Commercial Jingle, Latin Pop)",
    "mood": "Estado de ánimo",
    "genre": "Género musical",
    "lyrics_theme": "Tema de la letra"
}"""

        user_content = f"Brief: {descripcion}\nDuración: {duracion}s\nPlataforma: Instagram/TikTok/YouTube"

        if genero:
            user_content += f"\nGénero preferido: {genero}"
        if mood:
            user_content += f"\nMood preferido: {mood}"
        if es_instrumental:
            user_content += "\nNOTA: Debe ser INSTRUMENTAL, sin voces."

        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.openai_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.7,
            "response_format": {"type": "json_object"}
        }

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload
                )

                if response.status_code == 200:
                    content = response.json()['choices'][0]['message']['content']
                    data = json.loads(content)

                    # Truncar prompt si es necesario
                    if len(data.get("music_prompt", "")) > 295:
                        data["music_prompt"] = data["music_prompt"][:292] + "..."

                    return data

        except Exception as e:
            print(f"[MUSIC] Error OpenAI: {e}")

        # Fallback
        return {
            "music_prompt": "Upbeat pop jingle, vocals in Mexican Spanish, catchy commercial tune, energetic beat",
            "music_style": "Commercial Jingle, Latin Pop, Catchy Spanish Vocals",
            "mood": "energetic",
            "genre": "pop jingle",
            "lyrics_theme": "beneficios del producto"
        }

    async def generar_musica(
        self,
        prompt: str,
        music_style: str = "Commercial Jingle, Latin Pop",
        es_instrumental: bool = False,
        duracion: int = 30
    ) -> Dict[str, Any]:
        """
        Genera música usando MusicGPT API.

        Retorna:
        {
            "exito": bool,
            "conversion_id": str,
            "error": str (si hay error)
        }
        """
        if not self.musicgpt_key:
            return {"exito": False, "error": "No hay API key de MusicGPT configurada"}

        # Truncar prompt a 295 caracteres (límite de MusicGPT es 300)
        if len(prompt) > 295:
            prompt = prompt[:292] + "..."

        # Asegurar formato del header
        if self.musicgpt_key.startswith("Bearer"):
            auth_header = self.musicgpt_key
        else:
            auth_header = f"Bearer {self.musicgpt_key}"

        headers = {
            "Authorization": auth_header,
            "Content-Type": "application/json"
        }

        payload = {
            "prompt": prompt,
            "music_style": music_style,
            "make_instrumental": es_instrumental,
            "duration": duracion
        }

        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    f"{self.musicgpt_url}/MusicAI",
                    headers=headers,
                    json=payload
                )

                if response.status_code != 200:
                    return {
                        "exito": False,
                        "error": f"Error API código {response.status_code}: {response.text}"
                    }

                data = response.json()

                if not data.get("success"):
                    return {
                        "exito": False,
                        "error": f"API respondió success=False: {data}"
                    }

                conversion_id = data.get("conversion_id") or data.get("conversion_id_1")
                if not conversion_id:
                    return {
                        "exito": False,
                        "error": "No se recibió conversion_id"
                    }

                return {
                    "exito": True,
                    "conversion_id": conversion_id
                }

        except Exception as e:
            return {"exito": False, "error": str(e)}

    async def poll_resultado(
        self,
        conversion_id: str,
        max_intentos: int = 60,
        delay: float = 2.0
    ) -> Dict[str, Any]:
        """
        Hace polling para obtener el resultado de MusicGPT.

        Retorna:
        {
            "exito": bool,
            "audio_url": str,
            "error": str (si hay error)
        }
        """
        if self.musicgpt_key.startswith("Bearer"):
            auth_header = self.musicgpt_key
        else:
            auth_header = f"Bearer {self.musicgpt_key}"

        headers = {"Authorization": auth_header}

        for i in range(1, max_intentos + 1):
            try:
                async with httpx.AsyncClient(timeout=30) as client:
                    response = await client.get(
                        f"{self.musicgpt_url}/byId",
                        headers=headers,
                        params={
                            "conversionType": "MUSIC_AI",
                            "conversion_id": conversion_id
                        }
                    )

                    if response.status_code == 200:
                        data = response.json()
                        conversion = data.get("conversion") or {}
                        status = conversion.get("status") or conversion.get("message")

                        if status in ("COMPLETED", "success"):
                            # Intentar obtener URL de varias formas
                            audio_url = conversion.get("audio_url")
                            path = conversion.get("conversion_path_1") or conversion.get("conversion_path_2")

                            if audio_url:
                                return {"exito": True, "audio_url": audio_url}
                            if path:
                                url = path if path.startswith("http") else f"https://lalals.s3.amazonaws.com/{path.lstrip('/')}"
                                return {"exito": True, "audio_url": url}

                        if status in ("FAILED", "ERROR"):
                            return {
                                "exito": False,
                                "error": f"Generación falló en el servidor: {conversion}"
                            }

            except Exception as e:
                print(f"[MUSIC] Error en poll: {e}")

            await asyncio.sleep(delay)

        return {"exito": False, "error": "Tiempo de espera agotado"}

    async def descargar_audio(self, audio_url: str, output_path: str) -> bool:
        """Descarga el archivo de audio."""
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.get(audio_url)
                if response.status_code == 200:
                    # Asegurar que el directorio existe
                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    return True
        except Exception as e:
            print(f"[MUSIC] Error descargando audio: {e}")
        return False

    async def generar_cancion_completa(
        self,
        titulo: str,
        descripcion: str,
        duracion: int = 30,
        genero: Optional[str] = None,
        mood: Optional[str] = None,
        es_instrumental: bool = False
    ) -> Dict[str, Any]:
        """
        Flujo completo: genera prompt con OpenAI y música con MusicGPT.

        Retorna:
        {
            "exito": bool,
            "audio_url": str,
            "prompt_usado": str,
            "music_style": str,
            "mood": str,
            "genre": str,
            "lyrics_theme": str,
            "tiempo_ms": int,
            "error": str (si hay error)
        }
        """
        inicio = datetime.now()

        try:
            # 1. Generar prompt con OpenAI
            prompt_data = await self.generar_prompt_musical(
                descripcion=descripcion,
                duracion=duracion,
                genero=genero,
                mood=mood,
                es_instrumental=es_instrumental
            )

            music_prompt = prompt_data.get("music_prompt", "")
            music_style = prompt_data.get("music_style", "Commercial Jingle, Latin Pop")

            if not music_prompt:
                return {"exito": False, "error": "No se pudo generar prompt musical"}

            # 2. Solicitar generación a MusicGPT
            gen_result = await self.generar_musica(
                prompt=music_prompt,
                music_style=music_style,
                es_instrumental=es_instrumental,
                duracion=duracion
            )

            if not gen_result.get("exito"):
                return {
                    "exito": False,
                    "error": gen_result.get("error", "Error en generación"),
                    "prompt_usado": music_prompt
                }

            conversion_id = gen_result.get("conversion_id")

            # 3. Esperar resultado (polling)
            poll_result = await self.poll_resultado(conversion_id)

            if not poll_result.get("exito"):
                return {
                    "exito": False,
                    "error": poll_result.get("error", "Error en polling"),
                    "prompt_usado": music_prompt,
                    "conversion_id": conversion_id
                }

            tiempo_ms = int((datetime.now() - inicio).total_seconds() * 1000)

            return {
                "exito": True,
                "audio_url": poll_result.get("audio_url"),
                "conversion_id": conversion_id,
                "prompt_usado": music_prompt,
                "music_style": music_style,
                "mood": prompt_data.get("mood", ""),
                "genre": prompt_data.get("genre", ""),
                "lyrics_theme": prompt_data.get("lyrics_theme", ""),
                "tiempo_ms": tiempo_ms
            }

        except Exception as e:
            return {"exito": False, "error": str(e)}


# Instancia global del servicio
music_service = MusicService()
