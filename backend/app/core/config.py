from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = "u-sell-it API"
    environment: str = "dev"

    database_url: str = Field(alias="DATABASE_URL")

    jwt_secret_key: str = Field(alias="JWT_SECRECT_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_hours: int = Field(
        default=24, alias="ACCESS_TOKEN_EXPIRE_HOURS"
    )
    refresh_token_expire_days: int = Field(
        default=90, alias="REFRESH_TOKEN_EXPIRE_DAYS"
    )

    class Config:
        env_file = ".env.example"  # Placeholder and will need to be updated
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
