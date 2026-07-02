from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env.example", extra="ignore")

    project_name: str = "CogniWatch"
    environment: str = "development"
    database_url: str = "sqlite:///./cogniwatch.db"
    jwt_secret_key: str = "change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440
    backend_cors_origins: str = "http://localhost:3000"
    fcm_credentials_json: str | None = None
    fcm_enabled: bool = False
    ml_artifacts_dir: str = "/workspace/ml/artifacts"
    default_timezone: str = "America/Lima"

    @property
    def cors_origins_list(self) -> list[str]:
        return [item.strip() for item in self.backend_cors_origins.split(',') if item.strip()]


settings = Settings()
