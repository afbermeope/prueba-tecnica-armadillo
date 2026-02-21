from fastapi import FastAPI
from app.api.api_v1.api import api_router

app = FastAPI(
    title="FastAPI prueba técnica API",
    openapi_url="/api/v1/openapi.json"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to your FastAPI API. Go to /docs for the documentation."}
