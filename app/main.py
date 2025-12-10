import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import setup_logging
# Выполняем настройку до импортирования функций, чтобы в них работало логирование
setup_logging()
import routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Действия, выполняющиеся при старте и завершении приложения"""
    logger = logging.getLogger(__name__)
    logger.info("Начало работы приложения")
    yield
    logger.info("Окончание работы приложения")


app = FastAPI(title="Данные о торгах", lifespan=lifespan)

# Подключаем остальные маршруты
app.include_router(routers.router)


@app.get("/")
async def root():
    """Корневой маршрут для проверки работоспособности"""
    return {"message": "Добро пожаловать!"}
