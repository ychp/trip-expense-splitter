from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    
    DATABASE_URL: str = f"sqlite:///{DATA_DIR}/family_finance.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
settings.DATA_DIR.mkdir(exist_ok=True)
