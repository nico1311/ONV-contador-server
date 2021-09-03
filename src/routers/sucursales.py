from fastapi import APIRouter, Depends, HTTPException, Response
from pymysql.err import IntegrityError

from ..logger import logger
from ..auth import get_current_user
from ..database import db
from ..models.user import User
from ..models.sucursal import Sucursal

router = APIRouter()

@router.get("/sucursales", tags=["sucursales"])
async def get_all_sucursales():
    '''Obtener todas las sucursales'''
    query = "SELECT * FROM `sucursales`"
    try:
        sucursales = await db.fetch_all(query=query)
        return {"sucursales": sucursales}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Error no especificado")

@router.get("/sucursales/{id}", tags=["sucursales"])
async def get_sucursal(id=int):
    '''Obtener sucursal por ID'''
    query = "SELECT * FROM `sucursales` WHERE `id` = :id"
    try:
        sucursal = await db.fetch_one(query=query, values={"id": id})
        if sucursal:
            return sucursal
        else:
            raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    except HTTPException as e: # Si es un HTTPException, enviarlo como tal
        raise e
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Error no especificado")

@router.get("/sucursales/{id}/capacidad", tags=["sucursales"])
async def get_sucursal_capacidad(id=int):
    '''Obtener la capacidad actual de una sucursal'''
    return {"capacidad": 20}

@router.post("/sucursales", status_code=201, tags=["sucursales"])
async def create_sucursal(sucursal: Sucursal, user: User = Depends(get_current_user)):
    '''Crear una sucursal'''
    if (user.role is not 1):
        raise HTTPException(status_code=403, detail="Usuario no autorizado a crear sucursales")
    query = "INSERT INTO `sucursales` (nombre, direccion, localidad, lat, lng, capacidad, encargado) VALUES (:nombre, :direccion, :localidad, :lat, :lng, :capacidad, :encargado)"
    try:
        sucursal_dict = sucursal.dict()
        new_id = await db.execute(query=query, values=sucursal_dict)
        sucursal_dict['id'] = new_id
        return sucursal_dict
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Usuario encargado no existe")
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Error no especificado")

## TODO: endpoint para modificar una sucursal (update)

@router.delete("/sucursales/{id}", response_class=Response, status_code=204, tags=["sucursales"])
async def delete_sucursal(id=int, user: User = Depends(get_current_user)):
    '''Eliminar una sucursal'''
    if (user.role is not 1):
        raise HTTPException(status_code=403, detail="Usuario no autorizado a eliminar sucursales")
    query = "DELETE FROM `sucursales` WHERE `id` = :id"
    try:
        await db.execute(query=query, values={"id": id})
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Error no especificado")
