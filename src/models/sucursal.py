from typing import Optional
from pydantic import BaseModel

class Sucursal(BaseModel):
	nombre: str
	direccion: str
	localidad: str
	lat: str
	lng: str
	capacidad: int
	encargado: int
