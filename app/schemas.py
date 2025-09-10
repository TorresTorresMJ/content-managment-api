from sqlmodel import SQLModel
from typing import Optional
from app.models import ContentCategory

class ContentCreate(SQLModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    category: ContentCategory = ContentCategory.TECHNOLOGY

class ContentUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[ContentCategory] = None