# 📝 Guía Paso a Paso - Configurar Docker Swarm en AWS

## ✅ Lo que ya tienes listo:
- ✅ 4 instancias EC2 corriendo
- ✅ Bucket S3 "pokeneasss" con imágenes
- ✅ Security Group básico configurado

## 🎯 Lo que vamos a hacer:
1. Agregar reglas de firewall para Docker Swarm
2. Conectarnos a la primera instancia
3. Instalar Docker (si no está)
4. Crear el cluster Docker Swarm
5. Unir las otras 3 instancias al cluster
6. Desplegar la aplicación

---

## PASO 1: Agregar reglas de firewall ⚙️

### ¿Por qué?
Docker Swarm necesita que las instancias se comuniquen entre sí en ciertos puertos.

### Qué hacer:
1. **Ve a la consola de AWS EC2**
2. En el menú izquierdo, haz clic en **"Security Groups"**
3. Busca y selecciona el security group **"launch-wizard-1"** (o el que tenga tu instancia)
4. Abre la pestaña **"Inbound rules"**
5. Haz clic en **"Edit inbound rules"**
6. Haz clic en **"Add rule"** (hazlo 4 veces para agregar 4 reglas nuevas)

   **Regla 1:**
   - Type: `Custom TCP`
   - Port range: `2377`
   - Source type: `Custom`
   - Source: **Copia el ID del Security Group** (está arriba, algo como `sg-0feecf938317b692a`)
   - Description: `Docker Swarm manager`

   **Regla 2:**
   - Type: `Custom TCP`
   - Port range: `7946`
   - Source type: `Custom`
   - Source: **El mismo Security Group ID**
   - Description: `Docker Swarm gossip TCP`

   **Regla 3:**
   - Type: `Custom UDP`
   - Port range: `7946`
   - Source 생성: `Custom`
   - Source: **El mismo Security Group ID**
   - Description: `Docker Swarm gossip UDP`

   **Regla 4:**
   - Type: `Custom UDP`
   - Port range: `4789`
   - Source type: `Custom`
   - Source: **El mismo Security Group ID**
   - Description: `Docker overlay network`

7. Haz clic en **"Save rules"**

✅ **Resultado esperado:** Ahora deberías tener 6 reglas en total (SSH, HTTP, y las 4 nuevas)

---

## PASO 2: Preparar conexión SSH 🔐

### En Windows:

1. **Abre PowerShell o CMD**
2. **Ve a la carpeta donde guardaste tu archivo .pem:**
   ```powershell
   cd C:\Users\USUARIO\Desktop
   ```
   (Ajusta la ruta según donde guardaste tu `pokeneas-key.pem`)

3. **Arregla los permisos del archivo** (solo una vez):
   ```powershell
   icacls "pokeneas-key.pem" /inheritance:r
   icacls "pokeneas-key.pem" /grant:r "%username%:R"
   ```

4. **Obtén la IP pública de tu primera instancia:**
   - Ve a EC2 → Instances
   - Mira la columna "Public IPv4 address" de tu primera instancia
   - Anota esa IP (ejemplo: `3.16.213.92`)

---

## PASO 3: Conectarse a la primera instancia (Líder) 🖥️

### En PowerShell/CMD:

```powershell
ssh -i pokeneas-key.pem ec2-user@TU-IP-AQUI
```

**Ejemplo:**
```powershell
ssh -i pokeneas-key.pem ec2-user@3.16.213.92
```

### ¿Qué puede pasar?

**Si funciona:** Verás algo como:
```
The authenticity of host '...' can't be established.
Are you sure you want to continue connecting (yes/no)?
```
Escribe: `yes` y presiona Enter

**Si da error de permisos:** Vuelve al Paso 2 y arregla los permisos

**Si da error de conexión:** 
- Verifica que la IP sea correcta
- Espera 2-3 minutos más (la instancia está inicializando)
- Verifica que el Security Group permita SSH (puerto 22)

