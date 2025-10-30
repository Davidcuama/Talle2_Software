#!/bin/bash

# Script de configuración para instancias EC2
# Este script se ejecuta automáticamente al crear la instancia
# User Data en AWS EC2

echo "🏔️  Configurando instancia para Pokeneas de Antioquia"
echo "=================================================="

# Actualizar sistema
apt-get update -y
apt-get upgrade -y

# Instalar Docker
echo "🐳 Instalando Docker..."
apt-get install -y docker.io
systemctl start docker
systemctl enable docker

# Agregar usuario ubuntu al grupo docker
usermod -aG docker ubuntu

# Instalar Docker Compose
echo "🔧 Instalando Docker Compose..."
curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Instalar herramientas adicionales
echo "🛠️  Instalando herramientas adicionales..."
apt-get install -y curl wget git htop

# Configurar firewall
echo "🔥 Configurando firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 2376/tcp
ufw allow 2377/tcp
ufw allow 7946/tcp
ufw allow 7946/udp
ufw allow 4789/udp
ufw --force enable

# Crear directorio para la aplicación
mkdir -p /home/ubuntu/pokeneas
chown ubuntu:ubuntu /home/ubuntu/pokeneas

# Mostrar información del sistema
echo "📊 Información del sistema:"
echo "   Hostname: $(hostname)"
echo "   IP: $(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo "   Región: $(curl -s http://169.254.169.254/latest/meta-data/placement/region)"
echo "   Docker version: $(docker --version)"

echo ""
echo "✅ Configuración completada!"
echo "🚀 La instancia está lista para Docker Swarm"
echo ""
echo "📝 Próximos pasos:"
echo "   1. SSH a la instancia: ssh -i tu-key.pem ubuntu@<ip>"
echo "   2. En la instancia líder: docker swarm init"
echo "   3. En las otras: docker swarm join --token <token> <ip-lider>:2377"
echo "   4. Desplegar servicio: ./deploy.sh <dockerhub-username>"
