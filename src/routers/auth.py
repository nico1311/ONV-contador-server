from datetime import timedelta
from decouple import config
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..auth import oauth2_scheme, hash_password, verify_password, create_token
from ..database import db
from ..models.user import User

router = APIRouter()

async def get_user(email: str):
	query = "SELECT * FROM `usuarios` WHERE `email` = :email"
	user = await db.fetch_one(query=query, values={"email": email})
	return user


@router.post("/auth/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
	'''Autenticar mediante email y contraseña.
	Devuelve un token JWT'''
	user = await get_user(form_data.username)
	if not user:
		raise HTTPException(status_code=400, detail="Usuario inexistente")
	if not verify_password(form_data.password, user.password_hash):
		raise HTTPException(status_code=400, detail="Contraseña incorrecta")
	access_token_expires = timedelta(minutes=config('TOKEN_EXPIRY_MINUTES', default=1440, cast=int))
	access_token = create_token(
		data={"sub": user.email}, expires_delta=access_token_expires
	)

	return {
		"access_token": access_token,
		"token_type": "bearer",
		"expires_in": access_token_expires
	}