### Una vez conectado:
Verás algo como:
```
[ec2-user@ip-xxx ~]$
```
¡Perfecto! Ya estás dentro de la instancia.

---

## PASO 4: Instalar Docker 🐳

### Verifica si Docker ya está instalado:
```bash
docker --version
```

### Si dice "command not found", instálalo:

```bash
# Actualizar el sistema
sudo dnf update -y

# Instalar Docker
sudo dnf install -y docker

# Iniciar Docker
sudo systemctl start docker

# Habilitar Docker para que inicie automáticamente
sudo systemctl enable docker

 côngsudo usermod -aG docker ec2-user
```

### Verificar instalación:
```bash
docker --version
```
Debería mostrar algo como: `Docker version 24.x.x`

### Si agregaste tu usuario al grupo docker:
**Cierra la conexión y vuelve a conectarte:**
```bash
exit
```
Luego reconecta:
```powershell
ssh -i pokeneas-key.pem ec2-user@TU-IP
```

---

## PASO 5: Inicializar Docker Swarm 👑

### En la primera instancia (la líder), ejecuta:

```bash
docker swarm init
```

### Resultado esperado:
Verás algo como:
```
Swarm initialized: current node (xxxxx) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-xxxxx 3.16.213.92:2377
```

✅ **¡Perfecto! El Swarm está creado**

### Obtén el token para managers:

```bash
docker swarm join-token manager
```

### Resultado esperado:
Verás algo como:
```
To add a manager to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-xxxxx-xxxxx 3.16.213.92:2377
```

**⚠️ IMPORTANTE:** Copia TODO ese comando completo, lo necesitarás para las otras 3 instancias.

### Verifica que eres el líder:

```bash
docker node ls
```

Deberías ver:
```
ID                            HOSTNAME   STATUS    AVAILABILITY   MANAGER STATUS
xxxxx *   ip-xxx   Ready     Active       Leader
```

✅ **Perfecto, eres el líder**

---

## PASO 6: Unir las otras 3 instancias 🔗

### Para cada una de las otras 3 instancias:

1. **Cierra la conexión actual:**
   ```bash
   exit
   ```

2. **Obtén la IP de la siguiente instancia** (ve a EC2 → Instances)

3. **Conéctate a esa instancia:**
   ```powershell
   ssh -i pokeneas-key.pem ec2-user@IP-DE-ESTA-INSTANCIA
   ```

4. **Instala Docker** (si no está):
   ```bash
   sudo dnf update -y
   sudo dnf install -y docker
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker ec2-user
   exit
   ```
   
   Reconecta:
   ```powershell
   ssh -i pokeneas-key.pem ec2-user@IP-DE-ESTA-INSTANCIA
   ```

5. **Ejecuta el comando de join** (el que copiaste del Paso 5):
   ```bash
   docker swarm join --token SWMTKN-1-xxxxx 3.16.213.92:2377
   ```

   ✅ **Resultado esperado:**
   ```
   This node joined a swarm as a manager.
   ```

6. **Repite los pasos 1-5 para las otras 2 instancias**

---

## PASO 7: Verificar el cluster ✅

### Conéctate de vuelta a la instancia líder:

```powershell
ssh -i pokeneas-key.pem ec2-user@IP-LIDER
```

### Verifica todos los nodos:

```bash
docker node ls
```

### Resultado esperado:
Deberías ver **4 nodos**, algo como:

```
ID                            HOSTNAME      STATUS    AVAILABILITY   MANAGER STATUS
xxxxx *   ip-xxx-1   Ready     Active       Leader
yyyyy     ip-xxx-2   Ready     Active       Reachable
zzzzz     ip-xxx-3   Ready     Active       Reachable
wwwww     ip-xxx-4   Ready     Active       Reachable
```

✅ **¡Perfecto! Tienes un cluster de 4 nodos funcionando**

---

## PASO 8: Preparar para desplegar 🚀

