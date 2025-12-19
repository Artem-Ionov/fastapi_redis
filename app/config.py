import logging
import os

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DB_USER: str = Field(..., description="Имя пользователя БД")
    DB_PASS: str = Field(..., description="Пароль пользователя БД")
    DB_HOST: str = Field("localhost", description="Хост БД")
    DB_PORT: str = Field("5432", description="Порт БД")
    DB_NAME: str = Field(..., description="Название БД")

    REDIS_HOST: str = Field("localhost", description="Хост Redis")
    REDIS_PORT: int = Field(6379, description="Потр Redis")

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


settings = Settings()


def setup_logging():

    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    file_handler = logging.FileHandler(r"logs\app.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
