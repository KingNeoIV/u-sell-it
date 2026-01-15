from pydantic_settings import BaseSettings
from pydantic import Field


# Application configuration settings.
# Values are loaded from environment variables defined in the .env file.
# Pydantic handles validation, type conversion, and alias mapping.
class Settings(BaseSettings):
    # Basic application metadata.
    app_name: str = "u-sell-it API"
    environment: str = "dev"

    # Database connection string.
    # Loaded from the DATABASE_URL environment variable.
    DATABASE_URL: str = Field(alias="DATABASE_URL")

    # JWT configuration for authentication.
    jwt_secret_key: str = Field(alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_hours: int = Field(
        default=24, alias="ACCESS_TOKEN_EXPIRE_HOURS"
    )
    refresh_token_expire_days: int = Field(
        default=90, alias="REFRESH_TOKEN_EXPIRE_DAYS"
    )

    class Config:
        # Path to the environment file used for loading configuration.
        env_file = ".env"
        env_file_encoding = "utf-8"

        # Ignore any extra environment variables not defined in this model.
        extra = "ignore"


# Instantiate the settings object so it can be imported across the application.
settings = Settings()
