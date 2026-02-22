# Event Control System - EventLog (Prueba Técnica Armadillo)

Este sistema permite la gestión y trazabilidad de recursos físicos para eventos, con una arquitectura modular y escalable.

## Requisitos
- Python 3.10+
- PostgreSQL
- FastAPI + SQLAlchemy + Alembic

## Estructura Modular

El proyecto sigue una organización por capas y una estructura de **un archivo por entidad**:

- `app/api/api_v1/endpoints/`: Endpoints descriptivos (`category_endpoints.py`, `item_endpoints.py`, etc.).
- `app/services/`: Lógica de negocio modularizada (`resource_service.py`, `event_service.py`, etc.).
- `app/models/`: Modelos SQLAlchemy separados por entidad.
- `app/schemas/`: Esquemas Pydantic separados por entidad.
- `app/db/`: Configuración de sesión y persistencia.

## Configuración y Ejecución

1. **Dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Base de Datos**: 
   - Configura el `DATABASE_URL` en el archivo `.env`. (Nombre recomendado: `prueba-tecnica-armadillo`).
   - Ejecuta el script de creación inicial:
     ```bash
     python create_db.py
     ```
3. **Migraciones**:
   - Aplica la estructura de tablas con Alembic:
     ```bash
     alembic upgrade head
     ```
4. **Ejecutar**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Documentación API
Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
