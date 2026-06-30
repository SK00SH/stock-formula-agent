from models import GrowthResult
import yfinance as yf


def calculate_cagr(first: float, last: float, years: int):
    """
    Calculates Compound Annual Growth Rate (CAGR).
    Returns None if calculation is invalid.
    """

    if first is None or last is None:
        return None

    if first <= 0 or last <= 0:
        return None

    if years <= 0:
        return None

    return (last / first) ** (1 / years) - 1


def get_series_values(series):
    """
    Converts a financial series into a clean list of floats.
    Newest year is first from yfinance,
    so we reverse it into chronological order.
    """

    values = []

    for value in reversed(series.dropna().tolist()):
        try:
            values.append(float(value))
        except Exception:
            pass

    return values


def revenue_cagr(stock):

    try:

        financials = stock.income_stmt

        revenue = financials.loc["Total Revenue"]

        values = get_series_values(revenue)

        if len(values) < 2:
            return None

        return calculate_cagr(
            values[0],
            values[-1],
            len(values) - 1,
        )

    except Exception:

        return None


def eps_cagr(stock):

    try:

        financials = stock.income_stmt

        eps = financials.loc["Basic EPS"]

        values = get_series_values(eps)

        if len(values) < 2:
            return None

        return calculate_cagr(
            values[0],
            values[-1],
            len(values) - 1,
        )

    except Exception:

        return None
def calculate_growth(stock):

    revenue = revenue_cagr(stock)

    eps = eps_cagr(stock)

    # FCF comes next version
    fcf = None

    values = []

    if revenue is not None:
        values.append(revenue)

    if eps is not None:
        values.append(eps)

    if values:
        suggested = sum(values) / len(values)
    else:
        suggested = None

    return GrowthResult(
        revenue_cagr=revenue,
        eps_cagr=eps,
        fcf_cagr=fcf,
        dividend_growth=None,
        dividend_reliable=False,
        suggested_growth=suggested,
        confidence="Low",
        reason="Prototype Growth Engine",
    )