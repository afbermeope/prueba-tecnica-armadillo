from fastapi import APIRouter
from app.api.api_v1.endpoints import category_endpoints, item_endpoints, event_endpoints, warehouse_endpoints

api_router = APIRouter()
api_router.include_router(category_endpoints.router, prefix="/categories", tags=["categories"])
api_router.include_router(item_endpoints.router, prefix="/items", tags=["items"])
api_router.include_router(event_endpoints.router, prefix="/events", tags=["events"])
api_router.include_router(warehouse_endpoints.router, prefix="/departures", tags=["departures"])
