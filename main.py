# import asyncio
# import json
# from crawl4ai import AsyncWebCrawler
# from dotenv import load_dotenv

# from config import BASE_URL, CSS_SELECTOR, REQUIRED_KEYS
# from utils.ai_insights import get_ai_insights
# from utils.scraper_utils import fetch_and_process_stock, get_browser_config, get_llm_strategy

# load_dotenv()

# async def scrape_stock(symbol):
#     """
#     Scrape stock data for a specific stock symbol.
#     """
#     # Initialize configurations for browser and LLM extraction
#     browser_config = get_browser_config()
#     llm_strategy = get_llm_strategy()
#     session_id = "stock_scrape_session"
#     seen_names = set()

#     # Start the async web crawler
#     async with AsyncWebCrawler(config=browser_config) as crawler:
#         # Note: fetch_and_process_stock returns a tuple (stock_data, flag)
#         stock_data, _ = await fetch_and_process_stock(
#             crawler,
#             stock_symbol=symbol,
#             base_url=BASE_URL,
#             css_selector=CSS_SELECTOR,
#             llm_strategy=llm_strategy,
#             session_id=session_id,
#             required_keys=REQUIRED_KEYS,
#             seen_names=seen_names,
#         )

#     return stock_data if stock_data else {"error": "Stock data not found."}

# async def main():
#     """
#     Entry point to scrape a specific stock.
#     """
#     symbol = input("Enter stock symbol (e.g., AAPL, TSLA): ").strip().upper()
#     stock_data = await scrape_stock(symbol)
#     if "error" not in stock_data:
#         insights = get_ai_insights(stock_data)
#         # Update the stock data with AI insights
#         stock_data["ai_insights"] = insights
#     else:
#         stock_data["ai_insights"] = "No insights available due to error in fetching stock data."
    
#     # Print output in JSON format
#     print(json.dumps(stock_data, indent=4))

# if __name__ == "__main__":
#     asyncio.run(main())


import argparse
import asyncio
import json
from utils.scraper_utils import scrape_stock
from utils.ai_insights import get_ai_insights

async def main(symbols):
    """
    Fetch stock data for multiple symbols and generate AI insights.
    """
    results = []

    for symbol in symbols:
        symbol = symbol.strip().upper()
        print(f"Fetching data for {symbol}...")

        try:
            stock_data = await scrape_stock(symbol)
            if "error" not in stock_data:
                stock_data["ai_insights"] = get_ai_insights(stock_data)
            results.append(stock_data)
            print(json.dumps(stock_data, indent=4))
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch stock data and AI insights.")
    parser.add_argument("symbols", nargs="*", help="Stock symbols (e.g., AAPL TSLA)")
    args = parser.parse_args()

    if args.symbols:
        stock_symbols = args.symbols
    else:
        stock_symbols = input("Enter stock symbols (comma-separated, e.g., AAPL, TSLA): ").split(",")

    asyncio.run(main(stock_symbols))
