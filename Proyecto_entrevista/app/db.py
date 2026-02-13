"""
Modulo de conexión a la base de datos.

Que hace el codigo(configura):
-El motor de conexión (engine)
-La fabrica de sesiones (sessionLocal)
La clase base para los modelos (Base)
- La dependencia para usar la DB en endpoints de FastAPI

Este archivo se encarga de:
Conectar con MySQL 
Crear sesiones Por request
Definir la base para los modelos ORM(Object-Relational Mapping o Mapeo Objeto-Relacional)
ORM: Tecnica de programación que perimte conectar DB de datos relacionales con lenguajes de programación estilo POO
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import Settings

#Se crea el sistema de Conexión

# Engine es el punto principal de conexión a la base de datos
# Utiliza la URL definida en la configuración(.env)
# pool_pre_ping=True verifica que la conexión siga activa
# antes de usarla (evita errores por desconexión)
#Traduce los comandos de Python a SQL
engine = create_engine(
    Settings.database_url,
    pool_pre_ping=True
)
#Se crea la fabrica de sesiones
sessionLocal = sessionmaker(
    autocommit=False,   #No guarda cambios automáticamente
    autoflush=False,    #No envía cambios hasta que se indique
    bind=engine         #Enlaza la sesión con el engine
    )        

#Base para los modelos

#Base será la clase padre de todos los modelos ORM.
#Ejemplo:
#class User(Base):
#    __tablename__ = "users"
Base = declarative_base()


#dependencia para endpoints(FastAPI)
def get_db():
        """
    Dependencia que proporciona una sesión de base de datos
    a los endpoints de FastAPI.

    - Crea una nueva sesión
    - La entrega al endpoint
    - La cierra automáticamente al finalizar
    """
        db = sessionLocal()
        try:
            yield db
        finally:
            db.close()