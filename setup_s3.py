#!/usr/bin/env python3
"""
Script para configurar y subir imágenes al bucket S3 de Pokeneas
"""

import boto3
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def create_s3_bucket():
    """Crear bucket S3 para las imágenes de Pokeneas"""
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    
    bucket_name = os.getenv('S3_BUCKET')
    
    try:
        # Crear bucket
        if os.getenv('AWS_REGION') == 'us-east-1':
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': os.getenv('AWS_REGION')}
            )
        print(f"✅ Bucket '{bucket_name}' creado exitosamente")
        
        # Configurar política de acceso público
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }
        
        s3.put_bucket_policy(Bucket=bucket_name, Policy=str(bucket_policy).replace("'", '"'))
        print(f"✅ Política de acceso público configurada")
        
        # Desactivar bloqueo de acceso público
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )
        print(f"✅ Bloqueo de acceso público desactivado")
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print(f"ℹ️  El bucket '{bucket_name}' ya existe")
        else:
            print(f"❌ Error creando bucket: {e}")

def upload_sample_images():
    """Subir imágenes de ejemplo (necesitarás crear las imágenes reales)"""
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    
    bucket_name = os.getenv('S3_BUCKET')
    
    # Lista de imágenes que necesitas crear
    images = [
        'paisa.jpg',
        'antioqueño.jpg', 
        'medellin.jpg',
        'silletero.jpg',
        'arriero.jpg',
        'minero.jpg',
        'cafetero.jpg',
        'guadalupeño.jpg',
        'rionegrero.jpg',
        'santafereño.jpg'
    ]
    
    print("📝 Necesitas crear las siguientes imágenes:")
    for image in images:
        print(f"   - {image}")
    
    print("\n💡 Sugerencias para las imágenes:")
    print("   - Puedes usar imágenes de paisajes de Antioquia")
    print("   - O crear imágenes con herramientas como DALL-E, Midjourney, etc.")
    print("   - Tamaño recomendado: 400x400 píxeles")
    print("   - Formato: JPG o PNG")
    
    # Crear archivos de ejemplo (texto plano para testing)
    for image in images:
        try:
            # Crear un archivo de texto simple como placeholder
            content = f"Imagen placeholder para {image.split('.')[0]}"
            s3.put_object(
                Bucket=bucket_name,
                Key=image,
                Body=content.encode('utf-8'),
                ContentType='text/plain'
            )
            print(f"✅ Placeholder subido: {image}")
        except ClientError as e:
            print(f"❌ Error subiendo {image}: {e}")

def main():
    print("🏔️  Configuración de AWS S3 para Pokeneas de Antioquia")
    print("=" * 60)
    
    # Verificar variables de entorno
    required_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION', 'S3_BUCKET']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Variables de entorno faltantes:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Crea un archivo .env basado en env.example")
        return
    
    print("✅ Variables de entorno configuradas")
    
    # Crear bucket
    create_s3_bucket()
    
    # Subir imágenes de ejemplo
    upload_sample_images()
    
    print("\n🎉 Configuración completada!")
    print(f"🌐 URL del bucket: https://{os.getenv('S3_BUCKET')}.s3.amazonaws.com/")

if __name__ == "__main__":
    main()
