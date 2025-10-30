# Guía Paso a Paso - Taller 2 Pokeneas de Antioquia

## 📋 Checklist de Tareas

### ✅ Fase 1: Desarrollo Local (COMPLETADO)
- [x] Crear aplicación Flask con Pokeneas
- [x] Implementar rutas `/pokenea` y `/imagen`
- [x] Configurar boto3 para AWS S3
- [x] Crear Dockerfile y docker-compose
- [x] Crear estructura de proyecto

### 🔄 Fase 2: AWS S3 (PENDIENTE)
- [ ] Crear cuenta AWS (si no tienes)
- [ ] Crear bucket S3
- [ ] Configurar acceso público del bucket
- [ ] Crear credenciales IAM
- [ ] Subir imágenes de Pokeneas
- [ ] Probar conexión con boto3

### 🔄 Fase 3: GitHub y DockerHub (PENDIENTE)
- [ ] Crear repositorio en GitHub
- [ ] Subir código al repositorio
- [ ] Crear cuenta en DockerHub
- [ ] Configurar GitHub Actions
- [ ] Probar build automático

### 🔄 Fase 4: AWS EC2 y Docker Swarm (PENDIENTE)
- [ ] Crear 4 instancias EC2
- [ ] Instalar Docker en las instancias
- [ ] Configurar Docker Swarm
- [ ] Desplegar servicio con 10 réplicas
- [ ] Verificar funcionamiento

## 🚀 Instrucciones Detalladas

### 1. Configurar AWS S3

#### Crear Bucket S3:
1. Ve a [AWS S3 Console](https://console.aws.amazon.com/s3/)
2. Click "Create bucket"
3. Nombre único (ej: `pokeneas-antioquia-2024`)
4. Región: `us-east-1` (o la que prefieras)
5. Click "Create bucket"

#### Configurar Acceso Público:
1. Selecciona tu bucket
2. Ve a "Permissions" tab
3. Scroll down a "Block public access"
4. Click "Edit"
5. **DESACTIVA** todas las opciones:
   - ☐ Block all public access
   - ☐ Block public access to buckets and objects granted through new access control lists (ACLs)
   - ☐ Block public access to buckets and objects granted through any access control lists (ACLs)
   - ☐ Block public access to buckets and objects granted through new public bucket or access point policies
   - ☐ Block public access to buckets and objects granted through any public bucket or access point policies
6. Click "Save changes"
7. Escribe "confirm" y click "Confirm"

#### Crear Credenciales IAM:
1. Ve a [AWS IAM Console](https://console.aws.amazon.com/iam/)
2. Click "Users" → "Create user"
3. Nombre: `pokeneas-user`
4. Click "Next"
5. Attach policies: `AmazonS3FullAccess`
6. Click "Next" → "Create user"
7. Click en el usuario creado
8. Tab "Security credentials"
9. Click "Create access key"
10. Tipo: "Application running outside AWS"
11. **GUARDA** las credenciales (no se pueden ver después)

#### Subir Imágenes:
1. Ve a tu bucket S3
2. Click "Upload"
3. Sube las imágenes de los Pokeneas:
   - `paisa.jpg`
   - `antioqueño.jpg`
   - `medellin.jpg`
   - `silletero.jpg`
   - `arriero.jpg`
   - `minero.jpg`
   - `cafetero.jpg`
   - `guadalupeño.jpg`
   - `rionegrero.jpg`
   - `santafereño.jpg`

### 2. Configurar Variables de Entorno

Crea archivo `.env`:
```bash
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
S3_BUCKET=tu-bucket-name
```

### 3. Probar Localmente

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py

# Probar rutas:
# http://localhost:80/
# http://localhost:80/pokenea
# http://localhost:80/imagen
```

### 4. GitHub y DockerHub

#### GitHub:
1. Crear repositorio: `pokeneas-antioquia`
2. Subir código:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/tu-usuario/pokeneas-antioquia.git
git push -u origin main
```

#### DockerHub:
1. Crear cuenta en [DockerHub](https://hub.docker.com/)
2. Crear repositorio: `pokeneas-app`
3. Configurar GitHub Actions:
   - Ve a Settings → Secrets and variables → Actions
   - Agregar secrets:
     - `DOCKERHUB_USERNAME`: tu usuario DockerHub
     - `DOCKERHUB_TOKEN`: tu token DockerHub

### 5. AWS EC2 y Docker Swarm

#### Crear Instancias EC2:
1. Ve a [AWS EC2 Console](https://console.aws.amazon.com/ec2/)
2. Launch Instance (4 veces)
3. AMI: Ubuntu Server 22.04 LTS
4. Instance type: t2.micro (free tier)
5. Security Group: HTTP (80), SSH (22)
6. User Data (para instalar Docker):
```bash
#!/bin/bash
apt-get update
apt-get install -y docker.io
systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu
```

#### Configurar Docker Swarm:

**En la instancia líder:**
```bash
# Inicializar swarm
docker swarm init

# Obtener token para managers
docker swarm join-token manager
```

**En las otras 3 instancias:**
```bash
# Unirse como manager
docker swarm join --token <token> <ip-lider>:2377
```

#### Desplegar Servicio:
```bash
# En la instancia líder
export AWS_ACCESS_KEY_ID="tu-key"
export AWS_SECRET_ACCESS_KEY="tu-secret"
export AWS_REGION="us-east-1"
export S3_BUCKET="tu-bucket"

# Ejecutar script de despliegue
./deploy.sh tu-usuario-dockerhub
```

### 6. Verificación

#### Verificar Servicio:
```bash
# Ver estado de las réplicas
docker service ps pokeneas-service

# Ver logs
docker service logs pokeneas-service

# Verificar que hay 10 réplicas corriendo
docker service ls
```

#### Probar Aplicación:
- `http://<ip-instancia>:80/` - Página principal
- `http://<ip-instancia>:80/pokenea` - JSON aleatorio
- `http://<ip-instancia>:80/imagen` - Imagen y frase

#### Verificar Container IDs:
- Hacer múltiples requests a `/pokenea` y `/imagen`
- Verificar que los `container_id` cambian
- Esto confirma que el load balancing funciona

## 📸 Pantallazos Requeridos

1. **Consola Docker Swarm**: Mostrando las 10 réplicas corriendo
2. **AWS S3**: Lista de imágenes en el bucket
3. **Aplicación**: 2 pantallazos de `/imagen` con diferentes container IDs

## 🔗 Información Final

- **IP para docente**: `<ip-instancia-lider>`
- **Repositorio GitHub**: `https://github.com/tu-usuario/pokeneas-antioquia`

## 🆘 Troubleshooting

### Error de conexión S3:
- Verificar credenciales AWS
- Verificar región del bucket
- Verificar permisos IAM

### Error Docker Swarm:
- Verificar que todas las instancias están conectadas
- Verificar security groups (puerto 2377)
- Verificar que Docker está corriendo

### Error de despliegue:
- Verificar que la imagen existe en DockerHub
- Verificar variables de entorno
- Verificar logs del servicio: `docker service logs pokeneas-service`
