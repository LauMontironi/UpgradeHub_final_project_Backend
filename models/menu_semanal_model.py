from pydantic import BaseModel
from typing import Optional

class MenuSemanalCreate(BaseModel):
    numero: int
    titulo: str
    descripcion: Optional[str] = None
    foto_url: Optional[str] = None
    precio: float
    activo: bool = True
    fecha: str  # YYYY-MM-DD

class MenuSemanalUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    foto_url: Optional[str] = None
    precio: Optional[float] = None
    activo: Optional[bool] = None
    fecha: Optional[str] = None