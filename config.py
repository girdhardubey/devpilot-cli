from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    database_url: str

    # Tells Pydantic to read variables from your .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Create a single settings object we can import anywhere
settings = Settings()