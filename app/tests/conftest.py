from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database import Base, SpimexTradingResults


@pytest.fixture
def mock_get_cache():
    cache_handler = AsyncMock()
    cache_handler.get.return_value=None
    cache_handler.set = AsyncMock()
    return cache_handler


@pytest.fixture
def test_data():
    return [
        {
            "exchange_product_id":"A692URT005A",
            "exchange_product_name":"Бензин (АИ-92-К5)",
            "oil_id":"A692",
            "delivery_basis_id":"URT",
            "delivery_basis_name":"Сургут-25 БП",
            "delivery_type_id":"A",
            "volume":345,
            "total":21390000.0,
            "count":16,
            "date":"20251201"
        },
        {
            "exchange_product_id":"DE5EBTC065J",
            "exchange_product_name":"ДТ ЕВРО сорт E",
            "oil_id":"DE5E",
            "delivery_basis_id":"BTC",
            "delivery_basis_name":"БП (б.т.ц.) Осенцы",
            "delivery_type_id":"J",
            "volume":3575,
            "total":195205075.0,
            "count":38,
            "date":"20251202"
        }
    ]


@pytest_asyncio.fixture
async def configure_test_db():
    db_url = f"postgresql+asyncpg://postgres:123456@localhost:5432/test_async_db"
    engine = create_async_engine(db_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    AsyncSession = async_sessionmaker(engine, expire_on_commit=False)
    async with AsyncSession() as session:
         yield session

    await engine.dispose()


@pytest_asyncio.fixture
async def test_data_insert(test_data, configure_test_db):

    stmt = insert(SpimexTradingResults).values(test_data)
    await configure_test_db.execute(stmt)
    await configure_test_db.commit()

    return test_data
    
        
