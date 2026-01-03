"""
ViralPost AI - Aplicación principal FastAPI
Generador de imágenes virales para redes sociales
"""
import os
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from app.core.config import settings
from app.core.database import init_db, close_db
from app.api.auth import router as auth_router
from app.api.generation import router as generation_router
from app.api.payments import router as payments_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja el ciclo de vida de la aplicación"""
    # Startup
    await init_db()

    # Crear directorios necesarios
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.GENERATED_DIR, exist_ok=True)

    yield

    # Shutdown
    await close_db()


# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/viralpost/docs",
    redoc_url="/viralpost/redoc",
    openapi_url="/viralpost/openapi.json"
)

# Session middleware (necesario para Google OAuth)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
static_path = Path(__file__).parent / "static"
templates_path = Path(__file__).parent / "templates"

app.mount("/viralpost/static", StaticFiles(directory=str(static_path)), name="static")

# Templates
templates = Jinja2Templates(directory=str(templates_path))

# Registrar routers de API
app.include_router(auth_router, prefix="/viralpost/api")
app.include_router(generation_router, prefix="/viralpost/api")
app.include_router(payments_router, prefix="/viralpost/api")


# ============ RUTAS DE FRONTEND ============

@app.get("/viralpost", response_class=HTMLResponse)
@app.get("/viralpost/", response_class=HTMLResponse)
async def pagina_principal(request: Request):
    """Página principal / Landing page"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "stripe_key": settings.STRIPE_PUBLISHABLE_KEY
    })


@app.get("/viralpost/app", response_class=HTMLResponse)
@app.get("/viralpost/app/", response_class=HTMLResponse)
async def pagina_app(request: Request):
    """Aplicación principal (dashboard)"""
    return templates.TemplateResponse("app.html", {
        "request": request,
        "stripe_key": settings.STRIPE_PUBLISHABLE_KEY
    })


@app.get("/viralpost/login", response_class=HTMLResponse)
async def pagina_login(request: Request):
    """Página de login"""
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/viralpost/registro", response_class=HTMLResponse)
async def pagina_registro(request: Request):
    """Página de registro"""
    return templates.TemplateResponse("registro.html", {"request": request})


@app.get("/viralpost/creditos", response_class=HTMLResponse)
async def pagina_creditos(request: Request):
    """Página de compra de créditos"""
    return templates.TemplateResponse("creditos.html", {
        "request": request,
        "stripe_key": settings.STRIPE_PUBLISHABLE_KEY
    })


@app.get("/viralpost/pago-exitoso", response_class=HTMLResponse)
async def pagina_pago_exitoso(request: Request):
    """Página de confirmación de pago"""
    return templates.TemplateResponse("pago_exitoso.html", {"request": request})


@app.get("/viralpost/historial", response_class=HTMLResponse)
async def pagina_historial(request: Request):
    """Página de historial de generaciones"""
    return templates.TemplateResponse("historial.html", {"request": request})


@app.get("/viralpost/terminos", response_class=HTMLResponse)
async def pagina_terminos(request: Request):
    """Página de términos de servicio"""
    return templates.TemplateResponse("terminos.html", {"request": request})


@app.get("/viralpost/privacidad", response_class=HTMLResponse)
async def pagina_privacidad(request: Request):
    """Página de política de privacidad"""
    return templates.TemplateResponse("privacidad.html", {"request": request})


@app.get("/viralpost/contacto", response_class=HTMLResponse)
async def pagina_contacto(request: Request):
    """Página de contacto"""
    return templates.TemplateResponse("contacto.html", {"request": request})


# ============ RUTA DE IMÁGENES GENERADAS ============

@app.get("/viralpost/imagenes/{filename}")
async def servir_imagen_generada(filename: str):
    """Sirve las imágenes generadas"""
    ruta = Path(settings.GENERATED_DIR) / filename
    if ruta.exists():
        return FileResponse(str(ruta))
    return {"error": "Imagen no encontrada"}


# ============ HEALTH CHECK ============

@app.get("/viralpost/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


# ============ WEBHOOK DE STRIPE (sin prefijo /api) ============

@app.post("/viralpost-stripe-webhook")
async def stripe_webhook_direct(request: Request):
    """
    Webhook de Stripe - endpoint directo para nginx
    Redirige al router de pagos
    """
    from app.api.payments import stripe_webhook
    from app.core.database import async_session_maker

    async with async_session_maker() as db:
        return await stripe_webhook(request, db)
