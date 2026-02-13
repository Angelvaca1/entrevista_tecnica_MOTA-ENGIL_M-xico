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
Docker Desktop (incluye Docker Compose).
Git (para clonar el repositorio).

Estructura del Proyecto

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

Sigue estos pasos para levantar el proyecto desde cero:

1. Clonar el repositorio
Bash
git clone https://github.com/Angelvaca1/entrevista_tecnica_MOTA-ENGIL_M-xico.git
cd tu-proyecto

3. Configurar variables de entorno
Crea un archivo llamado .env en la raíz del proyecto y añade tus credenciales (agregaré el archivo env desde el correo)

ejemplo:
DATABASE_URL=mysql+pymysql://root:ClaveDeLaDB@db/backend_db

JWT_SECRET=Clave secreta para firmar tus tokens JWT. La puedes generar tú mismo; no debe compartirse públicamente.

ACCESS_TOKEN_EXPIRE_MINUTES=60

MAX_FILE_SIZE=5242880

UPLOAD_DIR=uploads

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

volumes → Persistencia de datos.

healthcheck → Permite que el backend espere a que la DB esté lista antes de iniciar.

Nota: El host en DATABASE_URL es db, porque ese es el nombre del servicio en Docker, no localhost.



Cómo Ejecutar el Proyecto

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

Demostrar:

Configuración profesional de backend

Uso correcto de Docker

Conexión segura a base de datos

Manejo de variables de entorno

Estructura limpia de proyecto

Buenas prácticas para entrevistas técnicas


segun yo ya con estas especificaciones queda entendido el todo jsjsjsj
igual cualquier duda me lo pueden comentar y estoy al pendiente 