### Necesitas tener listo:

1. **Tu imagen en DockerHub** (ejemplo: `tu-usuario/pokeneas-app:latest`)
2. **Tus credenciales de AWS:**
   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_REGION (ejemplo: `us-east-2`)
   - S3_BUCKET: `pokeneasss`

### En la instancia líder, configura las variables:

```bash
export AWS_ACCESS_KEY_ID="tu_access_key_aqui"
export AWS_SECRET_ACCESS_KEY="tu_secret_key_aqui"
export AWS_REGION="us-east-2"
export S3_BUCKET="pokeneasss"
```

---

## PASO 9: Desplegar la aplicación 🎯

### En la instancia líder, ejecuta:

```bash
docker service create \
  --name pokeneas-service \
  --replicas 10 \
  --publish 80:80 \
  --env AWS_ACCESS_KEY_ID \
  --env AWS_SECRET_ACCESS_KEY \
  --env AWS_REGION \
  --env S3_BUCKET \
  TU-USUARIO-DOCKERHUB/pokeneas-app:latest
```

**⚠️ IMPORTANTE:** Cambia `TU-USUARIO-DOCKERHUB` por tu usuario real de DockerHub

### Verifica que el servicio está corriendo:

```bash
docker service ls
```

Deberías ver:
```
ID             NAME              MODE         REPLICAS   IMAGE
xxxxx          pokeneas-service  replicated   10/10      tu-usuario/pokeneas-app:latest
```

### Ver las réplicas en cada nodo:

```bash
docker service ps pokeneas-service
```

Deberías ver 10 réplicas distribuidas en las 4 instancias.

---

## PASO 10: Probar la aplicación 🌐

### Obtén la IP pública de la instancia líder:
- Ve a EC2 → Instances
- Mira la IP pública de la primera instancia

### Prueba en tu navegador:

- **Página principal:** `http://IP-PUBLICA-LIDER`
- **JSON Pokenea:** `http://IP-PUBLICA-LIDER/pokenea`
- **Imagen y frase:** `http://IP-PUBLICA-LIDER/imagen`

### Verifica que funciona:
- Recarga varias veces `/pokenea` y `/imagen`
- Deberías ver diferentes `container_id` en cada respuesta
- Esto confirma que el load balancing funciona entre las 10 réplicas

---

## 🆘 Troubleshooting

### Error: "Cannot connect to Docker daemon"
```bash
sudo systemctl start docker
sudo usermod -aG docker ec2-user
exit
# Reconecta
```

### Error: "connection refused" en swarm join
- Verifica que las reglas del Security Group estén correctas
- Verifica que uses la IP correcta del líder
- Verifica que el puerto 2377 esté abierto

### Error: "No such service" o "image not found"
- Verifica que la imagen existe en DockerHub
- Verifica que escribiste bien el nombre: `usuario/repo:tag`
- Prueba: `docker pull TU-USUARIO-DOCKERHUB/pokeneas-app:latest`

### Las réplicas no se crean (0/10)
- Verifica las variables de entorno
- Verifica los logs: `docker service logs pokeneas-service`
- Verifica que la imagen se pueda descargar

---

## ✅ Checklist Final

- [ ] 4 reglas de firewall agregadas al Security Group
- [ ] Docker instalado en las 4 instancias
- [ ] Docker Swarm inicializado en la primera instancia
- [ ] Las otras 3 instancias unidas al cluster
- [ ] `docker node ls` muestra 4 nodos
- [ ] Variables de entorno configuradas
- [ ] Servicio desplegado con 10 réplicas
- [ ] `docker service ps pokeneas-service` muestra 10 réplicas
- [ ] La aplicación funciona en el navegador
- [ ] Los container_id cambian al refrescar

---

## 📞 ¿Necesitas ayuda?

Si te atascas en algún paso, dime exactamente:
1. En qué paso estás
2. Qué comando ejecutaste
3. Qué error te salió (copia el mensaje completo)
