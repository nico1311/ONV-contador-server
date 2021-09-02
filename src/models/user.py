from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
	nombre: str
	apellido: str
	email: str
	role: Optional[int] = 0

class DBUser(User):
	password_hash: str
