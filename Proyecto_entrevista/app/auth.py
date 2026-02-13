from datetime import datetime, timedelta
from jose import jwt, JWSError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.config import Settings
from app import models
from app.db import get_db


# CONFIGURACIÓN DE HASH

# Contexto para hashear contraseñas usando bcrypt
#usa pbkdf2_sha256 como algoritmo de hash seguro
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto") #manejamos las versiones antiguas automaticamente 

# Esquema de seguridad que espera:
# Authorization: Bearer <token>
#esto obliga a que los endpoints(apis) protegidas reciban un token jwt valido
security = HTTPBearer()

# Algoritmo usado para firmar el JWT
ALGORITHM = "HS256"


# HASH Y VERIFICACIÓN
def hash_password(password: str) -> str:
    """
    Convierte una contraseña en texto plano
    en un hash seguro usando bcrypt.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compara una contraseña en texto plano
    con su versión hasheada en la base de datos.
    """
    return pwd_context.verify(plain_password, hashed_password)

# CREACIÓN DE TOKEN JWT
def create_access_token(data: dict, expires_minutes: int = None):
    """
    Crea un token JWT con fecha de expiración.
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=(expires_minutes or Settings.access_token_expire_minutes)
    )

    # Se agrega el campo de expiración
    to_encode.update({"exp": expire})

    # Se firma el token con la clave secreta
    return jwt.encode(to_encode, Settings.jwt_secret, algorithm=ALGORITHM)


# DECODIFICACIÓN DE TOKEN
def decode_token(token: str):
    """
    Decodifica y valida un token JWT.
    """
    try:
        payload = jwt.decode(token, Settings.jwt_secret, algorithms=[ALGORITHM])
        return payload
    except JWSError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no valido o expirado"
        )


# OBTENER USUARIO ACTUAL
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Obtiene el usuario autenticado a partir del token JWT.
    Espera: Authorization: Bearer <token>
    """

    # Verifica que el esquema sea Bearer
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Esquema invalido"
        )

    token = credentials.credentials

    # Decodifica el token
    payload = decode_token(token)

    # Obtiene el subject (id del usuario)
    sub = payload.get("sub")

    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token sin subject"
        )

    # Busca el usuario en la base de datos
    user = db.query(models.User).filter(models.User.id == int(sub)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    return user