import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.db import get_db
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from app.config import Settings

router = APIRouter()

#Esta es la configuración, esto restringe los tipos de archivo permitidos. 
ALLOWED_MIMES = {"application/pdf","image/jpeg","image/png"} #se ocupa jpeg para jgp pero ambas son validas, una es la versión extendida y la otra corta según mi investigación
ALLOWED_EXT = {".pdf",".jpeg",".png"}

#registro
"""
Flujo explicado:
1- se verifica si el correo ya existe, si es el caso sale error code 400 "este correo esta en uso" pq tenemos unique=True y debe de ser unico
2- si el procedimimento paso bien se hassea la contraseña 
3- Guardamos el usuario creado en la DB 
4-Devolvemos datos del usuario pero sin la password(ya encriptada)
"""

@router.post("/register", response_model=schemas.UserOut)
def register (payload: schemas.UserCreate,db: Session = Depends(get_db)):
    #validaciones
    existing = db.query(models.User).filter(models.User.correo == payload.correo.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Este correo esta en uso")
    user = models.User(
        nombre=payload.nombre,
        correo=payload.correo.lower(),
        telefono=payload.telefono,
        password_hash=hash_password(payload.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#login
"""
flujo explicado:
1- Busca usuario por correo
2-verifica contraseña
3-genera jwt
4-Devuelve un json similar a este:

{
  "access_token": "token super grandote y muy malote >:3",
  "token_type": "bearer"
}

"""
@router.post("/login", response_model=schemas.Token)
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    #Usamos los datos de correo y password del payload(La librería para validar datos)
    user = db.query(models.User).filter(
        models.User.correo == data.correo.lower()
).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas"
        )
    token = create_access_token({"sub": str(user.id)}) 
    return {"access_token": token, "token_type": "bearer"}


#Upload document
"""
hacemos validaciones:

Tipo MIME permitido
Extensión válida
Tamaño máximo
Usuario autenticado

"""
@router.post("/documents/upload", response_model=schemas.DocumentOut)
async def upload_document(tipo_documento: str,archivo:UploadFile = File(...), current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    #validación de mime y exit
    if archivo.content_type not in ALLOWED_MIMES:
        raise HTTPException(status_code=400,detail="formato no permitido")
    
    #ext
    ext = os.path.splitext(archivo.filename)[1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400,detail="Formato no permitido")
    
    #asegurar uploads dir
    os.makedirs(Settings.upload_dir, exist_ok=True)

    #sgenera nombres unico para almacenar: esto es para evitar sobrescritura o problemas de seguridad 
    stored_filename = f"{uuid.uuid4().hex}{ext}" 
    file_path = os.path.join(Settings.upload_dir, stored_filename)

    #Guardar en disco en chunks y validar tamaño sin cargar todo en memoria
    size = 0
    with open(file_path, "wb") as f:
        while True:
            chunk = await archivo.read(1024 * 1024) #leer 1MB por vez
            if not chunk:
                break
            size += len(chunk)
            if size > Settings.max_file_size:
            #Elimar archivos parciales y lanza error 
                f.close()
                os.remove(file_path)
                raise HTTPException(status_code=400, detail="Archivo excede el tamaño maximo de 5mb")
            f.write(chunk)



    # persistir metadata en DB. No se guarda el archivo en la base de datos si no en el Disco
    doc = models.Document(
        user_id=current_user.id,
        tipo_documento=tipo_documento,
        original_filename=archivo.filename,
        stored_filename=stored_filename,
        mime_type=archivo.content_type,
        size=size
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # Devolver vista limitada
    return doc 

#Listar documentos del usuario
@router.get("/documents", response_model=List[schemas.DocumentOut])
def list_documents(current_user:models.User=Depends(get_current_user),db:Session=Depends(get_db)):
    docs = db.query(models.Document).filter(models.Document.user_id == current_user.id).all()
    return docs

# --------- Descargar documento ----------
@router.get("/documents/{document_id}/download")
def download_document(document_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    doc = db.query(models.Document).filter(models.Document.id == document_id, models.Document.user_id == current_user.id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    file_path = os.path.join(Settings.upload_dir, doc.stored_filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Archivo no disponible")
    # FileResponse hará streaming
    return FileResponse(path=file_path, filename=doc.original_filename, media_type=doc.mime_type)