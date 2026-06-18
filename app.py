import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import feedparser

from models.lstm_model import predict_next_price
from textblob import TextBlob
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="AI Stock Dashboard V4",
    layout="wide"
)

st.title("📈 AI Stock Market Dashboard V4")

# -----------------------------
# NEWS SENTIMENT FUNCTION
# -----------------------------

def get_news_sentiment(stock):

    url = f"https://news.google.com/rss/search?q={stock}+stock"

    feed = feedparser.parse(url)

    headlines = []
    sentiments = []

    for entry in feed.entries[:10]:

        headline = entry.title

        headlines.append(headline)

        score = TextBlob(
            headline
        ).sentiment.polarity

        sentiments.append(score)

    avg_sentiment = (
        np.mean(sentiments)
        if sentiments else 0
    )

    return headlines, avg_sentiment

# -----------------------------
# SIDEBAR
# -----------------------------

ticker = st.sidebar.text_input(
    "Stock Symbol",
    "TCS.NS"
)

st.sidebar.header("Portfolio")

buy_price = st.sidebar.number_input(
    "Buy Price",
    min_value=1.0,
    value=1000.0
)

shares = st.sidebar.number_input(
    "Number of Shares",
    min_value=1,
    value=10
)

try:

    # -----------------------------
    # DOWNLOAD DATA
    # -----------------------------

    data = yf.download(
        ticker,
        period="1y",
        progress=False,
        auto_adjust=False
    )

    if data.empty:
        st.error("No stock data found")
        st.stop()

    # Fix MultiIndex issue

    if isinstance(
        data.columns,
        pd.MultiIndex
    ):
        data.columns = (
            data.columns.get_level_values(0)
        )

    # -----------------------------
    # INDICATORS
    # -----------------------------

    data["MA50"] = (
        data["Close"]
        .rolling(50)
        .mean()
    )

    data["MA200"] = (
        data["Close"]
        .rolling(200)
        .mean()
    )

    data["RSI"] = RSIIndicator(
        close=data["Close"]
    ).rsi()

    macd = MACD(data["Close"])

    data["MACD"] = macd.macd()

    data["MACD_SIGNAL"] = (
        macd.macd_signal()
    )

    bb = BollingerBands(
        data["Close"]
    )

    data["BB_HIGH"] = (
        bb.bollinger_hband()
    )

    data["BB_LOW"] = (
        bb.bollinger_lband()
    )

    latest_price = float(
        data["Close"].iloc[-1]
    )

    # -----------------------------
    # SUMMARY
    # -----------------------------

    st.subheader("📊 Stock Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Current Price",
        f"₹{latest_price:.2f}"
    )

    c2.metric(
        "52 Week High",
        f"₹{data['High'].max():.2f}"
    )

    c3.metric(
        "52 Week Low",
        f"₹{data['Low'].min():.2f}"
    )

    # -----------------------------
    # PORTFOLIO
    # -----------------------------

    investment = (
        buy_price * shares
    )

    current_value = (
        latest_price * shares
    )

    profit_loss = (
        current_value - investment
    )

    st.subheader(
        "💼 Portfolio Tracker"
    )

    p1, p2, p3 = st.columns(3)

    p1.metric(
        "Investment",
        f"₹{investment:,.2f}"
    )

    p2.metric(
        "Current Value",
        f"₹{current_value:,.2f}"
    )

    p3.metric(
        "Profit/Loss",
        f"₹{profit_loss:,.2f}"
    )

    # -----------------------------
    # RISK ANALYSIS
    # -----------------------------

    returns = (
        data["Close"]
        .pct_change()
        .dropna()
    )

    volatility = (
        returns.std()
        * np.sqrt(252)
    )

    sharpe_ratio = (
        (returns.mean())
        / returns.std()
    ) * np.sqrt(252)

    st.subheader(
        "⚠️ Risk Analysis"
    )

    r1, r2 = st.columns(2)

    r1.metric(
        "Volatility",
        f"{volatility:.2f}"
    )

    r2.metric(
        "Sharpe Ratio",
        f"{sharpe_ratio:.2f}"
    )

    # -----------------------------
    # CHARTS
    # -----------------------------

    st.subheader(
        "🕯️ Candlestick Chart"
    )

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=data.index,
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"]
            )
        ]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "📈 Moving Averages"
    )

    st.line_chart(
        data[
            [
                "Close",
                "MA50",
                "MA200"
            ]
        ]
    )

    st.subheader(
        "📊 RSI Indicator"
    )

    st.line_chart(
        data["RSI"]
    )

    st.subheader(
        "📉 MACD Indicator"
    )

    st.line_chart(
        data[
            [
                "MACD",
                "MACD_SIGNAL"
            ]
        ]
    )

    st.subheader(
        "📈 Bollinger Bands"
    )

    st.line_chart(
        data[
            [
                "Close",
                "BB_HIGH",
                "BB_LOW"
            ]
        ]
    )

    # -----------------------------
    # NEWS SENTIMENT
    # -----------------------------

    st.subheader(
        "📰 News Sentiment"
    )

    headlines, sentiment_score = (
        get_news_sentiment(
            ticker
        )
    )

    for news in headlines:
        st.write("•", news)

    st.metric(
        "Sentiment Score",
        round(
            sentiment_score,
            2
        )
    )

    # -----------------------------
    # AI SCORE
    # -----------------------------

    latest_rsi = float(
        data["RSI"]
        .dropna()
        .iloc[-1]
    )

    score = 50

    if latest_rsi < 30:
        score += 20

    elif latest_rsi > 70:
        score -= 20

    if sentiment_score > 0:
        score += 15
    else:
        score -= 15

    if sharpe_ratio > 1:
        score += 15

    score = max(
        0,
        min(score, 100)
    )

    st.subheader(
        "🤖 AI Stock Score"
    )

    st.progress(score)

    st.metric(
        "Score",
        f"{score}/100"
    )

    st.subheader(
        "🤖 Recommendation"
    )

    if score >= 75:
        st.success(
            "STRONG BUY 🟢"
        )

    elif score >= 55:
        st.info(
            "BUY 🟢"
        )

    elif score >= 40:
        st.warning(
            "HOLD 🟡"
        )

    else:
        st.error(
            "SELL 🔴"
        )

    # -----------------------------
    # DATA TABLE
    # -----------------------------
    
    # -----------------------------
# AI PRICE PREDICTION
# -----------------------------
    # -----------------------------
    # AI PRICE PREDICTION
    # -----------------------------

    st.subheader("🔮 AI Price Prediction")

    predicted_price = predict_next_price(data)

    change_pct = (
        (predicted_price - latest_price)
        / latest_price
    ) * 100

    c1, c2 = st.columns(2)

    c1.metric(
        "Current Price",
        f"₹{latest_price:.2f}"
    )

    c2.metric(
        "Predicted Price",
        f"₹{predicted_price:.2f}",
        f"{change_pct:.2f}%"
    )

    if predicted_price > latest_price:
        st.success("AI predicts upward movement 📈")
    else:
        st.warning("AI predicts downward movement 📉")

    st.subheader("📋 Recent Data")

    st.dataframe(
        data.tail(10)
    )

    csv = (
        data.to_csv()
        .encode("utf-8")
    )

    st.download_button(
        "⬇️ Download CSV Report",
        csv,
        file_name=f"{ticker}_report.csv",
        mime="text/csv"
    )
except Exception as e:

    st.error(
        f"Error: {str(e)}"
    )