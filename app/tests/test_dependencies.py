import pytest

from dependencies import get_dates, get_trades_dynamics, get_trades_results


@pytest.mark.asyncio
async def test_get_dates(configure_test_db, test_data_insert):
    dates = await get_dates(days_back=3, db=configure_test_db)

    assert len(dates) == len(test_data_insert)
    assert dates == ["20251202", "20251201"]


@pytest.mark.asyncio
async def test_get_trades_dynamics(configure_test_db, test_data_insert):
    trades = await get_trades_dynamics(
        start_date="20251120", 
        end_date="20251201",
        oil_id=None,
        delivery_type_id=None,
        delivery_basis_id=None, 
        db=configure_test_db
        )

    assert len(trades) == len(test_data_insert) - 1
    assert trades[0]["exchange_product_id"] == "A692URT005A"


@pytest.mark.asyncio
async def test_get_trades_results(configure_test_db, test_data_insert):
    trades = await get_trades_results(
        limit = 2,
        oil_id=None,
        delivery_type_id=None,
        delivery_basis_id=None, 
        db=configure_test_db
        )

    assert len(trades) == len(test_data_insert)
    assert trades[0]["exchange_product_name"] == "Бензин (АИ-92-К5)"
    