from pydantic import BaseModel
from typing import Optional

class Stock(BaseModel):
    """
    Represents the financial data of a Stock.
    """
    name: str                         # Company name or ticker symbol
    price: float                      # Current stock price
    market_cap: Optional[str] = None  # Market capitalization (formatted string)
    pe_ratio: Optional[float] = None  # Price-to-Earnings ratio
    dividend_yield: Optional[float] = None  # Dividend yield percentage
    volume: Optional[int] = None      # Trading volume
    day_high: Optional[float] = None  # Day's high price
    day_low: Optional[float] = None   # Day's low price
    previous_close: Optional[float] = None  # Previous closing price
    description: Optional[str] = None  # Optional company description
    
