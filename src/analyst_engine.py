import yfinance as yf


def get_yahoo_growth_fields(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "earningsGrowth": info.get("earningsGrowth"),
        "revenueGrowth": info.get("revenueGrowth"),
        "earningsQuarterlyGrowth": info.get("earningsQuarterlyGrowth"),
        "recommendationMean": info.get("recommendationMean"),
        "recommendationKey": info.get("recommendationKey"),
        "numberOfAnalystOpinions": info.get("numberOfAnalystOpinions"),
        "targetMeanPrice": info.get("targetMeanPrice"),
        "targetHighPrice": info.get("targetHighPrice"),
        "targetLowPrice": info.get("targetLowPrice"),
    }


def print_analyst_debug(ticker: str) -> None:
    fields = get_yahoo_growth_fields(ticker)

    print("\n" + "=" * 80)
    print(f"{ticker} ANALYST / YAHOO DATA")
    print("=" * 80)

    for key, value in fields.items():
        print(f"{key}: {value}")