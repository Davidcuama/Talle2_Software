#!/usr/bin/env python3
"""
Script de prueba para verificar que la aplicación Flask funciona correctamente
"""

import requests
import json
import time
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_local_app():
    """Probar la aplicación Flask localmente"""
    base_url = "http://localhost:80"
    
    print("🧪 Probando aplicación Pokeneas localmente...")
    print("=" * 50)
    
    # Verificar que la aplicación esté corriendo
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Aplicación Flask está corriendo")
        else:
            print(f"❌ Error: Status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar a la aplicación")
        print("💡 Asegúrate de que la aplicación esté corriendo: python app.py")
        return False
    
    # Probar ruta principal
    print("\n🏠 Probando ruta principal...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Ruta principal funciona")
        else:
            print(f"❌ Error en ruta principal: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Probar ruta /pokenea
    print("\n📊 Probando ruta /pokenea...")
    container_ids = set()
    
    for i in range(5):
        try:
            response = requests.get(f"{base_url}/pokenea")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Request {i+1}: {data['nombre']} (ID: {data['container_id']})")
                container_ids.add(data['container_id'])
            else:
                print(f"❌ Error en request {i+1}: {response.status_code}")
        except Exception as e:
            print(f"❌ Error en request {i+1}: {e}")
        time.sleep(1)
    
    print(f"\n📈 Container IDs únicos encontrados: {len(container_ids)}")
    if len(container_ids) > 1:
        print("✅ Load balancing funcionando correctamente")
    else:
        print("⚠️  Solo se encontró un container ID (normal en desarrollo local)")
    
    # Probar ruta /imagen
    print("\n🖼️  Probando ruta /imagen...")
    try:
        response = requests.get(f"{base_url}/imagen")
        if response.status_code == 200:
            print("✅ Ruta /imagen funciona")
            # Verificar que contiene elementos esperados
            content = response.text
            if "Pokenea:" in content and "Container ID:" in content:
                print("✅ Contenido de imagen correcto")
            else:
                print("⚠️  Contenido de imagen podría estar incompleto")
        else:
            print(f"❌ Error en ruta /imagen: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎉 Pruebas completadas!")
    return True

def test_aws_connection():
    """Probar conexión con AWS S3"""
    print("\n☁️  Probando conexión con AWS S3...")
    print("=" * 50)
    
    # Verificar variables de entorno
    required_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION', 'S3_BUCKET']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Variables de entorno faltantes:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Crea un archivo .env basado en env.example")
        return False
    
    print("✅ Variables de entorno configuradas")
    
    # Probar conexión S3
    try:
        import boto3
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        
        bucket_name = os.getenv('S3_BUCKET')
        
        # Listar objetos en el bucket
        response = s3.list_objects_v2(Bucket=bucket_name)
        objects = response.get('Contents', [])
        
        print(f"✅ Conexión S3 exitosa")
        print(f"📦 Bucket: {bucket_name}")
        print(f"📁 Objetos encontrados: {len(objects)}")
        
        if objects:
            print("📋 Archivos en el bucket:")
            for obj in objects[:5]:  # Mostrar solo los primeros 5
                print(f"   - {obj['Key']}")
            if len(objects) > 5:
                print(f"   ... y {len(objects) - 5} más")
        else:
            print("⚠️  No se encontraron objetos en el bucket")
            print("💡 Sube las imágenes de Pokeneas al bucket S3")
        
    except Exception as e:
        print(f"❌ Error conectando con S3: {e}")
        return False
    
    return True

def main():
    print("🏔️  Pruebas del Sistema Pokeneas de Antioquia")
    print("=" * 60)
    
    # Probar aplicación local
    app_ok = test_local_app()
    
    # Probar conexión AWS
    aws_ok = test_aws_connection()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"   Aplicación Flask: {'✅ OK' if app_ok else '❌ ERROR'}")
    print(f"   Conexión AWS S3: {'✅ OK' if aws_ok else '❌ ERROR'}")
    
    if app_ok and aws_ok:
        print("\n🎉 ¡Todo está funcionando correctamente!")
        print("🚀 Listo para desplegar en AWS con Docker Swarm")
    else:
        print("\n⚠️  Hay problemas que resolver antes del despliegue")
        print("📖 Revisa la GUIA_TALLER.md para más detalles")

if __name__ == "__main__":
    main()
