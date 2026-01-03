#!/bin/bash
# ViralPost AI - Script de Despliegue
# Ejecutar como: sudo bash scripts/deploy.sh

set -e

echo "=========================================="
echo "  ViralPost AI - Despliegue"
echo "=========================================="

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Directorio del proyecto
PROJECT_DIR="/home/user/AGT4"
VENV_DIR="$PROJECT_DIR/venv"

# 1. Crear directorios necesarios
echo -e "${YELLOW}[1/7] Creando directorios...${NC}"
mkdir -p /var/www/agathoscreative/viralpost/uploads
mkdir -p /var/www/agathoscreative/viralpost/generated
chown -R www-data:www-data /var/www/agathoscreative/viralpost

# 2. Crear entorno virtual e instalar dependencias
echo -e "${YELLOW}[2/7] Instalando dependencias de Python...${NC}"
cd $PROJECT_DIR
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 3. Verificar archivo .env
echo -e "${YELLOW}[3/7] Verificando configuración...${NC}"
if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo -e "${YELLOW}ADVERTENCIA: No existe archivo .env${NC}"
    echo "Copia .env.example a .env y configura tus credenciales"
    cp $PROJECT_DIR/.env.example $PROJECT_DIR/.env
    echo "Archivo .env creado. DEBES editarlo con tus credenciales."
fi

# 4. Copiar configuración de nginx
echo -e "${YELLOW}[4/7] Configurando nginx...${NC}"
cp $PROJECT_DIR/nginx/agathoscreative_full.conf /etc/nginx/sites-available/agathoscreative.com
ln -sf /etc/nginx/sites-available/agathoscreative.com /etc/nginx/sites-enabled/

# Verificar configuración de nginx
nginx -t

# 5. Copiar servicio de systemd
echo -e "${YELLOW}[5/7] Configurando servicio systemd...${NC}"
cp $PROJECT_DIR/viralpost.service /etc/systemd/system/
systemctl daemon-reload

# 6. Iniciar servicios
echo -e "${YELLOW}[6/7] Iniciando servicios...${NC}"
systemctl enable viralpost
systemctl start viralpost
systemctl reload nginx

# 7. Verificar estado
echo -e "${YELLOW}[7/7] Verificando estado...${NC}"
sleep 2
if systemctl is-active --quiet viralpost; then
    echo -e "${GREEN}✓ ViralPost está corriendo${NC}"
else
    echo "✗ Error al iniciar ViralPost"
    systemctl status viralpost
fi

echo ""
echo "=========================================="
echo -e "${GREEN}  Despliegue completado${NC}"
echo "=========================================="
echo ""
echo "URLs:"
echo "  - Landing: https://agathoscreative.com/viralpost"
echo "  - App:     https://agathoscreative.com/viralpost/app"
echo "  - API:     https://agathoscreative.com/viralpost/docs"
echo ""
echo "Comandos útiles:"
echo "  - Ver logs:     journalctl -u viralpost -f"
echo "  - Reiniciar:    systemctl restart viralpost"
echo "  - Estado:       systemctl status viralpost"
echo ""
echo -e "${YELLOW}IMPORTANTE: Configura el webhook de Stripe en:${NC}"
echo "  https://dashboard.stripe.com/webhooks"
echo "  URL: https://agathoscreative.com/viralpost-stripe-webhook"
echo "  Eventos: checkout.session.completed"
echo ""
