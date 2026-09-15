"""Runtime configuration for the agent-host service.

Settings are loaded from environment variables and an optional ``.env`` file
in the process working directory.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application settings for the agent-host.

    Attributes:
        gemini_api_key: API key for Gemini model access.
        groq_api_key: API key for Groq model access.
    """

    gemini_api_key: str
    groq_api_key: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()