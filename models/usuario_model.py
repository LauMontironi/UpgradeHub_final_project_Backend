from pydantic import BaseModel, EmailStr
from typing import Optional

# 📥 Lo que el cliente envía para registrarse
class UsuarioCreate(BaseModel):
    nombre: str
    apellido: str
    dni: str
    email: EmailStr
    password: str
    telefono: Optional[str] = None
    edad: int
    alergias: Optional[str] = None
    rol: Optional[str] = "cliente"



# 📤 Lo que la API devuelve al frontend (sin contraseña)
class UsuarioOut(BaseModel):
    id: int
    nombre: str
    apellido: str
    dni: str
    email: EmailStr
    telefono: Optional[str] = None
    edad: int
    alergias: Optional[str] = None
    rol: str

    class Config:
        from_attributes = True

# 🔐 Para login
class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str
