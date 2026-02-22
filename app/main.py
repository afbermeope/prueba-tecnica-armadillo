from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.db import base
from app.api.api_v1.api import api_router
from app.core.exceptions import BusinessException

app = FastAPI(
    title="FastAPI prueba técnica API",
    openapi_url="/api/v1/openapi.json"
)

@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Bienvenido a la prueba técnica de armadillo, revisa la ruta /docs para la documentación."}
