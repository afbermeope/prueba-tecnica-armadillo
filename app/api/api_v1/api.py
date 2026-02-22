from app.api.api_v1.endpoints import item_endpoints, event_endpoints, person_endpoints, warehouse_endpoints, location_endpoints, role_endpoints
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(item_endpoints.router, prefix="/items", tags=["items"])
api_router.include_router(event_endpoints.router, prefix="/events", tags=["events"])
api_router.include_router(person_endpoints.router, prefix="/persons", tags=["persons"])
api_router.include_router(warehouse_endpoints.router, prefix="/warehouses", tags=["warehouses"])
api_router.include_router(location_endpoints.router, prefix="/locations", tags=["locations"])
api_router.include_router(role_endpoints.router, prefix="/roles", tags=["roles"])
