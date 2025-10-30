#!/bin/bash

# Script para desplegar Pokeneas en Docker Swarm
# Uso: ./deploy.sh <dockerhub-username>

if [ $# -eq 0 ]; then
    echo "❌ Error: Debes proporcionar tu nombre de usuario de DockerHub"
    echo "Uso: ./deploy.sh <dockerhub-username>"
    exit 1
fi

DOCKERHUB_USERNAME=$1
SERVICE_NAME="pokeneas-service"
IMAGE_NAME="$DOCKERHUB_USERNAME/pokeneas-app:latest"

echo "🏔️  Desplegando Pokeneas de Antioquia en Docker Swarm"
echo "=================================================="

# Verificar que estamos en un nodo manager
if ! docker node ls > /dev/null 2>&1; then
    echo "❌ Error: No estás en un nodo manager de Docker Swarm"
    echo "💡 Ejecuta este script en la instancia líder del cluster"
    exit 1
fi

echo "✅ Verificado: Estás en un nodo manager"

# Verificar que la imagen existe
echo "🔍 Verificando imagen: $IMAGE_NAME"
if ! docker pull $IMAGE_NAME > /dev/null 2>&1; then
    echo "❌ Error: No se pudo descargar la imagen $IMAGE_NAME"
    echo "💡 Asegúrate de que:"
    echo "   1. La imagen existe en DockerHub"
    echo "   2. GitHub Actions haya construido la imagen correctamente"
    echo "   3. El nombre de usuario sea correcto"
    exit 1
fi

echo "✅ Imagen encontrada: $IMAGE_NAME"

# Eliminar servicio existente si existe
echo "🗑️  Eliminando servicio existente (si existe)..."
docker service rm $SERVICE_NAME > /dev/null 2>&1

# Crear nuevo servicio
echo "🚀 Creando servicio con 10 réplicas..."
docker service create \
    --name $SERVICE_NAME \
    --replicas 10 \
    --publish 80:80 \
    --env AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
    --env AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
    --env AWS_REGION="$AWS_REGION" \
    --env S3_BUCKET="$S3_BUCKET" \
    $IMAGE_NAME

if [ $? -eq 0 ]; then
    echo "✅ Servicio creado exitosamente!"
    echo ""
    echo "📊 Estado del servicio:"
    docker service ps $SERVICE_NAME
    
    echo ""
    echo "🌐 El servicio estará disponible en:"
    echo "   - http://<ip-instancia-lider>:80/"
    echo "   - http://<ip-instancia-lider>:80/pokenea"
    echo "   - http://<ip-instancia-lider>:80/imagen"
    
    echo ""
    echo "🔍 Para monitorear el servicio:"
    echo "   docker service ps $SERVICE_NAME"
    echo "   docker service logs $SERVICE_NAME"
    
else
    echo "❌ Error creando el servicio"
    exit 1
fi
