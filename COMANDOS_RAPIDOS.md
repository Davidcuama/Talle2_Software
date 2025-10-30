# Comandos Rápidos - Taller 2 Pokeneas

## 🚀 Comandos de Desarrollo

### Configurar entorno local:
```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp env.example .env
# Editar .env con tus credenciales AWS

# Ejecutar aplicación
python app.py
```

### Probar aplicación:
```bash
# Ejecutar pruebas
python test_app.py

# Configurar S3
python setup_s3.py
```

## 🐳 Comandos Docker

### Desarrollo local:
```bash
# Construir imagen
docker build -t pokeneas-app .

# Ejecutar contenedor
docker run -p 80:80 --env-file .env pokeneas-app

# Con docker-compose
docker-compose up --build
```

## ☁️ Comandos AWS

### Crear bucket S3:
```bash
# Usar el script de configuración
python setup_s3.py
```

### Crear instancias EC2:
1. Usar el script `ec2-setup.sh` como User Data
2. O ejecutar manualmente:
```bash
# En cada instancia EC2
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
```

## 🔄 Comandos Docker Swarm

### Configurar cluster:
```bash
# En instancia líder
docker swarm init

# Obtener token para managers
docker swarm join-token manager

# En otras instancias
docker swarm join --token <token> <ip-lider>:2377
```

### Desplegar servicio:
```bash
# Configurar variables de entorno
export AWS_ACCESS_KEY_ID="tu-key"
export AWS_SECRET_ACCESS_KEY="tu-secret"
export AWS_REGION="us-east-1"
export S3_BUCKET="tu-bucket"

# Desplegar
./deploy.sh tu-usuario-dockerhub
```

### Monitorear servicio:
```bash
# Ver estado de réplicas
docker service ps pokeneas-service

# Ver logs
docker service logs pokeneas-service

# Ver servicios
docker service ls

# Escalar servicio
docker service scale pokeneas-service=10
```

## 🔧 Comandos de Mantenimiento

### Limpiar recursos:
```bash
# Eliminar servicio
docker service rm pokeneas-service

# Salir del swarm
docker swarm leave --force

# Limpiar imágenes
docker image prune -a
```

### Debugging:
```bash
# Ver logs detallados
docker service logs --follow pokeneas-service

# Inspeccionar servicio
docker service inspect pokeneas-service

# Ver nodos del cluster
docker node ls
```

## 📊 URLs de Prueba

Una vez desplegado, probar estas URLs:
- `http://<ip-instancia>:80/` - Página principal
- `http://<ip-instancia>:80/pokenea` - JSON aleatorio
- `http://<ip-instancia>:80/imagen` - Imagen y frase

## 🆘 Troubleshooting

### Error de conexión S3:
```bash
# Verificar credenciales
aws configure list

# Probar conexión
aws s3 ls s3://tu-bucket
```

### Error Docker Swarm:
```bash
# Verificar estado del cluster
docker node ls

# Reiniciar servicio
docker service update --force pokeneas-service
```

### Error de despliegue:
```bash
# Ver logs del servicio
docker service logs pokeneas-service

# Verificar imagen
docker pull tu-usuario/pokeneas-app:latest
```
