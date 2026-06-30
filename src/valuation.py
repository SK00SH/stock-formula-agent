from models import StockData, ValuationResult


DISCOUNT_RATE = 0.15
FORECAST_YEARS = 10
MARGIN_OF_SAFETY = 0.5
MEANINGFUL_DIVIDEND_YIELD = 0.0025  # 0.25%


def calculate_valuation(stock: StockData) -> ValuationResult:
    if stock.current_price is None or stock.current_price <= 0:
        return _fail(stock, "Missing or invalid current price")

    if stock.eps is None or stock.eps <= 0:
        return _fail(stock, "Missing or invalid EPS")

    if stock.pe_ratio is None or stock.pe_ratio <= 0:
        return _fail(stock, "Missing or invalid PE ratio")

    growth, growth_source, growth_reason = choose_growth(stock)

    if growth is None:
        return _fail(stock, "Missing growth assumption")

    future_price = stock.eps * ((1 + growth) ** FORECAST_YEARS) * stock.pe_ratio
    fair_value = future_price / ((1 + DISCOUNT_RATE) ** FORECAST_YEARS)
    buy_price = fair_value * MARGIN_OF_SAFETY
    margin_of_safety = (fair_value - stock.current_price) / fair_value
    qualifies = stock.current_price <= buy_price

    return ValuationResult(
        ticker=stock.ticker,
        current_price=round(stock.current_price, 2),
        eps=round(stock.eps, 2),
        pe_ratio=round(stock.pe_ratio, 2),
        expected_growth=_round_pct(stock.expected_growth),
        dividend_yield=_round_pct(stock.dividend_yield),
        dividend_growth=_round_pct(stock.dividend_growth),
        total_growth_used=round(growth * 100, 2),
        fair_value=round(fair_value, 2),
        buy_price=round(buy_price, 2),
        margin_of_safety=round(margin_of_safety * 100, 2),
        growth_source=growth_source,
        growth_reason=growth_reason,
        qualifies=qualifies,
        reason="Current price is below buy price" if qualifies else "Current price is above buy price",
        dividend_history=stock.dividend_history,
        dividend_growth_rates=stock.dividend_growth_rates,
    )


def choose_growth(stock: StockData) -> tuple[float | None, str, str]:
    if (
        stock.dividend_yield is not None
        and stock.dividend_growth is not None
        and stock.dividend_yield >= MEANINGFUL_DIVIDEND_YIELD
    ):
        return (
            stock.dividend_yield + stock.dividend_growth,
            "Dividend Formula",
            "Reliable dividend history and dividend yield is meaningful.",
        )

    if stock.expected_growth is not None:
        return (
           stock.expected_growth,
           stock.growth_estimate_source,
           stock.growth_estimate_reason,
       )

    return None, "Missing", "No reliable dividend growth or expected growth estimate available."


def _fail(stock: StockData, reason: str) -> ValuationResult:
    return ValuationResult(
        ticker=stock.ticker,
        current_price=stock.current_price,
        eps=stock.eps,
        pe_ratio=stock.pe_ratio,
        expected_growth=_round_pct(stock.expected_growth),
        dividend_yield=_round_pct(stock.dividend_yield),
        dividend_growth=_round_pct(stock.dividend_growth),
        total_growth_used=None,
        fair_value=None,
        buy_price=None,
        margin_of_safety=None,
        growth_source="N/A",
        growth_reason="N/A",
        qualifies=False,
        reason=reason,
        dividend_history=stock.dividend_history,
        dividend_growth_rates=stock.dividend_growth_rates,
    )


def _round_pct(value: float | None) -> float | None:
    if value is None:
        return None
    return round(value * 100, 2)