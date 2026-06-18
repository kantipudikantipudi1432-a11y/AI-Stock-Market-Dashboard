import pandas as pd


def calculate_portfolio_value(current_price, shares):
    """
    Calculate current portfolio value.
    """

    return current_price * shares


def calculate_profit_loss(
    buy_price,
    current_price,
    shares
):
    """
    Calculate profit or loss.
    """

    return (current_price - buy_price) * shares


def calculate_return_percentage(
    buy_price,
    current_price
):
    """
    Calculate percentage return.
    """

    return (
        (current_price - buy_price)
        / buy_price
    ) * 100


def portfolio_summary(
    stock_name,
    buy_price,
    current_price,
    shares
):
    """
    Generate portfolio summary.
    """

    investment = buy_price * shares

    current_value = (
        current_price * shares
    )

    profit_loss = (
        current_value - investment
    )

    return_pct = (
        profit_loss / investment
    ) * 100

    return {
        "Stock": stock_name,
        "Shares": shares,
        "Buy Price": round(buy_price, 2),
        "Current Price": round(current_price, 2),
        "Investment": round(investment, 2),
        "Current Value": round(current_value, 2),
        "Profit/Loss": round(profit_loss, 2),
        "Return %": round(return_pct, 2)
    }


def create_portfolio_dataframe(
    portfolio_list
):
    """
    Convert portfolio records into DataFrame.
    """

    return pd.DataFrame(
        portfolio_list
    )