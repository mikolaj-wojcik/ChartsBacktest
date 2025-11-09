from pydantic import BaseModel
from typing import Optional

class StrategyToRunModel(BaseModel):
    strategy_name: str
    strategy_code: Optional[str] = None
    params: dict
    statistics: list[str]
    min_commission: float
    commission_factor: float
    starting_balance: float

class StrategyModel(BaseModel):
    strategy_name: str
    strategy_code: Optional[str] = None
