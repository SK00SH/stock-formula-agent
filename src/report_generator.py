from pathlib import Path
from historical_growth_engine import historical_growth_summary
OUTPUT_FOLDER = Path("outputs")


def pct(value):
    if value is None:
        return "N/A"

    return f"{value * 100:.2f}%"


def write_report(stock, valuation):

    OUTPUT_FOLDER.mkdir(exist_ok=True)

    filename = OUTPUT_FOLDER / f"{stock.ticker}_report.txt"
    historical_growth = historical_growth_summary(stock.ticker)


    with open(filename, "w", encoding="utf-8") as f:

        f.write("=" * 70 + "\n")
        f.write(f"{stock.ticker} RESEARCH REPORT\n")
        f.write("=" * 70 + "\n\n")

        f.write("LIVE MARKET DATA\n")
        f.write("------------------------------\n")

        f.write(f"Current Price : {stock.current_price}\n")
        f.write(f"EPS           : {stock.eps}\n")
        f.write(f"PE            : {stock.pe_ratio}\n")
        f.write(f"Dividend Yield: {pct(stock.dividend_yield)}\n")
        f.write(f"Market Cap    : {stock.market_cap}\n\n")

        f.write("DIVIDEND HISTORY\n")
        f.write("------------------------------\n")

        if stock.dividend_history:

            for year, dividend in stock.dividend_history.items():
                f.write(f"{year}: {dividend}\n")

        else:

            f.write("No dividend history\n")

        f.write("\n")

        f.write("DIVIDEND GROWTH\n")
        f.write("------------------------------\n")

        if stock.dividend_growth_rates:

            for period, growth in stock.dividend_growth_rates.items():
                f.write(f"{period}: {growth * 100:.2f}%\n")

        else:

            f.write("Unavailable\n")

        f.write("\n")
        f.write("HISTORICAL GROWTH\n")
        f.write("------------------------------\n")
        f.write(f"Revenue CAGR: {pct(historical_growth.get('revenue_cagr'))}\n")
        f.write(f"EPS CAGR    : {pct(historical_growth.get('eps_cagr'))}\n")
        f.write(f"FCF CAGR    : {pct(historical_growth.get('fcf_cagr'))}\n")
        f.write(f"Suggested Historical Growth: {pct(historical_growth.get('suggested_historical_growth'))}\n\n")