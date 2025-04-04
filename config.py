# config.py

# Base URL for the stock page on Yahoo Finance. You could also leave this dynamic.
BASE_URL = "https://finance.yahoo.com/quote/{}/"

# CSS selector for extracting the regular market price from Yahoo Finance.
CSS_SELECTOR = 'fin-streamer[data-field="regularMarketPrice"]'

# List of required keys for our Stock data model.
REQUIRED_KEYS = [
    "name",           # Company name or ticker symbol
    "price",          # Current stock price
    "market_cap",     # Market capitalization
    "pe_ratio",       # Price-to-Earnings ratio
    "dividend_yield", # Dividend yield percentage
    "volume",         # Trading volume
    "day_high",       # Highest price of the day
    "day_low",        # Lowest price of the day
    "previous_close", # Previous closing price
    "description"     # Brief description of the company/stock
]
YAHOO_DATA_FIELDS = {
    "regularMarketOpen": "open_price",
    "regularMarketPrice": "current_price",
    "regularMarketPreviousClose": "previous_close",
    "regularMarketDayHigh": "day_high",
    "regularMarketDayLow": "day_low",
    "regularMarketVolume": "volume",
    "regularMarketChange": "change",
    "regularMarketChangePercent": "change_percent"
}
