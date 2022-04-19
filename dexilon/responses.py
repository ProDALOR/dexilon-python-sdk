from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class AvailableSymbol(BaseModel):

    symbol: str
    isFavorite: bool = False
    lastPrice: float = None
    volume: float = None
    price24Percentage: float = None


class OrderBookPosition(BaseModel):
    price: float
    size: float
    sum: float


class OrderBookInfo(BaseModel):

    ask: List[OrderBookPosition]
    bid: List[OrderBookPosition]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MarginData(BaseModel):

    margin: float
    upl: float
    equity: float
    lockedBalanceForOpenOrders: float


class OrderInfo(BaseModel):
    id: str
    type: str
    amount: float
    price: float
    side: str
    placedAt: datetime


class OrdersBySymbols(BaseModel):

    symbol: str
    orders: List[OrderInfo]


class FullOrderInfo(BaseModel):
    symbol: str
    orderId: str
    price: float
    amount: float
    filledAmount: float
    avgPrice: float
    type: str
    side: str
    status: str
