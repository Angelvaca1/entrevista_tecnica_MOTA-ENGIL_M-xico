from fastapi import FastAPI
from app.db import engine,Base
from app.routes import router as api_router
import os
from app.config import Settings

#crear uploads folder
os.makedirs(Settings.upload_dir,exist_ok=True)

#crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Api Usuarios y Documentos")
app.include_router(api_router,prefix="/api")