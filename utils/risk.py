import numpy as np
import pandas as pd


def calculate_daily_returns(data):
    """
    Calculate daily returns.
    """

    returns = data["Close"].pct_change()

    return returns.dropna()


def calculate_volatility(data):
    """
    Annualized volatility.
    """

    returns = calculate_daily_returns(data)

    volatility = (
        returns.std() * np.sqrt(252)
    )

    return volatility


def calculate_sharpe_ratio(
    data,
    risk_free_rate=0.05
):
    """
    Calculate annualized Sharpe Ratio.
    """

    returns = calculate_daily_returns(data)

    excess_return = (
        returns.mean() * 252
    ) - risk_free_rate

    volatility = (
        returns.std() * np.sqrt(252)
    )

    if volatility == 0:
        return 0

    sharpe_ratio = (
        excess_return / volatility
    )

    return sharpe_ratio


def calculate_max_drawdown(data):
    """
    Calculate maximum drawdown.
    """

    cumulative_max = (
        data["Close"].cummax()
    )

    drawdown = (
        data["Close"] - cumulative_max
    ) / cumulative_max

    return drawdown.min()


def risk_level(volatility):
    """
    Categorize risk level.
    """

    if volatility < 0.15:
        return "Low Risk 🟢"

    elif volatility < 0.30:
        return "Medium Risk 🟡"

    else:
        return "High Risk 🔴"


def generate_risk_report(data):
    """
    Generate complete risk report.
    """

    volatility = calculate_volatility(data)

    sharpe_ratio = calculate_sharpe_ratio(data)

    max_drawdown = calculate_max_drawdown(data)

    return {
        "Volatility (%)": round(
            volatility * 100, 2
        ),
        "Sharpe Ratio": round(
            sharpe_ratio, 2
        ),
        "Max Drawdown (%)": round(
            max_drawdown * 100, 2
        ),
        "Risk Level": risk_level(
            volatility
        )
    }