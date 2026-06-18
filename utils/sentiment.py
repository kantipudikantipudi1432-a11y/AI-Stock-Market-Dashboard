from textblob import TextBlob
import feedparser


def get_news_headlines(stock_name, max_news=10):
    """
    Fetch latest news headlines using Google News RSS.
    """

    query = stock_name.replace(".NS", "")

    url = (
        f"https://news.google.com/rss/search?"
        f"q={query}+stock&hl=en-IN&gl=IN&ceid=IN:en"
    )

    feed = feedparser.parse(url)

    news_list = []

    for entry in feed.entries[:max_news]:

        news_list.append({
            "title": entry.title,
            "link": entry.link
        })

    return news_list


def analyze_sentiment(text):
    """
    Analyze sentiment of a headline.
    """

    analysis = TextBlob(text)

    polarity = analysis.sentiment.polarity

    if polarity > 0.1:
        sentiment = "Positive 🟢"

    elif polarity < -0.1:
        sentiment = "Negative 🔴"

    else:
        sentiment = "Neutral 🟡"

    return sentiment, polarity


def get_news_sentiment(stock_name):
    """
    Get sentiment analysis for latest news.
    """

    news = get_news_headlines(stock_name)

    results = []

    positive = 0
    neutral = 0
    negative = 0

    for item in news:

        sentiment, polarity = analyze_sentiment(
            item["title"]
        )

        if "Positive" in sentiment:
            positive += 1

        elif "Negative" in sentiment:
            negative += 1

        else:
            neutral += 1

        results.append({
            "Headline": item["title"],
            "Sentiment": sentiment,
            "Polarity": round(polarity, 2),
            "Link": item["link"]
        })

    summary = {
        "Positive": positive,
        "Neutral": neutral,
        "Negative": negative
    }

    return results, summary


def overall_market_sentiment(summary):
    """
    Determine overall sentiment.
    """

    positive = summary["Positive"]
    negative = summary["Negative"]

    if positive > negative:
        return "Bullish 🟢"

    elif negative > positive:
        return "Bearish 🔴"

    else:
        return "Neutral 🟡"