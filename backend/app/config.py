from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI应用"
    DEBUG_MODE: bool = True
    API_PREFIX: str = "/api"
    
    class Config:
        env_file = ".env"

settings = Settings() 