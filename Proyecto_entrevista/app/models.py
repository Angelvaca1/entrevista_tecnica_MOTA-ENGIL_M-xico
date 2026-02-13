from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
 #permite crear relacipnes entre modelos NO crea columnas, crea vinculos ORM entre objetos
from sqlalchemy.orm import relationship
from app.db import Base
from sqlalchemy.sql import func


"""
ejemplo y aclaraciones:
PYTHON = id = Column(Integer, primary_key=True, index=True)
esto se convierte en sql a esto id INT PRIMARY KEY AUTO_INCREMENT

nullable=False no puede ser NULL (o sea texto obligatorio)
unique=True no puede repetirse
index=True búsquedas más rápidas
"""

#MODELO:USER

class User(Base):
    """
    Modelo que representa la tabla 'users' en la base de datos. 
    Cada instancia de esta clase representa a un usuario
    """
    #Nombre de la tabla en Mysql :3
    __tablename__ = "users"

    #clave primaria del usario
    id = Column(Integer,primary_key=True, index=True)

    # Nombre del usuario(obligatorio)
    nombre = Column(String(100), nullable=False)
    # Correo electronico(unico, obligatorio y con indice para busquedas rapidas)
    correo = Column(String(150), unique=True, index=True, nullable=False)
    # Telefono de usuario(obligatorio)
    telefono = Column(String(15), nullable=False)
    # Hash de la contraseña(No se guarda la contraseña si no el encriptado como un jeasfugsr0fhage)
    password_hash = Column(String(225), nullable=False)
    # Fecha de la contraseña automatica generada por la base de datis
    created_at = Column(TIMESTAMP, server_default=func.now())


    """
    -Relación uno a muchos con Document
    -Un usuario puede tener multiples documentos
    -Cascade="all,delete-orphan" funciona para que en dada ocasión si se borra el user
    se eliminan sus documentos junto con los datos que se borraron anteriormente


    para que se vea bonito y más ordenado usualmente se pone 
    documents = relationship(
        "Document",
        back_populates="owner",
        cascade="all, delete-orphan"
        pero la vrd casi se me va la onda de hacerlo bonito jsjsjsj  :c 
        dejo el ejemplo aqui arriba y como usualmente lo hago abajo
    """
    documents = relationship("Document", back_populates="owner", cascade="all,delete-orphan")

#MODELO: DOCUMENT

class Document(Base):
    """
    Modelo que representa la tabla 'documents'.
    Cada documento pertenece a un usuario
    """

    #Nombre real de la tabla
    __tablename__ = "documents"
    #Clave primaria del documento
    id = Column (Integer, primary_key=True, index=True)

    #clave foranea que apunta a user.id
    #ondelete="CASCADE" asegura que si el usuario se elimina Tambien se eliminan sus documentos de la DB
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Tipo de documento (ejemplo: ine, cv, pasaporte,etc etc etc.)
    tipo_documento = Column(String(100), nullable=False)
    # Nombre original del archivo subido por el usuario
    original_filename = Column(String(255),nullable=False)
    # Nombre interno con el que se guarda en el servidor
    # unique=True evita que se repita
    stored_filename = Column(String(255), unique=True, nullable=False)
    #tipo MINE del archivo (eemplo: application/pdf, image/png)
    mime_type = Column(String(100), nullable=False)

    #tamaño del archivo en bytes
    size = Column(Integer,nullable=False)
    #Fecha de creación automatica
    created_at = Column(TIMESTAMP,server_default=func.now())

    #Relación inversa hacía User
    #Permite acceder al usuario dueño del documento:
    #document.owner
    owner = relationship("User", back_populates="documents")