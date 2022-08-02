from pathlib import Path

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).parent.absolute()

ENV = {
    "_env_file": BASE_DIR / ".env",
    "_env_file_encoding": "utf-8"
}


class Settings(BaseSettings):
    ssl_cert: str = Field(None, env="SSL_CERT")
    ssl_key: str = Field(None, env="SSL_KEY")
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8000, env="PORT")
    verify_ssl: bool = Field(True, env="VERIFY_SSL")
    gd_service_url: str = Field(..., env="GD_SERVICE_URL")
    gd_api_key: str = Field(..., env="GD_API_KEY")
    log_path: Path = Field(BASE_DIR.parent.parent.joinpath("logs"), env="LOG_PATH")


settings = Settings(**ENV)
