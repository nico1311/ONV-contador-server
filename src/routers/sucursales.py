from fastapi import APIRouter, HTTPException
from ..database import db

router = APIRouter()

@router.get("/sucursales", tags=["sucursales"])
async def get_all_sucursales():
    '''Obtener todas las sucursales'''
    query = "SELECT * FROM `sucursales`"
    sucursales = await db.fetch_all(query=query)
    return {"sucursales": sucursales}

@router.get("/sucursales/{id}", tags=["sucursales"])
async def get_sucursal(id=int):
    '''Obtener sucursal por ID'''
    query = "SELECT * FROM `sucursales` WHERE `id` = :id"
    sucursal = await db.fetch_one(query=query, values={"id": id})
    if sucursal:
        return sucursal
    else:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
