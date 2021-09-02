from datetime import datetime, timedelta
from decouple import config
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional

from .database import db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
	return pwd_context.hash(password)

def verify_password(plaintext: str, hashed: str):
	return pwd_context.verify(plaintext, hashed)

def create_token(data: dict, expires_delta: Optional[timedelta] = None):
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=15)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, config('JWT_SECRET'), algorithm="HS256")
	return encoded_jwt

def decode_token(token: str):
	return jwt.decode(token, config('JWT_SECRET'), algorithms=["HS256"])

async def get_current_user(token: str = Depends(oauth2_scheme)):
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
		headers={"WWW-Authenticate": "Bearer"},
	)
	try:
		payload = decode_token(token)
		user_email = payload.get('sub')
		if user_email is None:
			raise credentials_exception
	except JWTError:
		raise credentials_exception
	query = "SELECT * FROM `usuarios` WHERE `email` = :email"
	user = await db.fetch_one(query=query, values={"email": user_email})
	if user is None:
		raise credentials_exception
	return user
