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



# 📤 Lo que la API devuelve al frontend (sin contraseña)( para interfaz de usuario by id)
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

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    edad: Optional[int] = None
    alergias: Optional[str] = None

##no dejo que modifiquen ni mail ni dni ni rol asi no toco ni registro ni login 


class UsuarioPasswordUpdate(BaseModel):
    current_password: str
    new_password: str
