from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.database import create_db_and_tables, get_session
from app.models import Content, ContentCategory
from app.schemas import ContentCreate, ContentUpdate

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

# Get contenido por ID
@app.get("/content/{content_id}", response_model=Content)
def get_content_by_id(content_id: int, session: Session = Depends(get_session)):
    content = session.get(Content, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    if not content.is_active:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

# Actualizar contenido por ID
@app.patch("/content/{content_id}", response_model=Content)
def update_content(content_id: int, content_data: ContentUpdate, session: Session = Depends(get_session)):
    content = session.get(Content, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    if not content.is_active:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Actualiza solo los campos que vienen en la request
    content_data_dict = content_data.dict(exclude_unset=True)
    for key, value in content_data_dict.items():
        setattr(content, key, value)
    
    session.add(content)
    session.commit()
    session.refresh(content)
    return content

# Borrado suave (soft delete) por ID
@app.delete("/content/{content_id}")
def delete_content(content_id: int, session: Session = Depends(get_session)):
    content = session.get(Content, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Soft delete: marca como inactivo en lugar de borrar
    content.is_active = False
    session.add(content)
    session.commit()
    return {"message": "Content deleted successfully"}

# Filtrar por categoría Y buscar en títulos (MEJORADO)
@app.get("/content/", response_model=list[Content])
def get_all_content(
    category: Optional[ContentCategory] = Query(None),
    search: Optional[str] = Query(None),
    session: Session = Depends(get_session)
):
    query = select(Content).where(Content.is_active == True)
    
    if category:
        query = query.where(Content.category == category)
    
    if search:
        query = query.where(Content.title.contains(search))
    
    contents = session.exec(query).all()
    return contents