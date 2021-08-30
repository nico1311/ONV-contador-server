from fastapi import FastAPI

from .database import db
from .routers import sucursales, users

app = FastAPI()

app.include_router(sucursales.router)
app.include_router(users.router)

@app.on_event("startup")
async def startup():
    # Conectar a la base de datos al arrancar servidor
    await db.connect()
    print("Conectado a base de datos")

@app.on_event("shutdown")
async def shutdown():
    # Desconectar al detener el servidor
    await db.disconnect()

@app.get("/")
async def root():
    return {"message": "Hello World"}
