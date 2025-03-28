from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    PROJECT_NAME: str = "FastAPI ToDo App"
    DATABASE_URL: str = "sqlite+aiosqlite:///./todos.db"
    PROJECT_DESCRIPTION: str = "A todolist with FastAPI."
    PROJECT_VERSION: str = "0.1.0"
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True



settings = Settings()
