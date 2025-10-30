# 🚀 Solución Rápida - Comandos para hacer funcionar el servicio

## ⚠️ Problema Actual:
La imagen `pokeneas-app:latest` no se encuentra cuando Docker Swarm intenta crear las réplicas.

## ✅ Solución Simple - Paso a Paso:

### En tu instancia EC2 (la líder):

```bash
# 1. Ir al directorio del código
cd ~/Talle2_Software

# 2. Construir la imagen
docker build -t pokeneas-app:latest .

# 3. Verificar que se constru历ó
docker images | grep pokeneas

# 4. Configurar variables de entorno
export AWS_ACCESS_KEY_ID="tu_access_key_aqui"
export AWS_SECRET_ACCESS_KEY="tu_secret_key_aqui"
export AWS_REGION="us-east-2"  # Ajusta según tu región
export S3_BUCKET="nombre_de_tu_bucket"

# 5. Inicializar Swarm (si no está activo)
docker swarm init

# 6. Eliminar servicio anterior si existe
docker service rm pokeneas-service 2>/dev/null || true

# 7. Crear el servicio (10 réplicas en la misma instancia)
docker service create \
  --name pokeneas-service \
  --replicas 10 \
  --publish 80:80 \
  --env AWS_ACCESS_KEY_ID \
  --env AWS_SECRET_ACCESS_KEY \
  --env AWS_REGION \
  --env S3_BUCKET \
  pokeneas-app:latest

# 8. Verificar que funciona
docker service ls
docker service ps pokeneas-service
```

### Si quieres distribuir en múltiples instancias:

Necesitas construir la imagen en cada instancia O usar DockerHub.

### Opción con DockerHub (Recomendado):

1. Sube la imagen a DockerHub
2. Todos los nodos pueden descargarla automáticamente

## 🔍 Verificar que funciona:

```bash
# Ver las réplicas
docker service ps pokeneas-service

# Ver logs
docker service logs pokeneas-service

# Probar la app (usa la IP pública de tu instancia)
curl http://localhost/pokenea
```
