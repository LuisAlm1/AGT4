# ViralPost AI 🚀

Generador de imágenes virales para redes sociales con inteligencia artificial.

## Características

- **8 Estilos Virales Únicos**: Desde explosiones macro hasta lujo oscuro
- **Generación con IA**: OpenAI GPT-4 para prompts + Google Gemini para imágenes
- **Copy para Redes Sociales**: Facebook e Instagram con hashtags optimizados
- **Sistema de Créditos**: 1 crédito = 1 generación completa
- **Pagos con Stripe**: Paquetes de 10, 25, 50 y 100 créditos
- **3 Créditos Gratis**: Al registrarse

## Estructura del Proyecto

```
AGT4/
├── app/
│   ├── api/              # Endpoints de la API
│   │   ├── auth.py       # Autenticación (registro, login)
│   │   ├── generation.py # Generación de imágenes
│   │   ├── payments.py   # Pagos con Stripe
│   │   └── schemas.py    # Esquemas Pydantic
│   ├── core/             # Configuración central
│   │   ├── config.py     # Settings de la app
│   │   ├── database.py   # SQLAlchemy async
│   │   └── security.py   # JWT y passwords
│   ├── models/           # Modelos de base de datos
│   │   ├── user.py
│   │   ├── generation.py
│   │   └── transaction.py
│   ├── services/         # Lógica de negocio
│   │   ├── generation.py # Servicio de generación
│   │   ├── stripe_service.py
│   │   └── viral_styles.py
│   ├── templates/        # HTML (Jinja2)
│   └── static/           # CSS, JS, imágenes
├── nginx/                # Configuración de nginx
├── scripts/              # Scripts de despliegue
├── requirements.txt
├── viralpost.service     # Servicio systemd
└── .env.example          # Plantilla de configuración
```

## Instalación

### 1. Clonar y configurar entorno

```bash
cd /home/user/AGT4
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
nano .env
```

Completa las siguientes claves:

| Variable | Descripción |
|----------|-------------|
| `SECRET_KEY` | Clave secreta para la app |
| `JWT_SECRET_KEY` | Clave para tokens JWT |
| `STRIPE_SECRET_KEY` | Clave secreta de Stripe (sk_live_...) |
| `STRIPE_PUBLISHABLE_KEY` | Clave pública de Stripe (pk_live_...) |
| `STRIPE_WEBHOOK_SECRET` | Secret del webhook (whsec_...) |
| `OPENAI_API_KEY` | API key de OpenAI |
| `GEMINI_API_KEY` | API key de Google Gemini |

### 3. Crear directorios

```bash
sudo mkdir -p /var/www/agathoscreative/viralpost/{uploads,generated}
sudo chown -R www-data:www-data /var/www/agathoscreative/viralpost
```

### 4. Configurar nginx

```bash
sudo cp nginx/agathoscreative_full.conf /etc/nginx/sites-available/agathoscreative.com
sudo ln -sf /etc/nginx/sites-available/agathoscreative.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. Configurar servicio systemd

```bash
sudo cp viralpost.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable viralpost
sudo systemctl start viralpost
```

### 6. Configurar webhook de Stripe

1. Ve a https://dashboard.stripe.com/webhooks
2. Crea un nuevo endpoint:
   - URL: `https://agathoscreative.com/viralpost-stripe-webhook`
   - Eventos: `checkout.session.completed`
3. Copia el "Signing secret" a `.env` como `STRIPE_WEBHOOK_SECRET`

## Uso

### URLs

| URL | Descripción |
|-----|-------------|
| `/viralpost` | Landing page |
| `/viralpost/app` | Aplicación (requiere login) |
| `/viralpost/login` | Iniciar sesión |
| `/viralpost/registro` | Crear cuenta |
| `/viralpost/creditos` | Comprar créditos |
| `/viralpost/historial` | Historial de generaciones |
| `/viralpost/docs` | Documentación API (Swagger) |

### API Endpoints

```
POST /viralpost/api/auth/registro     # Registrar usuario
POST /viralpost/api/auth/login        # Iniciar sesión
GET  /viralpost/api/auth/me           # Obtener perfil

GET  /viralpost/api/generacion/estilos    # Listar estilos
POST /viralpost/api/generacion/crear      # Generar imagen
GET  /viralpost/api/generacion/historial  # Ver historial

GET  /viralpost/api/pagos/paquetes    # Ver paquetes
POST /viralpost/api/pagos/checkout    # Crear checkout
```

## Estilos Virales

1. **💥 Explosión Macro** - Componentes flotando en el aire
2. **🪞 Metal Líquido** - Reflejos cromados futuristas
3. **🌃 Neon Noir** - Estética cyberpunk con luces neón
4. **🌺 Jardín Surrealista** - Naturaleza fantástica
5. **🚀 Gravedad Cero** - Todo flotando en microgravedad
6. **🏙️ Mundo Miniatura** - Perspectiva de diorama
7. **⏱️ Tiempo Congelado** - Acción suspendida
8. **✨ Lujo Oscuro** - Elegancia minimalista

## Precios (MXN)

| Paquete | Precio | Por Generación |
|---------|--------|----------------|
| 10 créditos | $30 | $3.00 |
| 25 créditos | $70 | $2.80 |
| 50 créditos | $130 | $2.60 |
| 100 créditos | $250 | $2.50 |

*Margen: 3x el costo de API*

## Comandos Útiles

```bash
# Ver logs
journalctl -u viralpost -f

# Reiniciar servicio
sudo systemctl restart viralpost

# Estado del servicio
sudo systemctl status viralpost

# Probar localmente
source venv/bin/activate
uvicorn app.main:app --reload --port 5001
```

## Tecnologías

- **Backend**: FastAPI + SQLAlchemy (async)
- **Frontend**: HTML + Tailwind CSS + JavaScript vanilla
- **Base de datos**: SQLite (puede migrar a PostgreSQL)
- **IA**: OpenAI GPT-4 + Google Gemini
- **Pagos**: Stripe Checkout
- **Servidor**: Uvicorn + nginx + systemd

## Licencia

Propietario - Agathoscreative.com
