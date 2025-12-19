import logging

from fastapi import APIRouter, Depends

from dependencies import get_cache, get_dates, get_trades_dynamics, get_trades_results
from models import TradingResults


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/trading-dates", response_model=list[str])
async def get_last_trading_dates(
    cache_handler=Depends(get_cache),
    dates=Depends(get_dates),
):

    cached_data = await cache_handler.get()
    if cached_data is not None:
        return cached_data

    await cache_handler.set(dates)

    return dates


@router.get(
    "/dynamics",
    response_model=list[TradingResults],
    summary="Получение списка торгов за заданный период",
)
async def get_dynamics(
    cache_handler=Depends(get_cache), trades=Depends(get_trades_dynamics)
):

    cached_data = await cache_handler.get()
    if cached_data is not None:
        return cached_data

    await cache_handler.set(trades)

    return trades


@router.get(
    "/trading-results",
    response_model=list[TradingResults],
    summary="Получение списка последних торгов",
)
async def get_trading_results(
    cache_handler=Depends(get_cache), trades=Depends(get_trades_results)
):

    cached_data = await cache_handler.get()
    if cached_data is not None:
        return cached_data

    await cache_handler.set(trades)

    return trades
