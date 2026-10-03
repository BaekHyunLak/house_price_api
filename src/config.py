from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_path: str = "artifacts/model.pkl"
    raw_data_path: str = "data/raw/Housing.csv"
    processed_data_path: str = "data/processed/housing_cleaned.csv"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
