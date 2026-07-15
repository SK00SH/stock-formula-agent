import yfinance as yf


def calculate_cagr(first: float, last: float, years: int):
    if first is None or last is None:
        return None
    if first <= 0 or last <= 0:
        return None
    if years <= 0:
        return None

    return (last / first) ** (1 / years) - 1


def clean_series(series):
    values = []

    for value in reversed(series.dropna().tolist()):
        try:
            values.append(float(value))
        except Exception:
            pass

    return values


def get_income_statement(stock: yf.Ticker):
    try:
        return stock.income_stmt
    except Exception:
        return None


def revenue_cagr(ticker: str):
    stock = yf.Ticker(ticker)
    income = get_income_statement(stock)

    if income is None or income.empty:
        return None

    if "Total Revenue" not in income.index:
        return None

    values = clean_series(income.loc["Total Revenue"])

    if len(values) < 2:
        return None

    return calculate_cagr(values[0], values[-1], len(values) - 1)


def eps_cagr(ticker: str):
    stock = yf.Ticker(ticker)
    income = get_income_statement(stock)

    if income is None or income.empty:
        return None

    if "Basic EPS" not in income.index:
        return None

    values = clean_series(income.loc["Basic EPS"])

    if len(values) < 2:
        return None

    return calculate_cagr(values[0], values[-1], len(values) - 1)

def fcf_cagr(ticker: str):
    stock = yf.Ticker(ticker)

    try:
        cashflow = stock.cashflow
    except Exception:
        return None

    if cashflow is None or cashflow.empty:
        return None

    if "Free Cash Flow" not in cashflow.index:
        return None

    values = clean_series(cashflow.loc["Free Cash Flow"])

    if len(values) < 2:
        return None
    return calculate_cagr(values[0], values[-1], len(values) - 1)

def historical_growth_summary(ticker: str) -> dict:
    revenue = revenue_cagr(ticker)
    eps = eps_cagr(ticker)
    fcf = fcf_cagr(ticker)

    available = [
        x for x in [revenue, eps, fcf]
        if x is not None
    ]

    if available:
        suggested = sum(available) / len(available)
    else:
        suggested = None

    return {
        "revenue_cagr": revenue,
        "eps_cagr": eps,
        "fcf_cagr": fcf,
        "suggested_historical_growth": suggested,
    }
