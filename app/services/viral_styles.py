"""
Definición de estilos virales para generación de imágenes
Basado en el sistema de KNIME proporcionado
"""

# Categorías de giros de negocio
CATEGORIAS_GIRO = {
    "comida": {
        "id": "comida",
        "nombre": "Comida y Bebidas",
        "icono": "🍕",
        "descripcion": "Restaurantes, panaderías, cafeterías, productos alimenticios"
    },
    "moda": {
        "id": "moda",
        "nombre": "Moda y Accesorios",
        "icono": "👗",
        "descripcion": "Ropa, zapatos, bolsas, joyería, accesorios"
    },
    "tecnologia": {
        "id": "tecnologia",
        "nombre": "Tecnología y Gadgets",
        "icono": "📱",
        "descripcion": "Electrónicos, gadgets, software, apps"
    },
    "belleza": {
        "id": "belleza",
        "nombre": "Belleza y Cosmética",
        "icono": "💄",
        "descripcion": "Maquillaje, skincare, productos de belleza"
    },
    "hogar": {
        "id": "hogar",
        "nombre": "Hogar y Decoración",
        "icono": "🏠",
        "descripcion": "Muebles, decoración, artículos para el hogar"
    },
    "todos": {
        "id": "todos",
        "nombre": "Ver Todos",
        "icono": "✨",
        "descripcion": "Todos los estilos disponibles"
    }
}

