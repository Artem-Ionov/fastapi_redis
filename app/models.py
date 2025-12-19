from pydantic import BaseModel


class TradingResults(BaseModel):

    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: int
    total: float
    count: int
    date: str

    class Config:
        from_attributes = True  # Обеспечивает взаимодействие с моделями SQLalchemy
