import logging

from fastapi import Request, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import SpimexTradingResults, get_db
from models import TradingResults
from redis_cache import RedisCache


logger = logging.getLogger(__name__)

cache = RedisCache()

class CasheHandler:
    def __init__(self, key: str):
        self.key = key

    async def get(self):
        cached_data = await cache.get(self.key)
        if cached_data is not None:
            logger.info(f"Берём данные из кэша по ключу {self.key}")
        return cached_data
    
    async def set(self, data):
        ttl = await cache.get_ttl()
        await cache.set(self.key, data, ttl)
        logger.info(f"Сохраняем данные в кэш по ключу {self.key}")


async def get_cache(request: Request):
    cache_key = str(request.url)     # для redis_cache
    return CasheHandler(cache_key)


async def get_dates(
    days_back: int = Query(default=5, description="Количество последних торговых дней"),
    db: AsyncSession = Depends(get_db)
):
    
    stmt = (
        select(SpimexTradingResults.date)
        .distinct()
        .order_by(SpimexTradingResults.date.desc())
        .limit(days_back)
    )

    result = await db.execute(stmt)  
    dates = result.scalars().all()   
    return dates


async def get_trades_dynamics(
    start_date: str = Query(..., description="Начальная дата"),
    end_date: str = Query(..., description="Конечная дата"),
    oil_id: str | None = Query(None, description="Фильтр по коду нефтепродукта"),
    delivery_type_id: str | None = Query(None, description="Фильтр по типу поставки"),
    delivery_basis_id: str | None = Query(None, description="Фильтр по базису"),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(SpimexTradingResults).where(
        SpimexTradingResults.date.between(start_date, end_date)
    )

    if oil_id:
        stmt = stmt.where(SpimexTradingResults.oil_id == oil_id)
    if delivery_type_id:
        stmt = stmt.where(SpimexTradingResults.delivery_type_id == delivery_type_id)
    if delivery_basis_id:
        stmt = stmt.where(
            SpimexTradingResults.delivery_basis_id == delivery_basis_id
        )

    result = await db.execute(stmt)
    trades = result.scalars().all()

    # Преобразуем объекты SQLalchemy в dict для корректного сохранения в Redis
    trades_dict = [
        TradingResults.model_validate(trade).model_dump() for trade in trades
    ]

    return trades_dict


async def get_trades_results(
    limit: int = Query(default=10, description="Количество последних торгов"),
    oil_id: str | None = Query(None, description="Фильтр по коду нефтепродукта"),
    delivery_type_id: str | None = Query(None, description="Фильтр по типу поставки"),
    delivery_basis_id: str | None = Query(None, description="Фильтр по базису"),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(SpimexTradingResults).limit(limit)

    if oil_id:
        stmt = stmt.where(SpimexTradingResults.oil_id == oil_id)
    if delivery_type_id:
        stmt = stmt.where(SpimexTradingResults.delivery_type_id == delivery_type_id)
    if delivery_basis_id:
        stmt = stmt.where(
            SpimexTradingResults.delivery_basis_id == delivery_basis_id
        )

    result = await db.execute(stmt)
    trades = result.scalars().all()

    trades_dict = [
        TradingResults.model_validate(trade).model_dump() for trade in trades
    ]

    return trades_dict
