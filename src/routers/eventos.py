from datetime import datetime
from decouple import config
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from hashlib import sha1
from pymysql.err import IntegrityError

from ..logger import logger
from ..auth import get_current_user
from ..database import db
from ..models.user import User
from ..models.sucursal import Sucursal

router = APIRouter()

@router.get("/sucursales/{id}/eventos", tags=["Eventos"])
async def get_sucursal_events(id=int, user: User = Depends(get_current_user)):
	'''Obtener eventos de sucursal'''
	query = "SELECT * FROM `sucursales` WHERE `id` = :id"
	try:
		sucursal = await db.fetch_one(query=query, values={"id": id})
		if sucursal:
			# Permitir si el usuario es encargado de la sucursal, o es admin (role 1)
			if (sucursal.encargado == user.id) or (user.role == 1):
				query = "SELECT * FROM `eventos` WHERE `sucursal` = :id_sucursal"
				eventos = await db.fetch_all(query=query, values={"id_sucursal": sucursal.id})
				return eventos
			else:
				raise HTTPException(status_code=403, detail="No autorizado a ver eventos de esta sucursal")
		else:
			raise HTTPException(status_code=404, detail="Sucursal no encontrada")
	except HTTPException as e: # Si es un HTTPException, enviarlo como tal
		raise e
	except Exception as e:
		logger.exception(e)
		raise HTTPException(status_code=500, detail="Error no especificado")

@router.post("/sucursales/{id}/eventos", status_code=201, tags=["Eventos"])
async def get_sucursal_events(request: Request, id=int, user: User = Depends(get_current_user)):
	'''Crear evento (endpoint utilizado por el frontend)'''
	query = "SELECT * FROM `sucursales` WHERE `id` = :id"
	try:
		sucursal = await db.fetch_one(query=query, values={"id": id})
		if sucursal:
			# Permitir si el usuario es encargado de la sucursal, o es admin (role 1)
			if (sucursal.encargado == user.id) or (user.role == 1):
				body = await request.json()
				evt_type = int(body['tipo'])
				timestamp = datetime.utcnow().isoformat()
				if (evt_type not in (1, 2)):
					raise HTTPException(status_code=422, detail="Tipo de evento no válido")		
				event_query = "INSERT INTO `eventos` (sucursal, timestamp, tipo) VALUES (:sucursal, :timestamp, :tipo)"
				event_id = await db.execute(query=event_query, values={"sucursal": id, "timestamp": timestamp, "tipo": evt_type})
				return {
					"id": event_id,
					"sucursal": id,
					"timestamp": timestamp,
					"tipo": evt_type
				}
			else:
				raise HTTPException(status_code=403, detail="No autorizado a crear eventos de esta sucursal")
		else:
			raise HTTPException(status_code=404, detail="Sucursal no encontrada")
	except HTTPException as e: # Si es un HTTPException, enviarlo como tal
		raise e
	except Exception as e:
		logger.exception(e)
		raise HTTPException(status_code=500, detail="Error no especificado")

@router.post("/sucursales/{id}/eventos/hw", tags=["Eventos"])
async def create_sucursal_event_hw(request: Request, id=int):
	'''Crear evento (endpoint utilizado por los sensores)'''
	query = "SELECT * FROM `sucursales` WHERE `id` = :id"
	try:
		sucursal = await db.fetch_one(query=query, values={"id": id})
		if sucursal:
			hw_secret = config('HW_SECRET')
			api_key = sha1("{id}:{secret}".format(id=id, secret=hw_secret).encode()).hexdigest()
			key_header = request.headers.get('x-api-key')
			if key_header == api_key:
				body = await request.json()
				evt_type = int(body['tipo'])
				timestamp = datetime.utcnow().isoformat()
				if (evt_type not in (1, 2)):
					raise HTTPException(status_code=422, detail="Tipo de evento no válido")		
				event_query = "INSERT INTO `eventos` (sucursal, timestamp, tipo) VALUES (:sucursal, :timestamp, :tipo)"
				event_id = await db.execute(query=event_query, values={"sucursal": id, "timestamp": timestamp, "tipo": evt_type})
				return {
					"id": event_id,
					"sucursal": id,
					"timestamp": timestamp,
					"tipo": evt_type
				}
			else:
				raise HTTPException(status_code=401, detail="API key no válida")
		else:
			raise HTTPException(status_code=404, detail="Sucursal no encontrada")
	except HTTPException as e: # Si es un HTTPException, enviarlo como tal
		raise e
	except Exception as e:
		logger.exception(e)
		raise HTTPException(status_code=500, detail="Error no especificado")
