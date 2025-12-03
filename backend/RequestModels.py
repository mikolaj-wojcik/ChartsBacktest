from pydantic import BaseModel
from typing import Optional, Dict


class PriceBar(BaseModel):
    open: float
    high: float
    low: float
    close: float
    date: str

class StrategyToRunModel(BaseModel):
    strategy_name: str
    strategy_code: Optional[str] = None
    prices: list[PriceBar]
    params: dict
    min_commission: float
    commission_factor: float
    starting_balance: float
    metrics: list [str]


class StrategyModel(BaseModel):
    strategy_name: str
    strategy_code: Optional[str] = None
    #strategy_code: Optional[str] = None


