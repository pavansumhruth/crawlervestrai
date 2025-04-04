import asyncio
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv

from config import BASE_URL, CSS_SELECTOR, REQUIRED_KEYS
from utils.scraper_utils import fetch_and_process_stock, get_browser_config, get_llm_strategy
from utils.ai_insights import get_ai_insights

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

def run_async(coro):
    """Helper function to run an async coroutine synchronously."""
    return asyncio.run(coro)

async def scrape_stock(symbol: str) -> dict:
    """
    Asynchronously scrapes stock data for a given stock symbol.
    """
    browser_config = get_browser_config()
    llm_strategy = get_llm_strategy()
    session_id = "stock_scrape_session"
    seen_names = set()

    # Import AsyncWebCrawler here to avoid potential conflicts with Flask's event loop
    from crawl4ai import AsyncWebCrawler

    async with AsyncWebCrawler(config=browser_config) as crawler:
        stock_data, _ = await fetch_and_process_stock(
            crawler,
            stock_symbol=symbol,
            base_url=BASE_URL,
            css_selector=CSS_SELECTOR,
            llm_strategy=llm_strategy,
            session_id=session_id,
            required_keys=REQUIRED_KEYS,
            seen_names=seen_names,
        )
    return stock_data if stock_data else {"error": "Stock data not found."}

@app.route("/analyze-stock", methods=["POST"])
def analyze_stock():
    """
    Expects a JSON payload with:
    {
        "symbol": "AAPL"
    }
    and returns a JSON response containing the stock data along with AI insights.
    """
    data = request.get_json()
    if not data or "symbol" not in data:
        return jsonify({"error": "Missing 'symbol' parameter."}), 400

    symbol = data["symbol"].strip().upper()
    stock_data = run_async(scrape_stock(symbol))

    # If there's no error, generate AI insights
    if not stock_data.get("error"):
        insights = get_ai_insights(stock_data)
        stock_data["ai_insights"] = insights
    else:
        stock_data["ai_insights"] = "No insights available due to error in fetching stock data."

    return jsonify(stock_data)

@app.route("/")
def index():
    return "Welcome to the Financial Analysis API. Use /analyze-stock endpoint with a JSON payload."

if __name__ == "__main__":
    # Run Flask in debug mode on port 5000
    app.run(debug=True, port=5000)
# In this Flask application, we define two routes:
#       




                