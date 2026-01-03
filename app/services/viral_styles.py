"""
Definición de estilos virales para generación de imágenes
Basado en el sistema de KNIME proporcionado
"""

# Sistema de estilos virales (8 categorías únicas)
VIRAL_STYLES = {
    "macro_explosion": {
        "id": "macro_explosion",
        "nombre": "Explosión Macro",
        "descripcion": "Fotografía macro extrema donde el producto explota mostrando sus componentes",
        "icono": "💥",
        "preview_color": "#FF6B35",
        "imagen_ejemplo": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop",
        "camera": "Extreme macro lens 100mm, f/1.4, focus stacking",
        "lighting": "Multiple rim lights creating product halo, dramatic shadows",
        "environment": "El producto EXPLOTA en sus componentes/ingredientes suspendidos en el aire como big bang culinario",
        "vfx": "Partículas flotando, gotas suspendidas mid-air, polvo cósmico",
        "mood": "Épico, científico, descubrimiento",
        "viral_hook": "Revela la 'anatomía secreta' del producto"
    },
    "liquid_metal": {
        "id": "liquid_metal",
        "nombre": "Metal Líquido",
        "descripcion": "Estética futurista con superficies cromadas y reflejos metálicos",
        "icono": "🪞",
        "preview_color": "#C0C0C0",
        "imagen_ejemplo": "https://images.unsplash.com/photo-1635322966219-b75ed372eb01?w=400&h=400&fit=crop",
        "camera": "Medium shot, 50mm anamorphic, shallow DOF with lens flares",
        "lighting": "Single hard light source creating mercury-like reflections",
        "environment": "El producto emerge de un charco de metal líquido cromado que refleja un cielo dramático",
        "vfx": "Gotas de cromo, reflejos imposibles, superficie especular perfecta",
        "mood": "Futurista, premium, tecnológico",
        "viral_hook": "Aesthetic satisfactorio de texturas líquidas"
    },
    "neon_noir": {
        "id": "neon_noir",
        "nombre": "Neon Noir Cyberpunk",
        "descripcion": "Atmósfera urbana nocturna con luces neón y lluvia",
        "icono": "🌃",
        "preview_color": "#FF00FF",
        "imagen_ejemplo": "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=400&h=400&fit=crop",
        "camera": "Dutch angle 15°, 35mm wide, deep shadows",
        "lighting": "Neon rosa/cyan como únicas fuentes, lluvia cayendo",
        "environment": "Callejón de Blade Runner con el producto como elemento central iluminado",
        "vfx": "Reflejos en charcos, humo volumétrico, rain streaks",
        "mood": "Misterioso, urbano, cinematográfico",
        "viral_hook": "Estética cyberpunk ultra-trendy"
    },
    "botanical_luxury": {
        "id": "botanical_luxury",
        "nombre": "Jardín Surrealista",
        "descripcion": "Naturaleza exuberante y flores exóticas en un entorno de lujo orgánico",
        "icono": "🌺",
        "preview_color": "#228B22",
        "imagen_ejemplo": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400&h=400&fit=crop",
        "camera": "Overhead 45°, 85mm portrait lens, creamy bokeh",
        "lighting": "Golden hour natural light filtering through leaves",
        "environment": "El producto crece orgánicamente de plantas exóticas, flores imposibles, naturaleza fantástica",
        "vfx": "Pétalos cayendo, rocío en superficies, raíces visibles",
        "mood": "Orgánico, lujoso, sostenible",
        "viral_hook": "Conexión naturaleza-producto para audiencias eco-conscious"
    },
    "zero_gravity": {
        "id": "zero_gravity",
        "nombre": "Gravedad Cero",
        "descripcion": "Todo flota en un ambiente espacial de microgravedad",
        "icono": "🚀",
        "preview_color": "#1E90FF",
        "imagen_ejemplo": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=400&h=400&fit=crop",
        "camera": "Low angle heroic shot, 24mm wide, everything floating",
        "lighting": "Soft wraparound light como estación espacial, rim light azul",
        "environment": "Interior de nave espacial con el producto y sus elementos flotando en microgravedad",
        "vfx": "Burbujas de líquido esféricas, cables flotantes, luz solar entrando por ventana",
        "mood": "Innovador, aventurero, único",
        "viral_hook": "Física imposible = scroll-stopping"
    },
    "miniature_world": {
        "id": "miniature_world",
        "nombre": "Mundo Miniatura",
        "descripcion": "Perspectiva de diorama donde el producto es gigante",
        "icono": "🏙️",
        "preview_color": "#FFD700",
        "imagen_ejemplo": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop",
        "camera": "Tilt-shift lens effect, producto gigante, perspectiva forzada",
        "lighting": "Soft diffused daylight, sombras suaves de escala real",
        "environment": "El producto es GIGANTE en una ciudad miniatura donde personas diminutas interactúan con él",
        "vfx": "Escala imposible, detalles microscópicos en ciudad, efecto diorama",
        "mood": "Fantástico, memorable, storytelling",
        "viral_hook": "Perspectiva inesperada genera engagement"
    },
    "frozen_time": {
        "id": "frozen_time",
        "nombre": "Tiempo Congelado",
        "descripcion": "Captura el momento exacto de una acción congelada en el tiempo",
        "icono": "⏱️",
        "preview_color": "#00CED1",
        "imagen_ejemplo": "https://images.unsplash.com/photo-1509773896068-7fd415d91e2e?w=400&h=400&fit=crop",
        "camera": "Bullet-time multi-angle, 200mm telephoto compression",
        "lighting": "Flash de alta velocidad, todo perfectamente nítido",
        "environment": "Momento exacto de acción CONGELADO: splash, impacto, derrame, caída",
        "vfx": "Gotas perfectamente esféricas, ondas de choque visibles, motion blur selectivo",
        "mood": "Dinámico, energético, impactante",
        "viral_hook": "Satisfacción visual de física capturada"
    },
    "dark_luxury": {
        "id": "dark_luxury",
        "nombre": "Lujo Oscuro",
        "descripcion": "Elegancia minimalista sobre fondo negro con acentos dorados",
        "icono": "✨",
        "preview_color": "#1a1a1a",
        "imagen_ejemplo": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400&h=400&fit=crop",
        "camera": "Straight-on symmetrical, 90mm macro, razor thin DOF",
        "lighting": "Single dramatic spotlight from above, rest in pure black",
        "environment": "Fondo negro absoluto, el producto flota en terciopelo de oscuridad con acentos dorados",
        "vfx": "Partículas de oro flotando, humo negro elegante, reflejos mínimos calculados",
        "mood": "Exclusivo, misterioso, deseable",
        "viral_hook": "Elegancia minimalista de alto contraste"
    }
}


