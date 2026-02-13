from pydantic import BaseModel, EmailStr
from datetime import datetime
"""
este archivo es de schemas (Pydantic)

"""

#Users
class UserCreate(BaseModel):
    """
    Esquema para crear un usuario.
    Se utiliza cuando el cliente envia datos para registrarse.
    """
    nombre: str
    correo: EmailStr  #Valida automaticamente que sea un email valido
    telefono: str
    password: str   #Contraseña en texto plano ( se haseha antes de guardar)

class UserOut(BaseModel):
    """
    Esquema para devolver información del usuario.
    No incluye datos sensibles como el password_hash.
    """
    id: int
    nombre: str
    correo: EmailStr
    telefono: str

    class Config:
        #Permite convertir automaticamente objetos orm (SQLAlchemy) a JSON
        #Actualización antes tenía esto: orm_mode = True pero me lanzaba varios warning en el docker entonces lo cambie
        from_attributes = True

#AUTH
class Token(BaseModel):
    """
    Esquema que representa el token JWT que se devuelve al hacer login.

    """
    access_token: str
    token_type: str = "bearer" #Estandar para autenticación JWT

#DOCUMENTS
class DocumentOut(BaseModel):
    """
    Esquema para deolver información de documentos.
    """
    id: int
    tipo_documento: str
    original_filename: str
    mime_type: str
    size: int
    created_at: datetime

    class Config:
        #Permite trabajar con modelos ORM directamente
        from_attributes = True


#especificación para el login
#Actualización antes tenía esto: orm_mode = True pero me lanzaba varios warning en el docker entonces lo cambie
class LoginRequest(BaseModel):
    correo: str
    password: str
