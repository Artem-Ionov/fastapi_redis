import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

import routers
from config import setup_logging
from middleware import catch_exceptions_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Начало работы приложения")
    yield
    logger.info("Окончание работы приложения")


app = FastAPI(title="Данные о торгах", lifespan=lifespan)

app.middleware("http")(catch_exceptions_middleware)

app.include_router(routers.router)
