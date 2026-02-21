from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Ecosystem"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/prueba-tecnica-armadillo"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
