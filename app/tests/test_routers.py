import pytest
from fastapi.testclient import TestClient

from main import app
from routers import get_cache, get_dates, get_trades_dynamics, get_trades_results


client = TestClient(app)

@pytest.mark.parametrize(
    "days_back, expected_days",
    [
        (1, ["2025-12-01"]),
        (3, ["2025-12-01", "2025-12-03"]),
        (0, []),
        (10, ["2025-12-01", "2025-12-03"])
    ]
)
def test_trading_dates(mock_get_cache, days_back, expected_days):
    mock_dates = ["2025-12-01", "2025-12-03"]

    # Пишем мок-функцию, т.к. зависимость get_dates ожидает days_back и db
    async def mock_get_dates(days_back: int = 5, db = None):
        return mock_dates[:min(days_back, len(expected_days))]

    app.dependency_overrides = {
        get_dates: mock_get_dates,
        get_cache: lambda: mock_get_cache
    }

    try:
        response = client.get(f"/trading-dates?days_back={days_back}")
        assert response.status_code == 200
        assert response.json() == expected_days
    finally:
        app.dependency_overrides = {}


def test_dynamics(mock_get_cache, test_data):

    async def mock_get_trades_dynamics(
        start_date: str = "20251201",  
        end_date: str = "20251203",
        oil_id: str = None,
        delivery_type_id: str = None,
        delivery_basis_id: str = None,
        db = None
    ):
        return test_data
    
    app.dependency_overrides = {
        get_trades_dynamics: mock_get_trades_dynamics,
        get_cache: lambda: mock_get_cache
    }

    try:
        response = client.get("/dynamics?start_date=20251201&end_date=20251203")
        assert response.status_code == 200
        assert response.json() == test_data
    finally:
        app.dependency_overrides = {}


def test_trading_results(mock_get_cache, test_data):

    async def mock_get_trades_results(
        limit: int = 5,
        oil_id: str = None,
        delivery_type_id: str = None,
        delivery_basis_id: str = None,
        db = None
    ):
        return test_data
    
    app.dependency_overrides = {
        get_trades_results: mock_get_trades_results,
        get_cache: lambda: mock_get_cache
    }

    try:
        response = client.get("/trading-results?limit=5")
        assert response.status_code == 200
        assert response.json() == test_data
    finally:
        app.dependency_overrides = {}