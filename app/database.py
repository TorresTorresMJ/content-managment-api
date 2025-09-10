from sqlmodel import SQLModel, create_engine, Session
import os

# Configuración de la base de datos
# SQLite para desarrollo/produccion
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./content.db")

# Crear el motor de la base de datos
# echo=True muestra las SQL queries en consola (útil para desarrollo)
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Crea todas las tablas definidas en los modelos SQLModel"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Obtiene una sesión de base de datos para interactuar con ella"""
    with Session(engine) as session:
        yield session