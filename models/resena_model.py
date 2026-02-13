from pydantic import BaseModel
from typing import Optional
from datetime import date

class ResenaCreate(BaseModel):
    reserva_id: int
    comentario: str
    puntuacion: int  # Del 1 al 5
    fecha: str       # Formato 'YYYY-MM-DD'

class ResenaResponse(ResenaCreate):
    id: int
    usuario_id: int
    nombre: Optional[str] = None # Para mostrar quién la escribió

    class Config:
        from_attributes = True