def obtener_estilo(estilo_id: str) -> dict:
    """Obtiene la configuración de un estilo por ID"""
    return VIRAL_STYLES.get(estilo_id, VIRAL_STYLES["macro_explosion"])


def obtener_todos_estilos() -> list:
    """Retorna lista de todos los estilos disponibles"""
    return [
        {
            "id": style["id"],
            "nombre": style["nombre"],
            "descripcion": style["descripcion"],
            "icono": style["icono"],
            "preview_color": style["preview_color"],
            "imagen_ejemplo": style.get("imagen_ejemplo", "")
        }
        for style in VIRAL_STYLES.values()
    ]


def construir_prompt_imagen(
    estilo_id: str,
    nombre_producto: str,
    descripcion_producto: str,
    marca: str = None,
    tiene_logo: bool = False
) -> str:
    """
    Construye el prompt maestro para generación de imagen
    basado en el estilo seleccionado
    """
    style = obtener_estilo(estilo_id)

    # Instrucciones de logo
    if tiene_logo:
        instruccion_logo = """### LOGO OFICIAL (Imagen del logo proporcionada)
- INTEGRACIÓN FÍSICA OBLIGATORIA: El logo debe estar FABRICADO en la escena.
- Opciones: grabado en metal, bordado en tela, neón real, tallado en madera, impreso en material del producto.
- PROHIBIDO: Logo flotando, pegado digitalmente, o sobrepuesto como watermark."""
    else:
        instruccion_logo = """### LOGO (Crear tipográfico si hay marca)
- Diseña logotipo elegante usando el nombre de la marca.
- Debe estar físicamente integrado en un material de la escena."""

    prompt = f"""
##############################################
#  SISTEMA DE GENERACIÓN VIRAL              #
##############################################

### BRIEF DEL PRODUCTO
- **Producto:** {nombre_producto}
- **Descripción:** {descripcion_producto or 'No especificada'}
- **Marca:** {marca or 'No especificada'}

REGLA DE ORO: Jamás inventar precios, promociones o información no proporcionada.

--------------------------------------------------
### ESTILO VISUAL: {style['nombre'].upper()}
--------------------------------------------------

**CÁMARA:**
{style['camera']}

**ILUMINACIÓN:**
{style['lighting']}

**ENTORNO/CONCEPTO:**
{style['environment']}

**EFECTOS VISUALES:**
{style['vfx']}

**MOOD/EMOCIÓN:**
{style['mood']}

--------------------------------------------------
### REGLAS DE PRODUCCIÓN CINEMATOGRÁFICA
--------------------------------------------------

**1. EL PRODUCTO COMO HÉROE ABSOLUTO**
- Replica EXACTAMENTE el producto de la imagen adjunta.
- Fidelidad 100% en: colores, forma, etiquetas, proporciones.
- El producto debe verse REAL, no renderizado ni plástico.

**2. FÍSICA REAL (CON LICENCIA CREATIVA)**
- Respeta gravedad, reflejos, sombras coherentes.
- Los materiales deben comportarse como en realidad.
- La "magia" viene del CONCEPTO, no de física rota.

{instruccion_logo}

**4. COMPOSICIÓN PARA SCROLL-STOPPING**
- Punto focal inmediatamente claro.
- Contraste dramático figura-fondo.
- Detalle que recompense el zoom.
- Aspecto ratio: 1:1 (optimizado para Instagram/Facebook).

--------------------------------------------------
### OUTPUT REQUERIDO (JSON)
--------------------------------------------------
```json
{{
  "image_prompt": "Prompt detallado en INGLÉS para generación de imagen. Incluir: estilo visual, cámara, iluminación, ambiente. Mínimo 100 palabras.",
  "facebook": {{
    "copy": "Texto para Facebook en español mexicano (máx 280 chars). SIN mencionar el estilo visual, solo hablar del producto.",
    "hashtags": ["#relevante1", "#relevante2", "#viral"]
  }},
  "instagram": {{
    "copy": "Texto para Instagram en español mexicano (máx 150 chars). SIN mencionar el estilo visual.",
    "hashtags": ["#insta1", "#insta2", "#aesthetic"]
  }}
}}
```

IMPORTANTE PARA COPY DE REDES:
- PROHIBIDO mencionar el estilo visual en el copy
- El copy debe hablar SOLO del PRODUCTO REAL: sabor, beneficios, características
- Tono: natural, atractivo, directo. Como lo escribiría el dueño del negocio.
"""

    return prompt
