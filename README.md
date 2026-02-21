# FastAPI Ecosystem

Estructura de proyecto profesional para FastAPI con versionamiento de endpoints.

## Estructura de Carpetas

- `app/`: Paquete principal de la aplicación.
  - `api/`: Enrutamiento de la API.
    - `api_v1/`: Endpoints de la Versión 1.
  - `core/`: Configuraciones globales.
  - `crud/`: Operaciones CRUD.
  - `db/`: Conexión y sesión de base de datos.
  - `models/`: Modelos de base de datos.
  - `schemas/`: Modelos de Pydantic.
- `main.py`: Punto de entrada de la aplicación.

## Cómo ejecutar

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecutar el servidor:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Acceder a la documentación:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
