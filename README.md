# Pokeneas de Antioquia 🏔️

Sistema web desarrollado en Flask que muestra información sobre Pokeneas (nacidos en Antioquia) con imágenes almacenadas en AWS S3.

## Características

- **Ruta `/pokenea`**: Devuelve información básica de un Pokenea aleatorio en formato JSON
- **Ruta `/imagen`**: Muestra la imagen y frase filosófica de un Pokenea aleatorio
- **Ruta `/`**: Página principal con navegación
- **Docker Swarm**: Despliegue con múltiples réplicas en AWS

## Pokeneas Incluidos

1. **Paisa** - Arriero: "El que madruga, Dios lo ayuda"
2. **Antioqueño** - Minero: "Más vale pájaro en mano que cien volando"
3. **Medellín** - Empresario: "La plata no da la felicidad, pero cómo ayuda"
4. **Silletero** - Florista: "Las flores alegran el corazón"
5. **Arriero** - Transportista: "Caminante no hay camino, se hace camino al andar"
6. **Minero** - Excavador: "El trabajo dignifica al hombre"
7. **Cafetero** - Agricultor: "El café es la bebida de los dioses"
8. **Guadalupeño** - Peregrino: "La fe mueve montañas"
9. **Rionegrero** - Ceramista: "Del barro nacen las obras de arte"
10. **Santafereño** - Historiador: "La historia se repite"

## Configuración AWS

### 1. Crear Bucket S3

1. Ve a la consola de AWS S3
2. Crea un nuevo bucket con nombre único
3. Configura el bucket para acceso público:
   - Ve a "Configuración de bloqueo de acceso público"
   - Desactiva el bloqueo a todo acceso público
4. Sube las imágenes de los Pokeneas al bucket

### 2. Configurar Credenciales IAM

1. Ve a [AWS IAM Console](https://console.aws.amazon.com/iam)
2. Users → Security Credentials → Create Access Key
3. Guarda las credenciales (no se pueden ver después)

### 3. Variables de Entorno

Crea un archivo `.env` basado en `env.example`:

```bash
AWS_ACCESS_KEY_ID=tu_access_key_aqui
AWS_SECRET_ACCESS_KEY=tu_secret_key_aqui
AWS_REGION=us-east-1
S3_BUCKET=nombre_de_tu_bucket
```

## Desarrollo Local

### Instalación

```bash
# Clonar repositorio
git clone <tu-repositorio>
cd pokeneas-antioquia

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp env.example .env
# Editar .env con tus credenciales

# Ejecutar aplicación
python app.py
```

### Con Docker

```bash
# Construir imagen
docker build -t pokeneas-app .

# Ejecutar contenedor
docker run -p 80:80 --env-file .env pokeneas-app
```

## Despliegue en AWS con Docker Swarm

### 1. Crear Instancias EC2

Crear 4 instancias EC2 con Docker instalado usando el template del tutorial.

### 2. Configurar Docker Swarm

```bash
# En la instancia líder
docker swarm init

# En las otras 3 instancias (como managers)
docker swarm join --token <token> <ip-lider>:2377
```

### 3. Desplegar Servicio

```bash
# Crear servicio con 10 réplicas
docker service create \
  --name pokeneas-service \
  --replicas 10 \
  --publish 80:80 \
  --env AWS_ACCESS_KEY_ID=<tu_key> \
  --env AWS_SECRET_ACCESS_KEY=<tu_secret> \
  --env AWS_REGION=us-east-1 \
  --env S3_BUCKET=<tu_bucket> \
  <tu-usuario>/pokeneas-app:latest
```

## Estructura del Proyecto

```
pokeneas-antioquia/
├── app.py                 # Aplicación Flask principal
├── requirements.txt       # Dependencias Python
├── Dockerfile            # Imagen Docker
├── docker-compose.yml    # Compose para desarrollo
├── env.example          # Ejemplo de variables de entorno
└── README.md            # Este archivo
```

## Rutas de la API

- `GET /` - Página principal
- `GET /pokenea` - Información JSON de Pokenea aleatorio
- `GET /imagen` - Imagen y frase de Pokenea aleatorio

## Tecnologías Utilizadas

- **Flask**: Framework web Python
- **AWS S3**: Almacenamiento de imágenes
- **boto3**: SDK de AWS para Python
- **Docker**: Containerización
- **Docker Swarm**: Orquestación de contenedores
- **AWS EC2**: Servidores en la nube

## Autor

Desarrollado como parte del Taller 2 de AWS - Universidad Nacional de Colombia
