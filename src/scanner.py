import csv
from report_generator import write_report
import json
from pathlib import Path

import pandas as pd

from data_fetcher import fetch_stock_data
from valuation import calculate_valuation


WATCHLIST_PATH = Path("data/watchlist.csv")
OUTPUT_CSV = Path("outputs/results.csv")
OUTPUT_JSON = Path("outputs/results.json")


def run_scan() -> None:
    rows = load_watchlist()
    results = []

    for row in rows:
        ticker = row["ticker"]
        manual_growth = row.get("manual_growth")

        print(f"Scanning {ticker}...")

        try:
            stock_data = fetch_stock_data(ticker, manual_growth)
            valuation = calculate_valuation(stock_data)
            write_report(stock_data, valuation)
            results.append(valuation.__dict__)
        except Exception as e:
            results.append({
                "ticker": ticker,
                "current_price": None,
                "eps": None,
                "pe_ratio": None,
                "manual_growth": manual_growth,
                "dividend_yield": None,
                "dividend_growth": None,
                "total_growth_used": None,
                "fair_value": None,
                "buy_price": None,
                "margin_of_safety": None,
                "qualifies": False,
                "reason": f"Error: {e}",
            })

    save_results(results)
    print_results(results)


def load_watchlist() -> list[dict]:
    rows = []

    with open(WATCHLIST_PATH, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            ticker = row.get("ticker")
            if not ticker:
                continue

            manual_growth = parse_float(row.get("manual_growth"))

            rows.append({
                "ticker": ticker.strip().upper(),
                "manual_growth": manual_growth,
            })

    return rows


def parse_float(value: str | None) -> float | None:
    if value is None or value.strip() == "":
        return None

    return float(value)


def save_results(results: list[dict]) -> None:
    OUTPUT_CSV.parent.mkdir(exist_ok=True)

    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_CSV, index=False)

    with open(OUTPUT_JSON, "w") as file:
        json.dump(results, file, indent=2)


def print_results(results: list[dict]) -> None:
    print("\n=== Stock Formula Agent Results ===\n")

    for result in results:
        print("\n" + "=" * 80)
        print(result["ticker"])
        print("=" * 80)

        print(f"Price: {result['current_price']}")
        print(f"EPS: {result['eps']}")
        print(f"PE: {result['pe_ratio']}")
        print(f"Dividend Yield: {result['dividend_yield']}%")
        print(f"Dividend Growth: {result['dividend_growth']}%")
        print(f"Expected Sustainable Growth: {result['expected_growth']}%")
        print(f"Growth Used: {result['total_growth_used']}%")
        print(f"Growth Source: {result.get('growth_source')}")
        print(f"Growth Reason: {result.get('growth_reason')}")
        print(f"Fair Value: {result['fair_value']}")
        print(f"Buy Price: {result['buy_price']}")
        print(f"Qualifies: {result['qualifies']}")
        print(f"Reason: {result['reason']}")