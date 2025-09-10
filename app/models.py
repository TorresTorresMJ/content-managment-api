from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# Opcional: Enums para categorías (como los tableros de Pinterest)
class ContentCategory(str, Enum):
    TECHNOLOGY = "technology"
    DESIGN = "design"
    TRAVEL = "travel"
    FOOD = "food"
    ART = "art"
    EDUCATION = "education"

# Modelo principal de contenido
class Content(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    image_url: Optional[str] = None
    category: ContentCategory = Field(default=ContentCategory.TECHNOLOGY)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    # Configuración adicional para buen comportamiento
    class Config:
        arbitrary_types_allowed = True