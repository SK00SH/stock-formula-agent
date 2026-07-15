# Sunny Formula Product Specification

## Product purpose

Sunny Formula is an investment decision engine.

It helps answer:

- Is this company undervalued?
- What buy price should I wait for?
- Why was this growth rate used?
- Is the valuation still valid?
- When should I recalculate?
- Is the business high quality?
- Why is the stock cheap?
- Should I hold, trim, or sell?

---

## Core philosophy

The market price changes every second.

The valuation should only change when the business changes.

A valuation remains valid until new fundamental information appears, usually the next earnings release.

---

## Current V2 workflow

1. Run scanner.
2. Calculate valuation.
3. Save report.
4. Save valuation date.
5. Save next earnings date.
6. Mark valuation as VALID.
7. Export buy price for Trading212 / HL alerts.
8. If price hits buy price before next earnings, use saved valuation.
9. After earnings, mark valuation EXPIRED.
10. Re-run Sunny Formula.

---

## Growth logic

Dividend method should be used only when reliable.

If dividend is unsuitable:
- use historical growth if reliable
- use cached analyst/API growth if available
- call Alpha Vantage only when needed
- fall back to CSV manual estimate

Every growth estimate must include:
- source
- reason
- confidence

---

## Research report should eventually include

- Buy price
- Fair value
- Current price
- Growth used
- Growth source
- Why this growth was chosen
- Dividend reliability
- 3Y / 5Y / 10Y growth
- Business model
- Competitors
- Moat
- CEO / mission / goals
- Risks
- Debt
- Margins
- ROIC / ROE
- Debt-to-equity
- Payout ratio
- Cash flow quality
- Profitability outlook
- Why stock is cheap
- Value trap warning
- Next earnings date
- Valuation status
- Confidence score

---

## Sell framework

Do not sell simply because a stock is up 200–300%.

Sell / trim if:
- price is materially above updated fair value
- thesis breaks
- business quality deteriorates
- position becomes too concentrated

---

## Productisation principles

Do not build native mobile first.

Build:
1. Python engine
2. Web app
3. PWA
4. Native app only if proven demand

Before UI, compare:
- Lovable
- Bolt
- Replit
- Vercel v0
- Cursor + React
- other best tools available at that time