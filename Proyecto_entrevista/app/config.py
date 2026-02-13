"""
modulo de configuracion para la aplicación
utiliza Pydantic SEttings para cargar variables de entorno desde un archivo .env
y validar automaticamente los tipos de datos.

Esto permite:
-separar la configuración del codigo
proteger datos sensibles (como las claves JWT)
-facilitar cambios por entorno (dev, testing, producción)
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
"""
Se crea la clase que define todas las configuraciones del sistema,
Los valores se cargan des la variable de entorno
"""

class Settings(BaseSettings):
    # URL de conexión a la base de datos(obligatoria)
    database_url: str
    # Clave secreta para firmar y verificar tokens JWT (obligatoria)
    jwt_secret:str
    # Tiempo de expiración del token en minutos (Usualmente el valor se queda en 60 min[1hr])
    access_token_expire_minutes: int = 60
    # Tamaño máximo permitido para archivos De acuerdo a lo que comentaron (5 MB por defecto)
    max_file_size: int = 5 * 1024 * 1024
    # directorio donde se almacenarán los archivos subidos (por ejemplo CV_profesionarl.pdf)
    upload_dir:str = "uploads"
    # Configuración para cargar variables desde el archivo .env
    model_config = SettingsConfigDict(env_file=".env")

#   instancia global que podrá importarse en toda la aplicación
Settings = Settings()