import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import SpimexTradingResults, get_db
from models import TradingResults
from redis_cache import RedisCache

cache = RedisCache()

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/trading-dates", response_model=list[str])
async def get_last_trading_dates(
    days_back: int = Query(default=5, description="Количество последних торговых дней"),
    db: AsyncSession = Depends(get_db),
):
    """Получение дат торгов с фильтрацией по количеству торговых дней"""

    # Формируем уникальный ключ из параметров запроса
    cache_key = f"trading_date: {days_back}"
    cached_data = await cache.get(cache_key)
    if cached_data is not None:
        logger.info(f"Берём данные из кэша по ключу {cache_key}")
        return cached_data

    try:
        # Объект ORM-запроса
        stmt = (
            select(SpimexTradingResults.date)
            .distinct()
            .order_by(SpimexTradingResults.date.desc())
            .limit(days_back)
        )
        result = await db.execute(stmt)  # Выполняем ORM-запрос
        dates = result.scalars().all()   # Преобразуем в список дат

        ttl = await cache.get_ttl()
        await cache.set(cache_key, dates, ttl)
        logger.info(f"Сохраняем данные в кэш по ключу {cache_key}")

    except Exception as e:
        logger.error(f"Ошибка при получении данных {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {e}")

    return dates


@router.get("/dynamics", response_model=list[TradingResults])
async def get_dynamics(
    start_date: str = Query(..., description="Начальная дата"),
    end_date: str = Query(..., description="Конечная дата"),
    oil_id: str = Query(None, description="Фильтр по коду нефтепродукта"),
    delivery_type_id: str = Query(None, description="Фильтр по типу поставки"),
    delivery_basis_id: str = Query(None, description="Фильтр по базису поставки"),
    db: AsyncSession = Depends(get_db),
):
    """Получение списка торгов за заданный период"""

    try:
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
    except Exception as e:
        logger.error(f"Ошибка при получении данных {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {e}")
    return trades


@router.get("/trading-results", response_model=list[TradingResults])
async def get_trading_results(
    limit: int = Query(default=10, description="Количество последних торгов"),
    oil_id: str = Query(None, description="Фильтр по коду нефтепродукта"),
    delivery_type_id: str = Query(None, description="Фильтр по типу поставки"),
    delivery_basis_id: str = Query(None, description="Фильтр по базису поставки"),
    db: AsyncSession = Depends(get_db),
):
    """Получение списка последних торгов"""

    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {e}")
    return trades
