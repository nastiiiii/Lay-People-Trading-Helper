import yfinance as yf
import requests
import json

# Replace with your FastAPI base URL
BASE_URL = "http://127.0.0.1:8000/stocks/"

# List of stock tickers to fetch
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")  # last 1 year
    historical_prices = hist["Close"].dropna().tolist()

    info = stock.info

    return {
        "stock_symbol": ticker,
        "company_name": info.get("shortName", ticker),
        "sector": info.get("sector", "Unknown"),
        "historical_prices": historical_prices
    }

def post_to_api(stock_data):
    response = requests.post(BASE_URL, json=stock_data)
    if response.status_code == 200:
        print(f"✅ Uploaded: {stock_data['stock_symbol']}")
    else:
        print(f"❌ Failed: {stock_data['stock_symbol']} - {response.status_code}")
        print(response.text)

def main():
    for ticker in TICKERS:
        data = fetch_stock_data(ticker)
        post_to_api(data)

if __name__ == "__main__":
    main()
