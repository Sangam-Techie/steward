"""Runtime configuration for the control-plane service.

Settings are loaded from environment variables and an optional ``.env`` file
in the process working directory.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application settings for the control-plane.

    Attributes:
        database_url: SQLAlchemy-compatible database connection string.
        environment: Deployment environment name (defaults to ``development``).
    """

    database_url : str
    environment : str = "development"

    model_config =  SettingsConfigDict(env_file=".env")

settings = Settings()