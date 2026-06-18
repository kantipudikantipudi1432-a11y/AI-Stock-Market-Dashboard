import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from ta.momentum import RSIIndicator

# Get stock symbol from user
ticker = input("Enter Stock Symbol (e.g., AAPL, TSLA, TCS.NS): ").upper()

try:
    print(f"\nFetching data for {ticker}...")

    # Download 1 year of stock data
    stock = yf.Ticker(ticker)
    data = stock.history(period="1y")

    if data.empty:
        print("Invalid stock symbol or no data available.")
        exit()

    # Moving Averages
    data["MA50"] = data["Close"].rolling(window=50).mean()
    data["MA200"] = data["Close"].rolling(window=200).mean()

    # RSI
    data["RSI"] = RSIIndicator(close=data["Close"]).rsi()

    # Latest values
    latest_close = data["Close"].iloc[-1]
    latest_rsi = data["RSI"].iloc[-1]

    print("\n===== STOCK ANALYSIS REPORT =====")
    print(f"Stock Symbol : {ticker}")
    print(f"Current Price: {latest_close:.2f}")
    print(f"52 Week High : {data['High'].max():.2f}")
    print(f"52 Week Low  : {data['Low'].min():.2f}")
    print(f"Average Volume: {int(data['Volume'].mean())}")

    print(f"\nRSI Value: {latest_rsi:.2f}")

    if latest_rsi > 70:
        print("Signal: OVERBOUGHT (Possible Sell Signal)")
    elif latest_rsi < 30:
        print("Signal: OVERSOLD (Possible Buy Signal)")
    else:
        print("Signal: NEUTRAL")

    # Save report
    data.to_csv("stock_report.csv")
    print("\nReport saved as stock_report.csv")

    # Plot Chart
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data["Close"], label="Close Price")
    plt.plot(data.index, data["MA50"], label="50-Day MA")
    plt.plot(data.index, data["MA200"], label="200-Day MA")

    plt.title(f"{ticker} Stock Analysis")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)

    plt.show()

except Exception as e:
    print("Error:", e)