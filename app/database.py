from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings


db_url = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
engine = create_async_engine(db_url)
AsyncSession = async_sessionmaker(engine)


async def get_db():
    """Функция-генератор сессий для каждого запроса"""
    async with AsyncSession() as session:
        yield session


class Base(DeclarativeBase):
    pass


class SpimexTradingResults(Base):

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
