import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "password")

    MYSQL_WRITE_HOST: str = os.getenv("MYSQL_WRITE_HOST")
    MYSQL_WRITE_PORT: int = int(os.getenv("MYSQL_WRITE_PORT", 3306))

    MYSQL_READ_HOSTS_RAW: str = os.getenv("MYSQL_READ_HOSTS", "")
    MYSQL_READ_PORT: int = int(os.getenv("MYSQL_READ_PORT", 3306))

    MYSQL_DB: str = os.getenv("MYSQL_DB", "fastapi")

    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", 4))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", 4))
    DB_POOL_TIMEOUT: int = int(os.getenv("DB_POOL_TIMEOUT", 3))

    DATABASE_WRITE_URL: str = ""
    DATABASE_READ_URLS: list[str] = []

    JWT_SECRET: str = "supersecret"
    JWT_ALGO: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    def __init__(self, **values):
        super().__init__(**values)

        self.DATABASE_WRITE_URL = (
            f"mysql+asyncmy://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_WRITE_HOST}:{self.MYSQL_WRITE_PORT}/{self.MYSQL_DB}"
        )

        read_hosts = [
            h.strip() for h in self.MYSQL_READ_HOSTS_RAW.split(",") if h.strip()
        ]

        self.DATABASE_READ_URLS = [
            f"mysql+asyncmy://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{host}:{self.MYSQL_READ_PORT}/{self.MYSQL_DB}"
            for host in read_hosts
        ]


settings = Settings()
