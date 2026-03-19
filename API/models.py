from pydantic import BaseModel
from datetime import date
from typing import Optional



class Usuari(BaseModel):
    id: Optional[int] = None
    nom: str
    rol: Optional[str] = None
    password: str

class Material(BaseModel):
    id: int
    descripcio: str
    imatge: str

class Reserva(BaseModel):
    idusuari: int
    idmaterial: int
    datareserva: date
    datafinal: date