# Sistema de estilos virales (8 categorías únicas) - Especificaciones Cinematográficas Profesionales
VIRAL_STYLES = {
    "macro_explosion": {
        "id": "macro_explosion",
        "nombre": "Explosión Macro",
        "descripcion": "Fotografía macro extrema donde el producto explota mostrando sus componentes",
        "icono": "💥",
        "preview_color": "#FF6B35",
        "imagen_ejemplo": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop",
        "categorias": ["comida", "tecnologia", "belleza"],
        # CINEMATOGRAFÍA PROFESIONAL
        "camera": "Laowa 100mm f/2.8 2X Ultra Macro APO lens, shot at f/5.6 for focus stacking, 8K RED V-RAPTOR sensor, 1/2000s freeze frame, probe lens perspective for impossible angles",
        "lighting": "4-point lighting rig: Key light (ARRI SkyPanel S60-C at 5600K, 45° camera left), 2x Aputure 600d as rim lights creating dramatic product halo (backlit at 135° and 225°), fill bounce card at 2:1 ratio, dedicated macro ring light for shadow fill on details",
        "environment": "El producto EXPLOTA en sus componentes/ingredientes suspendidos en el aire como big bang culinario. Captured in controlled studio with phantom high-speed reference. Black gradient seamless backdrop transitioning to warm amber. Each particle individually lit.",
        "vfx": "Practical effects with compressed air bursts, real ingredient particles captured at 10,000fps, atomized liquid droplets, fine powder suspended with precise air cannons, subtle lens dust particles, volumetric light rays through particles",
        "color_grade": "Kodak Vision3 500T film emulation, pushed 1 stop. Warm shadows, vibrant product colors. Contrast ratio 6:1. Subtle orange/teal split toning in shadows/highlights",
        "composition": "Center-weighted with rule of thirds breakout particles. Leading lines from explosion toward product center. Negative space intentionally asymmetric for dynamic tension. 1:1 aspect optimized for social",
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
        "categorias": ["tecnologia", "moda", "belleza"],
        # CINEMATOGRAFÍA PROFESIONAL
        "camera": "Cooke Anamorphic 50mm T2.3 SF (Special Flare) lens, 2.39:1 desqueezed to 1:1 crop. Alexa Mini LF large format sensor for shallow DOF and characteristic oval bokeh. Focus pull on product emergence.",
        "lighting": "Single ARRI M40 HMI with mirror ball reflection setup creating mercury-like specular highlights. 12x12 ultrabounce for soft ambient fill at 8:1 ratio. Dedicated practical chrome sphere reference for reflection mapping. Underwater-style caustics projected on background.",
        "environment": "El producto emerge de un charco de metal líquido cromado (practical galinstan or CG mercury simulation) que refleja un cielo dramático con storm clouds. Reflective floor creates infinite mirror effect. Chrome environment dome for 360° reflections.",
        "vfx": "Practical chrome/mercury liquid effects combined with fluid simulation. Dripping metal strands, impossible physics reflections showing product from multiple angles simultaneously, rippling surface distortion, lens chromatic aberration on bright reflections",
        "color_grade": "Blade Runner 2049 inspired. Roger Deakins' sodium vapor palette. Desaturated environment with product colors popping. Highlight rolloff to creamy whites. Shadow detail crushed to pure black. Heavy atmosphere haze.",
        "composition": "Golden spiral composition with product at fibonacci focal point. Reflection creates visual dialogue. Anamorphic horizontal lens flares as leading lines toward product. Dutch angle 7° for subtle unease.",
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
        "categorias": ["tecnologia", "moda"],
        # CINEMATOGRAFÍA PROFESIONAL
        "camera": "Zeiss Supreme Prime 35mm T1.5, Dutch angle 12°, shot wide open for maximum bokeh and glow bleed. Sony Venice 2 sensor with dual ISO for extreme low-light latitude. Slight camera movement suggests handheld energy.",
        "lighting": "Zero traditional key light - only practicals. Primary: Quasar Science Rainbow 2 tubes (magenta R: 255, G: 0, B: 180) and (cyan R: 0, G: 255, B: 255) as competing sources at 90° angles. Secondary: Astera Titan tubes for background accent. Negative fill opposite key for deep shadows (10:1 ratio). Atmospheric haze from MDG hazer.",
        "environment": "Bar/lounge cyberpunk futurista con el producto exhibido elegantemente. Reflective wet surfaces (glycerin on black plexi). Background bokeh of distant city lights. Kanji signage glow. Steam vents. Holographic displays as out-of-focus elements.",
        "vfx": "Practical rain machine with backlit droplets, animated neon flicker (12% variation), lens moisture droplets, steam wisps from practical steamers, subtle chromatic aberration on neon sources, visible light rays through haze",
        "color_grade": "Wong Kar-wai meets Blade Runner. Crushed blacks with magenta/cyan split. Halation bloom on neon sources. FilmConvert Nitrate with Kodak 5219 stock. Pushed 2 stops in post. Heavy grain (ISO 3200 simulation). Cross-processed look in midtones.",
        "composition": "Off-center product placement using negative space. Depth layers: foreground bokeh elements, product focus plane, background neon blur. Converging perspective lines from architecture. Frame within frame using doorways/windows.",
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
        "categorias": ["comida", "belleza", "hogar"],
        # CINEMATOGRAFÍA PROFESIONAL
        "camera": "Canon CN-E 85mm T1.3 L F Cinema Prime, shot at T2 for creamy separation. 45° overhead angle on slider for subtle movement. RED Komodo 6K for organic skin-tone science. Macro diopter for foreground floral blur.",
        "lighting": "Simulated golden hour: ARRI SkyPanel S360-C through 12x12 Light Grid Cloth at 3200K with CTO gel. Practical sunbeams through plant leaves using Dedolight projector with custom gobo. Background 1 stop underexposed. Reflector bounce for gentle fill at 3:1 ratio.",
        "environment": "El producto crece orgánicamente de plantas exóticas, flores imposibles, naturaleza fantástica. Practical botanical set with real exotic plants (orchids, monstera, birds of paradise). Morning dew from glycerin/water mix. Moss ground cover. Visible roots breaking through soil.",
        "vfx": "Practical falling petals on monofilament, misting for atmosphere, water droplets from fine spray nozzle, subtle flower movement from hidden fan, dust motes in light beams (practical fuller's earth), occasional butterfly or bee element",
        "color_grade": "Terrence Malick's nature photography meets Gucci campaign. Lifted shadows with green bias. Highlight protection for skin/flower detail. Split tone: shadows olive, highlights peachy. Kodak Portra 400 emulation. Subtle vignette drawing eye to center.",
        "composition": "Overhead 45° angle with product at optical center. Botanical elements frame product in circular wreath pattern. Layered depth: macro foreground flowers, sharp product, soft background foliage. Organic asymmetry following Fibonacci spiral.",
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
        "categorias": ["tecnologia", "comida", "belleza"],
        # CINEMATOGRAFÍA PROFESIONAL
        "camera": "Zeiss Master Prime 24mm T1.4 for heroic wide perspective. Low angle (15° up) shooting toward floating elements. ARRI Alexa 65 for maximum detail in floating particles. High frame rate 120fps for potential slow-motion elements.",
        "lighting": "Wraparound soft key from ARRI SkyPanel S120-C (simulating space station interior panels) at 6500K daylight. Hard backlight through window cutout simulating direct sunlight (Mole-Richardson 20K fresnel at 5600K). Blue rim light (RGB tube) for zero-G atmosphere. Ratio: Key 4:1 to fill, backlight 2 stops over key.",
        "environment": "Interior de nave espacial con el producto y sus elementos flotando en microgravedad. Practical wire rig with invisible monofilament. White/grey spacecraft panels with subtle blue accent lights. Circular window showing Earth curve. Control panels with practical LEDs. Floating cables and small objects.",
        "vfx": "Wire removal for suspension rigs, perfectly spherical liquid bubbles (practical glycerin orbs), floating fabric/hair simulation, lens dust particles, subtle star field through windows, interactive reflections on helmet visor, caustic light patterns from liquid spheres",
        "color_grade": "Gravity (2013) / Interstellar reference. Clean whites for spacecraft interior. Earth-blue bounce light. High contrast for space exterior shots. Desaturated shadows, saturated Earth tones. ACES workflow with careful highlight rolloff for window blowout.",
        "composition": "Low angle heroic framing. Product at golden ratio intersection. Floating elements create circular movement around product. Depth: foreground floating particles, product mid-ground, spacecraft/window background. Diagonal tension lines from floating cables.",
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
        "categorias": ["comida", "tecnologia", "moda", "belleza", "hogar"],
        # CINEMATOGRAFÍA PROFESIONAL
        "camera": "Canon TS-E 90mm f/2.8L Macro Tilt-Shift for selective focus plane. Extreme aperture f/16-22 for forced miniature depth. Overhead crane perspective 60° down. Hasselblad X2D 100MP for extreme detail in miniature elements.",
        "lighting": "Simulated overcast day: 20x20 silk overhead with ARRI M90 through 1/2 grid cloth at 5600K. Soft wrap-around suggesting outdoor ambient. Small LED practicals for miniature building windows. No harsh shadows to maintain scale illusion. Ratio 2:1 soft.",
        "environment": "El producto es GIGANTE en una ciudad miniatura donde personas diminutas interactúan con él. Highly detailed architectural model (1:87 HO scale) with real miniature cars, trees, and people. Forced perspective streets leading to product. Tiny workers, cranes, and construction equipment interacting with product.",
        "vfx": "Tilt-shift blur gradient emphasizing miniature scale, practical smoke from tiny chimneys, miniature traffic movement, tiny LED headlights, scale-accurate shadows, dust/atmosphere for aerial perspective, occasional tiny human interaction elements",
        "color_grade": "Wes Anderson meets Miyazaki. Pastel color palette with saturated accents. Lifted blacks for storybook feel. Consistent neutral whites. Cross-processed yellows in highlights. Subtle clarity boost for hyper-detail in miniatures. Light nostalgic grain.",
        "composition": "Overhead 60° angle emphasizing scale difference. Product as impossible skyscraper. Rule of thirds with miniature city filling frame. Leading lines from roads/rivers toward product. Tiny vehicles and people for scale reference. Frame balanced with architectural elements.",
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
        "categorias": ["comida", "belleza", "tecnologia"],
        # CINEMATOGRAFÍA PROFESIONAL
        "camera": "Canon 200mm f/2L IS lens for telephoto compression and isolation. 1/8000s shutter equivalent freeze. Phantom Flex4K high-speed reference at 3000fps. Multi-camera array for Matrix-style bullet-time (12 cameras at 15° intervals). Medium format Phase One for hero still.",
        "lighting": "Broncolor Scoro 3200 S flash system at 1/10000s t.1 duration for absolute freeze. 3-light setup: Key Para 222 at 45°, fill white v-flat at 4:1 ratio, backlight Strip at 180° creating liquid edge definition. Background lit separately 1 stop under.",
        "environment": "Momento exacto de acción CONGELADO: splash, impacto, derrame, caída. Black or gradient background isolating action. Perfect liquid crown formation. Suspended droplets with internal refraction. Impact ripples at peak formation. Zero motion blur, impossible sharpness.",
        "vfx": "Practical high-speed liquid capture, perfectly spherical droplets, visible shockwave displacement rings, splash corona formations, selective motion blur only on fastest elements, subtle time-slice ghosting effect, liquid tensile strings",
        "color_grade": "High contrast commercial look. Pure whites, deep blacks (20:1 ratio). Vibrant saturated product colors. Clean color science. Hyper-real clarity and sharpening on frozen elements. Subtle complementary color in shadows. No grain - clinical precision.",
        "composition": "Telephoto compression stacking liquid elements. Product dead-center with action radiating outward. Golden ratio placement of largest droplets. Symmetry broken by dynamic splash direction. Negative space for impact emphasis. Action frozen at mathematical peak.",
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
        "categorias": ["moda", "belleza", "tecnologia", "comida"],
        # CINEMATOGRAFÍA PROFESIONAL
        "camera": "Zeiss Otus 85mm f/1.4 for clinical sharpness with smooth rolloff. Shot at f/2.8 for razor DOF. Perfectly straight-on symmetrical framing. Phase One IQ4 150MP for luxury detail reproduction. Precise product placement on measured grid.",
        "lighting": "Single dramatic spotlight: ARRI Orbiter with 30° lens grid from directly above (0° azimuth) at 3200K tungsten for warmth. Rest of scene in pure black (negative fill 360°). Light ratio infinite (unmeasurable - spotlight to void). Subtle golden bounce card for shadow side kiss at 32:1 ratio.",
        "environment": "Fondo negro absoluto, el producto flota en terciopelo de oscuridad con acentos dorados. Black velvet sweep absorbing all light. Product on invisible black glass for subtle reflection. No visible ground plane. Floating gold leaf particles. Minimal gold accent elements (frame, line, geometric shape).",
        "vfx": "Practical gold leaf particles suspended in air, subtle elegant smoke wisps (black smoke on black = texture only), calculated specular highlights on product, invisible support rig, floating gold geometric elements, subtle lens breathing movement",
        "color_grade": "Chanel No. 5 commercial meets Tom Ford. Pure black crushing to #000000. Tungsten warmth on product (3200K bias). Gold accents at precise hex #D4AF37. Minimal highlight roll-off maintaining texture in whites. Zero midtone color cast. Contrast: 50:1 in final. No grain - ultimate precision.",
        "composition": "Perfect symmetry with product at mathematical center. Minimal negative space doctrine. Gold accent elements at 1/3 and 2/3 lines. Single-point focus, everything else falls to black. Circular spotlight creates natural vignette. Product floating creates aspirational 'untouchable' feel.",
        "mood": "Exclusivo, misterioso, deseable",
        "viral_hook": "Elegancia minimalista de alto contraste"
    }
}


def obtener_estilo(estilo_id: str) -> dict:
    """Obtiene la configuración de un estilo por ID"""
    return VIRAL_STYLES.get(estilo_id, VIRAL_STYLES["macro_explosion"])


def obtener_categorias() -> list:
    """Retorna lista de categorías de giro de negocio"""
    return [
        {
            "id": cat["id"],
            "nombre": cat["nombre"],
            "icono": cat["icono"],
            "descripcion": cat["descripcion"]
        }
        for cat in CATEGORIAS_GIRO.values()
    ]


def obtener_todos_estilos(categoria: str = None) -> list:
    """
    Retorna lista de todos los estilos disponibles.
    Si se proporciona una categoría, filtra por ella.
    """
    estilos = []
    for style in VIRAL_STYLES.values():
        # Si hay categoría y no es "todos", filtrar
        if categoria and categoria != "todos":
            if categoria not in style.get("categorias", []):
                continue

        estilos.append({
            "id": style["id"],
            "nombre": style["nombre"],
            "descripcion": style["descripcion"],
            "icono": style["icono"],
            "preview_color": style["preview_color"],
            "imagen_ejemplo": style.get("imagen_ejemplo", ""),
            "categorias": style.get("categorias", [])
        })

    return estilos


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
