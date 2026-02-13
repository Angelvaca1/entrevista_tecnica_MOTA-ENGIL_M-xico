holaaaaa. hago este README con ayuda de gemini para explicar el funcionamiento, las tecnologias ocupadas y el caso de instalación


📦 Tecnologías utilizadas

🐍 Python 3.11

⚡ FastAPI

🗄️ MySQL 8

🐳 Docker & Docker Compose

🧱 SQLAlchemy

🔐 JWT Authentication

📁 Sistema de carga de archivos (uploads)

📋 Requisitos previos

Antes de empezar, asegúrate de tener instalado:

Docker Desktop (incluye Docker Compose)

Git (para clonar el repositorio)

📁 Estructura del Proyecto
Proyecto_entrevista/
│
├── app/
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   ├── auth.py
│   ├── db.py
│   ├── config.py
│   └── main.py
│
├── uploads/
├── requirements.txt
├── .env
├── schema.sql
├── Dockerfile
├── docker-compose.yml
└── README.md

⚙️ Instalación y Despliegue

1️⃣ Clonar el repositorio

git clone https://github.com/Angelvaca1/entrevista_tecnica_MOTA-ENGIL_M-xico.git
cd entrevista_tecnica_MOTA-ENGIL_M-xico

2️⃣ Configurar variables de entorno

Crea un archivo .env en la raíz del proyecto y añade tus credenciales:

DATABASE_URL=mysql+pymysql://root:ClaveDeLaDB@db/backend_db
JWT_SECRET=ClaveSecretaParaFirmarTusTokens
ACCESS_TOKEN_EXPIRE_MINUTES=60
MAX_FILE_SIZE=5242880
UPLOAD_DIR=uploads

💡 Notas importantes:

JWT_SECRET → Genera tu propia clave secreta, no la compartas públicamente.

DATABASE_URL → El host es db, no localhost, porque db es el servicio de Docker.

🗄️ Configuración de Base de Datos en Docker

En docker-compose.yml:

services:
  db:
    image: mysql:8
    container_name: mysql_db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ClaveDeLaDB
      MYSQL_DATABASE: backend_db
    ports:
      - "3307:3306"
    volumes:
      - db_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-pClaveDeLaDB"]
      interval: 5s
      timeout: 5s
      retries: 5

💡 Explicación:

image → Imagen oficial de MySQL 8.

volumes → Mantiene los datos aunque el contenedor se reinicie.

healthcheck → Permite que el backend espere a que la DB esté lista antes de iniciar.

🚀 Cómo Ejecutar el Proyecto

Desde la raíz del proyecto:

docker compose up --build

Luego, abre la documentación automática de FastAPI en tu navegador:

http://localhost:8000/docs
🔄 Reiniciar desde cero (cuando hay errores de credenciales)
docker compose down -v
docker compose up --build

⚠ -v elimina el volumen y reinicia la base desde cero.

🧠 Cómo Funciona la Comunicación

Docker crea una red interna automática.
El backend se conecta a la base usando:

mysql+pymysql://root:ClaveDeLaDB@db/backend_db

root → Usuario

ClaveDeLaDB → Contraseña

db → Servicio MySQL en Docker

backend_db → Base de datos

📦 Dependencias principales

En requirements.txt:

fastapi
uvicorn
sqlalchemy
pymysql
cryptography
email-validator
python-dotenv
🏗 Flujo de Arranque

Docker levanta MySQL.

MySQL ejecuta healthcheck.

Backend espera a que la DB esté lista.

FastAPI inicia.

SQLAlchemy crea tablas automáticamente.

Swagger queda disponible en /docs.

🛠 Comandos Útiles

Ver contenedores activos: docker ps

Ver logs en tiempo real: docker compose logs -f

Detener contenedores: docker compose down

Eliminar base de datos: docker compose down -v
segun yo ya con estas especificaciones queda entendido el todo jsjsjsj
igual cualquier duda me lo pueden comentar y estoy al pendiente 









