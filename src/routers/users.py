from fastapi import APIRouter, Depends

from ..auth import oauth2_scheme, get_current_user
from ..database import db
from ..models.user import User, DBUser

router = APIRouter()

@router.get("/users/", tags=["Usuarios"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/users/me", response_model=User, tags=["Usuarios"])
async def read_user_me(current_user: DBUser = Depends(get_current_user)):
    # Quitar la contraseña de los datos que se envian al cliente
    user = dict(current_user)
    user.pop('password_hash')
    return user

@router.get("/users/{username}", tags=["Usuarios"])
async def read_user(username: str):
    return {"username": username}
