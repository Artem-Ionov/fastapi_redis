from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

db_url = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(db_url)        # Создаём асинхронный движок
AsyncSession = async_sessionmaker(engine)   # Асинхронную фабрику сессий


async def get_db():
    """Функция-генератор сессий для каждого запроса"""
    async with AsyncSession() as session:
        yield session


class Base(DeclarativeBase):
    """Базовый класс для всех моделей, в который можно занести общий функционал"""
    pass


class SpimexTradingResults(Base):
    """Класс-модель для взаимодействия с БД"""

    __tablename__ = "spimex_trading_results"

    id = Column(Integer, primary_key=True)
    exchange_product_id = Column(String(20))
    exchange_product_name = Column(String(200))
    oil_id = Column(String(10))
    delivery_basis_id = Column(String(10))
    delivery_basis_name = Column(String(100))
    delivery_type_id = Column(String(5))
    volume = Column(Integer)
    total = Column(Float)
    count = Column(Integer)
    date = Column(String(10))
    created_on = Column(DateTime, default=datetime.now)
    # onupdate обновляет автоматически при любом изменении
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)
