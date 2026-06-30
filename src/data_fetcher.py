import yfinance as yf

from models import StockData


def fetch_stock_data(ticker: str, manual_growth: float | None = None) -> StockData:
    stock = yf.Ticker(ticker)
    info = stock.info

    current_price = info.get("currentPrice") or info.get("regularMarketPrice")
    eps = info.get("trailingEps")
    pe_ratio = info.get("trailingPE")
    market_cap = info.get("marketCap")

    dividend_yield = info.get("trailingAnnualDividendYield")

    if dividend_yield is None:
        dividend_rate = info.get("dividendRate")
        if dividend_rate is not None and current_price:
            dividend_yield = dividend_rate / current_price

    dividend_growth, dividend_history, dividend_growth_rates = calculate_dividend_growth(stock)

    auto_growth, growth_source, growth_reason = calculate_auto_growth(stock)

    return StockData(
        ticker=ticker,
        current_price=current_price,
        eps=eps,
        pe_ratio=pe_ratio,
        expected_growth=auto_growth if auto_growth is not None else manual_growth,
        growth_estimate_source=growth_source,
        growth_estimate_reason=growth_reason,
        dividend_yield=dividend_yield,
        dividend_growth=dividend_growth,
        market_cap=market_cap,
        dividend_history=dividend_history,
        dividend_growth_rates=dividend_growth_rates,
    )


def calculate_dividend_growth(stock: yf.Ticker) -> tuple[float | None, dict[int, float], dict[str, float]]:
    dividends = stock.dividends

    if dividends is None or dividends.empty:
        return None, {}, {}

    annual_dividends = dividends.groupby(dividends.index.year).sum().tail(10)
    from datetime import datetime

    current_year = datetime.now().year

    if current_year in annual_dividends.index:
       annual_dividends = annual_dividends.drop(current_year)

    # Fill missing years with 0 so dividend suspensions are visible.
    start_year = int(annual_dividends.index.min())
    end_year = int(annual_dividends.index.max())
    full_years = range(start_year, end_year + 1)
    annual_dividends = annual_dividends.reindex(full_years, fill_value=0)

    if len(annual_dividends) < 3:
        return None, annual_dividends.to_dict(), {}

    # If any year has zero dividends, treat dividend history as unreliable.
    # We still show the dividend history, but do not use dividend growth.
    if (annual_dividends == 0).any():
        return None, annual_dividends.to_dict(), {}

    growth_rates = annual_dividends.pct_change().dropna()

    # Remove extreme one-off changes.
    growth_rates = growth_rates[
        (growth_rates > -0.80) & (growth_rates < 1.00)
    ]

    if growth_rates.empty:
        return None, annual_dividends.to_dict(), {}

    growth_rate_dict = {
        f"{int(year - 1)}->{int(year)}": float(rate)
        for year, rate in growth_rates.items()
    }

    return float(growth_rates.mean()), annual_dividends.to_dict(), growth_rate_dict


def calculate_auto_growth(stock: yf.Ticker) -> tuple[float | None, str, str]:
    info = stock.info

    growth_fields = {
        "Yahoo earningsGrowth": info.get("earningsGrowth"),
        "Yahoo revenueGrowth": info.get("revenueGrowth"),
        "Yahoo earningsQuarterlyGrowth": info.get("earningsQuarterlyGrowth"),
    }

    for source, value in growth_fields.items():
        if value is None:
            continue

        try:
            value = float(value)
        except Exception:
            continue

        if 0 <= value <= 0.35:
            return value, source, "Yahoo growth estimate available and within accepted range."

    return None, "watchlist.csv", "Yahoo growth estimate unavailable or rejected, so watchlist value was used."


def calculate_revenue_cagr(stock: yf.Ticker) -> float | None:
    try:
        income_stmt = stock.income_stmt

        if income_stmt is None or income_stmt.empty:
            return None

        if "Total Revenue" not in income_stmt.index:
            return None

        revenue_series = income_stmt.loc["Total Revenue"].dropna()

        if len(revenue_series) < 2:
            return None

        latest = float(revenue_series.iloc[0])
        earliest = float(revenue_series.iloc[-1])
        years = len(revenue_series) - 1

        if latest <= 0 or earliest <= 0 or years <= 0:
            return None

        return (latest / earliest) ** (1 / years) - 1

    except Exception:
        return None