from pathlib import Path


OUTPUT_FOLDER = Path("outputs")


def pct(value):
    if value is None:
        return "N/A"

    return f"{value * 100:.2f}%"


def write_report(stock, valuation):

    OUTPUT_FOLDER.mkdir(exist_ok=True)

    filename = OUTPUT_FOLDER / f"{stock.ticker}_report.txt"

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

        f.write("VALUATION\n")
        f.write("------------------------------\n")

        f.write(f"Growth Used : {valuation.total_growth_used}%\n")
        f.write(f"Fair Value  : {valuation.fair_value}\n")
        f.write(f"Buy Price   : {valuation.buy_price}\n")
        f.write(f"Qualifies   : {valuation.qualifies}\n")
        f.write(f"Reason      : {valuation.reason}\n")