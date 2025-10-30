# 🔑 Cómo Obtener las Credenciales de AWS

## 📋 Checklist de Credenciales Necesarias

- [ ] AWS_ACCESS_KEY_ID
- [ ] AWS_SECRET_ACCESS_KEY  
- [ ] AWS_REGION
- [ ] S3_BUCKET

---

## 1️⃣ AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY

### Paso a paso para crearlas:

1. **Ve a la Consola de AWS:**
   - Entra a: https://console.aws.amazon.com/iam/
   - O desde la consola principal: Services → IAM

2. **Ve a la sección de Usuarios:**
   - En el menú izquierdo, haz clic en **"Users"** (Usuarios)
   - Si ya tienes un usuario, selecciónalo
   - Si no tienes uno, crea uno nuevo:
     - Click en **"Create user"**
     - Nombre: `pokeneas-user` (o el que prefieras)
     - Click **"Next"**

3. **Asignar permisos:**
   - Selecciona **"Attach policies directly"**
   - Busca y marca: **"AmazonS3FullAccess"** (para acceder al bucket)
   - También puedes agregar: **"AmazonEC2ReadOnlyAccess"** (opcional)
   - Click **"Next"** → **"Create user"**

4. **Crear las credenciales:**
   - Haz clic en el usuario que acabas de crear
   - Ve a la pestaña **"Security credentials"** (Credenciales de seguridad)
   - Scroll down hasta **"Access keys"**
   - Haz clic en **"Create access key"**

5. **Configurar el tipo de clave:**
   - Selecciona: **"Application running outside AWS"**
   - Description: `Para Pokeneas proyecto` (opcional)
   - Click **"Next"** → **"Create access key"**

6. **⚠️ IMPORTANTE - Guardar las credenciales:**
   - Te mostrará dos valores:
     - **Access key ID** (algo como: `AKIAIOSFODNN7EXAMPLE`)
     - **Secret access key** (algo como: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`)
   
   **⚠️ GUARDA ESTOS VALORES AHORA MISMO**
   - Descarga el archivo CSV o cópialos en un lugar seguro
   - **NO podrás ver el Secret access key después** de cerrar esta ventana
   - No compartas estas credenciales con nadie

---

## 2️⃣ AWS_REGION

### Cómo saber qué región usar:

1. **Ve a EC2 Console:**
   - https://console.aws.amazon.com/ec2/
   - O Services → EC2

2. **Mira tus instancias:**
   - En la lista de instancias, mira la columna **"Availability Zone"**
   - Ejemplo: Si dice `us-east-2c`, entonces tu región es: **`us-east-2`**

### Regiones comunes:
- `us-east-1` - N. Virginia
- `us-east-2` - Ohio
- `us-west-1` - California
- `us-west-2` - Oregon
- `eu-west-1` - Ireland
- `sa-east-1` - São Paulo

### También puedes verlo aquí:
- Arriba a la derecha en la consola de AWS verás el nombre de la región
- Ejemplo: "N. Virginia" = `us-east-1`

---

## 3️⃣ S3_BUCKET

### Nombre de tu bucket:
Ya lo sabes: **`pokeneasss`**

### Para verificar:
1. Ve a S3 Console: https://console.aws.amazon.com/s3/
2. Verás tu bucket listado ahí
3. El nombre exacto es el que debes usar

---

## ✅ Ejemplo Completo

Una vez que tengas todo, tus variables quedarán algo así:

```bash
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
export AWS_REGION="us-east-2"
export S3_BUCKET="pokeneasss"
```

---

## 🔒 Seguridad - Buenas Prácticas

1. **Nunca subas estas credenciales a GitHub**
   - Ya están en `.gitignore` para que no se suban por error
   - Usa `env.example` como template, no `.env`

2. **Rota las credenciales periódicamente**
   - Si crees que se comprometieron, elimínalas y crea nuevas

3. **Usa políticas específicas**
   - En lugar de `AmazonS3FullAccess`, puedes crear políticas más restrictivas
   - Solo para el bucket que necesitas

4. **En producción:**
   - Usa IAM Roles en lugar de Access Keys cuando sea posible
   - Las Access Keys son para desarrollo

---

## 🆘 Troubleshooting

### Error: "Invalid credentials"
- Verifica que copiaste bien las credenciales (sin espacios extra)
- Asegúrate de que el usuario tiene permisos para S3

### Error: "Access Denied" al acceder a S3
- Verifica que el usuario tiene `AmazonS3FullAccess` o permisos sobre el bucket específico
- Verifica que el nombre del bucket es correcto

### Error: "Region mismatch"
- Ver PK que el bucket y las instancias estén en la misma región
'></parameter>
</invoke>
