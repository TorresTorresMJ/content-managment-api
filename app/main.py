from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from app.database import create_db_and_tables, get_session
from app.models import Content
from app.schemas import ContentCreate

app = FastAPI(title="Content Management API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Endpoint para crear contenido
@app.post("/content/", response_model=Content)
def create_content(content: ContentCreate, session: Session = Depends(get_session)):
    # Convierte el schema de creación en un modelo de base de datos
    db_content = Content.model_validate(content)
    
    # Guarda en la base de datos
    session.add(db_content)
    session.commit()
    session.refresh(db_content)
    
    return db_content

@app.get("/")
def read_root():
    return {"message": "Content Management API is running!"}

# Endpoint para OBTENER todo el contenido
@app.get("/content/", response_model=list[Content])
def get_all_content(session: Session = Depends(get_session)):
    # Consulta TODOS los contenidos de la base de datos
    contents = session.exec(select(Content)).all()
    return contents

@app.get("/health")
def health_check():
    return {"status": "healthy"}