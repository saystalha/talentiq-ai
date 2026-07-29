from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings using Pydantic BaseSettings."""
    APP_NAME: str = "TalentIQ AI"
    APP_VERSION: str = "1.0.0"
    UPLOAD_FOLDER: str = "uploads"
    LOG_LEVEL: str = "INFO"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    SKILL_MATCH_WEIGHT: float = 0.40
    SEMANTIC_WEIGHT: float = 0.35
    EXPERIENCE_WEIGHT: float = 0.15
    EDUCATION_WEIGHT: float = 0.10

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
