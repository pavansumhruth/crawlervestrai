from typing import Set, List, Dict

def is_duplicate_stock(stock_name: str, seen_names: Set[str]) -> bool:
    """
    Check if a stock with the given name has already been processed.
    """
    return stock_name in seen_names

def is_complete_stock(stock: Dict, required_keys: List[str]) -> bool:
    """
    Verify that the stock entry contains all the required keys.
    """
    return all(key in stock for key in required_keys)
