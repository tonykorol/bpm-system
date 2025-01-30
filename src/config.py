from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MODE: str

    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str

    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    model_config = ConfigDict(env_file=".env")

    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALGORITHM: str = "HS256"
    token_expires_minutes: int = 1440

    BEARER_TOKEN_TYPE: str = "Bearer"

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
