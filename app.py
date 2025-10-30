from flask import Flask, jsonify, render_template_string
import boto3
import os
import random
import socket
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración AWS S3
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)
S3_BUCKET = os.getenv('S3_BUCKET')

# Datos de Pokeneas (nacidos en Antioquia)
pokeneas = [
    {
        "id": 1,
        "nombre": "Paisa",
        "altura": 1.65,
        "habilidad": "Arriero",
        "imagen": "paisa.jpg",
        "frase": "El que madruga, Dios lo ayuda"
    },
    {
        "id": 2,
        "nombre": "Antioqueño",
        "altura": 1.70,
        "habilidad": "Minero",
        "imagen": "antioqueño.jpg",
        "frase": "Más vale pájaro en mano que cien volando"
    },
    {
        "id": 3,
        "nombre": "Medellín",
        "altura": 1.60,
        "habilidad": "Empresario",
        "imagen": "medellin.jpg",
        "frase": "La plata no da la felicidad, pero cómo ayuda"
    },
    {
        "id": 4,
        "nombre": "Silletero",
        "altura": 1.75,
        "habilidad": "Florista",
        "imagen": "silletero.jpg",
        "frase": "Las flores alegran el corazón"
    },
    {
        "id": 5,
        "nombre": "Arriero",
        "altura": 1.68,
        "habilidad": "Transportista",
        "imagen": "arriero.jpg",
        "frase": "Caminante no hay camino, se hace camino al andar"
    },
    {
        "id": 6,
        "nombre": "Minero",
        "altura": 1.62,
        "habilidad": "Excavador",
        "imagen": "minero.jpg",
        "frase": "El trabajo dignifica al hombre"
    },
    {
        "id": 7,
        "nombre": "Cafetero",
        "altura": 1.72,
        "habilidad": "Agricultor",
        "imagen": "cafetero.jpg",
        "frase": "El café es la bebida de los dioses"
    },
    {
        "id": 8,
        "nombre": "Guadalupeño",
        "altura": 1.66,
        "habilidad": "Peregrino",
        "imagen": "guadalupeño.jpg",
        "frase": "La fe mueve montañas"
    },
    {
        "id": 9,
        "nombre": "Rionegrero",
        "altura": 1.69,
        "habilidad": "Ceramista",
        "imagen": "rionegrero.jpg",
        "frase": "Del barro nacen las obras de arte"
    },
    {
        "id": 10,
        "nombre": "Santafereño",
        "altura": 1.71,
        "habilidad": "Historiador",
        "imagen": "santafereño.jpg",
        "frase": "La historia se repite"
    }
]

def get_container_id():
    """Obtiene el ID del contenedor desde el cual se ejecuta la aplicación"""
    try:
        with open('/proc/self/cgroup', 'r') as f:
            for line in f:
                if 'docker' in line:
                    return line.split('/')[-1].strip()[:12]
    except:
        pass
    
    # Si no se puede obtener el ID del contenedor, usar hostname
    return socket.gethostname()

@app.route('/pokenea')
def get_pokenea():
    """Ruta que devuelve información básica de un Pokenea aleatorio en formato JSON"""
    pokenea = random.choice(pokeneas)
    container_id = get_container_id()
    
    response = {
        "id": pokenea["id"],
        "nombre": pokenea["nombre"],
        "altura": pokenea["altura"],
        "habilidad": pokenea["habilidad"],
        "container_id": container_id
    }
    
    return jsonify(response)

@app.route('/imagen')
def mostrar_imagen():
    """Ruta que muestra la imagen y frase filosófica de un Pokenea aleatorio"""
    pokenea = random.choice(pokeneas)
    container_id = get_container_id()
    
    # Construir URL de la imagen en S3
    image_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{pokenea['imagen']}"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pokenea - {pokenea['nombre']}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f0f0f0;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            img {{
                max-width: 400px;
                height: auto;
                border-radius: 10px;
                margin: 20px 0;
            }}
            .frase {{
                font-style: italic;
                font-size: 18px;
                color: #333;
                margin: 20px 0;
                padding: 15px;
                background-color: #f9f9f9;
                border-left: 4px solid #007bff;
            }}
            .container-id {{
                font-size: 12px;
                color: #666;
                margin-top: 20px;
            }}
            h1 {{
                color: #007bff;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Pokenea: {pokenea['nombre']}</h1>
            <img src="{image_url}" alt="{pokenea['nombre']}">
            <div class="frase">
                "{pokenea['frase']}"
            </div>
            <div class="container-id">
                Container ID: {container_id}
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

@app.route('/')
def index():
    """Página principal con información del proyecto"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pokeneas de Antioquia</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f0f0f0;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .route {
                margin: 20px 0;
                padding: 15px;
                background-color: #f9f9f9;
                border-radius: 5px;
            }
            a {
                color: #007bff;
                text-decoration: none;
                font-weight: bold;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏔️ Pokeneas de Antioquia 🏔️</h1>
            <p>Bienvenido al sistema de Pokeneas nacidos en Antioquia</p>
            
            <div class="route">
                <h3>📊 Información JSON</h3>
                <p>Obtén información básica de un Pokenea aleatorio</p>
                <a href="/pokenea">Ver Pokenea (JSON)</a>
            </div>
            
            <div class="route">
                <h3>🖼️ Imagen y Frase</h3>
                <p>Ve la imagen y frase filosófica de un Pokenea aleatorio</p>
                <a href="/imagen">Ver Imagen y Frase</a>
            </div>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
