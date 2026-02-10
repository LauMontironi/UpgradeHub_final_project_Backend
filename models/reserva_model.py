from pydantic import BaseModel
from typing import Optional

class ReservaCreate(BaseModel):
    mesa_id: int
    fecha: str 
    hora: str 
    party_size: int
    resena: Optional[str] = None  # Opcional por si no escriben nada al reservar

class ReservaReview(BaseModel):
    resena: str