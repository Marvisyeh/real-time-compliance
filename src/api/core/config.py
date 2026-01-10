import os
from typing import Optional


class DBConfig:
    # 支持两种环境变量命名方式，优先使用 POSTGRES_* 格式（与 consumers 保持一致）
    DB_USER: Optional[str] = os.getenv("POSTGRES_USER")
    DB_PASSWORD: Optional[str] = os.getenv("POSTGRES_PASSWORD")
    DB_HOST: Optional[str] = os.getenv("POSTGRES_HOST")
    DB_PORT: Optional[str] = os.getenv("POSTGRES_PORT")
    DB_NAME: Optional[str] = os.getenv("POSTGRES_DB")

    @classmethod
    def get_db_url(cls) -> str:
        db_url = os.getenv("DB_URL")
        if db_url:
            return db_url

        if cls.DB_USER and cls.DB_PASSWORD and cls.DB_HOST and cls.DB_NAME:
            return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"

        assert False, "DB_URL or database credentials (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB) are not set"


class APIConfig:
    API_TITLE: str = os.getenv("API_TITLE", "Monitoring API")
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")
    API_DESCRIPTION: str = os.getenv(
        "API_DESCRIPTION", "Monitoring and Alerting API")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
