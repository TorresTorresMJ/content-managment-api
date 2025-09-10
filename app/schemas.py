from sqlmodel import SQLModel  # ¡AÑADE ESTA IMPORTACIÓN!
from typing import Optional
from app.models import ContentCategory

# Schema para CREAR contenido (sin ID ni fechas, eso lo pone la DB)
class ContentCreate(SQLModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    category: ContentCategory = ContentCategory.TECHNOLOGY