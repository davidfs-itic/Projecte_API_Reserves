from pydantic import BaseModel
from datetime import date



class Usuari(BaseModel):
    id: int
    nom: str
    rol: str
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

