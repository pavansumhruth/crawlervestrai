import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL =  "https://api.groq.com/openai/v1/chat/completions"
               

def get_ai_insights(stock_data):
    """
    Sends stock data to Groq AI for insights.
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Analyze the following stock data and provide financial insights:

    - Name: {stock_data.get('name', 'N/A')}
    - Price: {stock_data.get('price', 'N/A')}
    - P/E Ratio: {stock_data.get('pe_ratio', 'N/A')}
    - Market Cap: {stock_data.get('market_cap', 'N/A')}
    - Dividend Yield: {stock_data.get('dividend_yield', 'N/A')}
    - Day High: {stock_data.get('day_high', 'N/A')}
    - Day Low: {stock_data.get('day_low', 'N/A')}
    - Volume: {stock_data.get('volume', 'N/A')}

    Based on this data, provide an analysis of the stock’s performance and investment potential.
    """

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a financial analyst."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    
    except requests.exceptions.RequestException as e:
        return f"Error calling Groq API: {e}"
