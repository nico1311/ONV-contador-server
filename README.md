# ONV-contador-server

## Configuración del entorno
----
1. Crear un entorno virtual usando `venv`: ejecutar `python -m venv .venv`. El entorno se crea en el subdirectorio `.venv` del directorio actual.
2. Activar el entorno virtual:

    Windows: `.venv\Scripts\Activate.ps1`
    
    Linux/Mac: `source .venv/bin/activate`

    Al activarse, el *prompt* de la terminal que se está usando mostrará `(.venv)` al inicio para indicar el entorno que está activado.


3. Instalar dependencias: `pip install -r requirements.txt`

### Ejecutar servidor
* Ejecutar en modo desarrollo con: `uvicorn src.main:app --reload`
* El server se inicia en http://localhost:8000
