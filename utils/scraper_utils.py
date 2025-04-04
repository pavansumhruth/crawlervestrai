import json
import os
from typing import List, Set, Tuple

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    LLMExtractionStrategy,
)

from models.Stock import Stock
from utils.data_utils import is_complete_stock, is_duplicate_stock


def get_browser_config() -> BrowserConfig:
    """
    Returns the browser configuration for the crawler.

    Returns:
        BrowserConfig: The configuration settings for the browser.
    """
    return BrowserConfig(
        browser_type="chromium",  # Type of browser to simulate
        headless=True,            # Running in headless mode (no GUI)
        verbose=True,             # Enable verbose logging
    )


def get_llm_strategy() -> LLMExtractionStrategy:
    """
    Returns the configuration for the language model extraction strategy.

    Returns:
        LLMExtractionStrategy: The settings for extracting stock data using LLM.
    """
    return LLMExtractionStrategy(
        provider="groq/deepseek-r1-distill-llama-70b",  # Adjust provider as needed
        api_token=os.getenv("GROQ_API_KEY"),  # API token for authentication
        schema=Stock.model_json_schema(),     # JSON schema based on the Stock model
        extraction_type="schema",             # Type of extraction to perform
        instruction=(
            "Extract all stock objects with 'name', 'price', 'market_cap', 'pe_ratio', "
            "'dividend_yield', 'volume', 'day_high', 'day_low', 'previous_close', "
            "and a brief description of the stock from the following content."
        ),
        input_format="markdown",  # Format of the input content
        verbose=True,             # Enable verbose logging
    )


async def check_no_results(
    crawler: AsyncWebCrawler,
    url: str,
    session_id: str,
) -> bool:
    """
    Checks if the "No Results Found" message is present on the page.

    Args:
        crawler (AsyncWebCrawler): The web crawler instance.
        url (str): The URL to check.
        session_id (str): The session identifier.

    Returns:
        bool: True if a "No Results Found" message is found, False otherwise.
    """
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            session_id=session_id,
        ),
    )

    if result.success and "No Results Found" in result.cleaned_html:
        return True

    if not result.success:
        print(f"Error during no-results check: {result.error_message}")

    return False


async def fetch_and_process_stock(
    crawler: AsyncWebCrawler,
    stock_symbol: str,
    base_url: str,
    css_selector: str,
    llm_strategy: LLMExtractionStrategy,
    session_id: str,
    required_keys: List[str],
    seen_names: Set[str],
) -> Tuple[dict, bool]:
    """
    Fetches and processes data for a single stock.

    Args:
        crawler (AsyncWebCrawler): The web crawler instance.
        stock_symbol (str): The stock symbol to fetch.
        base_url (str): The base URL of the stock website.
        css_selector (str): The CSS selector to target the relevant content.
        llm_strategy (LLMExtractionStrategy): The LLM extraction strategy.
        session_id (str): The session identifier.
        required_keys (List[str]): List of required keys in the stock data.
        seen_names (Set[str]): Set of stock names that have already been processed.

    Returns:
        Tuple[dict, bool]:
            - dict: The processed stock data.
            - bool: A flag indicating if the "No Results Found" message was encountered.
    """
    url = f"{base_url.format(stock_symbol)}"  # Construct stock-specific URL
    print(f"Fetching stock data for {stock_symbol}...")

    # Check if stock page is empty or invalid
    no_results = await check_no_results(crawler, url, session_id)
    if no_results:
        return {}, True  # No results found, stop processing

    # Fetch stock page with the LLM extraction strategy
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,  # Do not use cached data
            extraction_strategy=llm_strategy,  # Use LLM to extract data
            css_selector=css_selector,         # Target specific content on the page
            session_id=session_id,             # Unique session ID for the crawl
        ),
    )

    if not (result.success and result.extracted_content):
        print(f"Error fetching stock data for {stock_symbol}: {result.error_message}")
        return {}, False

    # Parse the extracted JSON content
    extracted_data = json.loads(result.extracted_content)
    if not extracted_data:
        print(f"No stock data found for {stock_symbol}.")
        return {}, False

    print("Extracted data:", extracted_data)

    # Validate and filter extracted stock data
    stock_data = extracted_data[0] if isinstance(extracted_data, list) else extracted_data

    if not is_complete_stock(stock_data, required_keys):
        print(f"Stock data for {stock_symbol} is incomplete. Skipping.")
        return {}, False

    if is_duplicate_stock(stock_data["name"], seen_names):
        print(f"Duplicate stock '{stock_data['name']}' found. Skipping.")
        return {}, False

    seen_names.add(stock_data["name"])
    print(f"Stock data successfully extracted for {stock_symbol}: {stock_data}")

    return stock_data, False  # Successfully fetched stock data
