from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ErrorBody(BaseModel):
    code: int
    name: Optional[str]
    details: Optional[List[str]]


class JWTTokenResponse(BaseModel):
    accessToken: str
    refreshToken: str


class SymbolStats(BaseModel):
    symbol: str
    lastPrice: Optional[float]
    volume24h: Optional[float]
    price24Percentage: Optional[float]


class SymbolInfo(BaseModel):
    symbol: str
    marginAsset: str
    baseAsset: str
    pair: str
    quoteAsset: str
    status: str


class ServerTime(BaseModel):
    serverTime: int


class RateLimit(BaseModel):
    intervalNum: int
    limit: int
    interval: str
    rateLimitType: str


class ExchangeInformation(ServerTime):
    rateLimits: List[RateLimit]
    symbols: List[SymbolInfo]
    timezone: str


class OrderInfo(BaseModel):
    orderId: int
    clientOrderId: Optional[str]
    symbol: str
    type: str
    amount: float
    filled: float
    price: float
    side: str
    notionalValue: int
    placedAt: datetime


class AllOpenOrders(BaseModel):
    content: List[OrderInfo]
    totalPages: int
    totalElements: int
    size: int


class OrderBook(BaseModel):
    price: float
    size: float
    sum: float


class OrderBookInfo(BaseModel):
    ask: List[OrderBook]
    bid: List[OrderBook]


class OrderEvent(BaseModel):
    orderId: Optional[str]
    clientOrderId: Optional[str]
    symbol: Optional[str]
    amount: float
    price: Optional[float]
    filled: float
    averageExecutionPrice: Optional[float]
    type: str
    side: str
    status: str
    updatedAt: datetime


class PositionInfo(BaseModel):
    symbol: str
    marginMode: Optional[str]
    amount: float
    basePrice: float
    liquidationPrice: Optional[float]
    markPrice: Optional[float]
    upl: Optional[float]
    uplPercentage: Optional[int]
    lockedBalance: Optional[float]
    leverage: int


class OrderBalanceInfo(BaseModel):
    symbol: str
    lockedAsk: float
    lockedBid: float
    sumSizeAsk: float
    sumSizeBid: float


class AssetInfo(BaseModel):
    name: str
    deposited: Optional[float]
    margin: Optional[float]
    locked: Optional[float]
    isMargin: Optional[bool]


class AccountInfo(BaseModel):
    upl: float
    equity: float
    feeTierStructure: int
    feeTierDiscount: int
    tradeFeeAsset: str
    assets: List[AssetInfo]
    positions: List[PositionInfo]
    orders: List[OrderBalanceInfo]


class LeverageEvent(BaseModel):
    leverage: int


class SymbolRule(BaseModel):
    symbol: str
    limitOrderBuyPriceCap: float
    limitOrderSellPriceCap: float
    minTradeAmount: float
    minOrderAmount: float
    maxMarketNotionalOrder: float
    minOrderNotionalValue: float
