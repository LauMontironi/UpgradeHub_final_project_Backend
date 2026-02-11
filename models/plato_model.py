from pydantic import BaseModel
from typing import Optional

class PlatoCreate(BaseModel):
    categoria: str      # 'entrante', 'principal', 'postre'
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    ingredientes: Optional[str] = None
    alergenos: Optional[str] = None
    info_nutricional: Optional[str] = None
    imagen_url: Optional[str] = None
    activo: bool = True

class PlatoUpdate(BaseModel):
    categoria: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    ingredientes: Optional[str] = None
    alergenos: Optional[str] = None
    info_nutricional: Optional[str] = None
    imagen_url: Optional[str] = None
    activo: Optional[bool] = None

class PlatoBase(BaseModel):
    categoria: str
    nombre: str
    descripcion: str
    precio: float
    ingredientes: Optional[str] = None
    alergenos: Optional[str] = None
    info_nutricional: Optional[str] = None
    imagen_url: Optional[str] = None