# Sunny Formula Roadmap

## V1 — Frozen baseline

Status: Complete / frozen.

Purpose:
Recreate Sunny's original valuation formula.

Rules:
- Do not change V1 logic.
- Use dividend formula where reliable.
- If dividend method is unsuitable, use external/manual growth fallback.
- Output fair value, buy price, growth source, and reason.

Formula:
- Future price = EPS × (1 + growth)^10 × PE
- Fair value = future price / 1.15^10
- Buy price = fair value × 0.5

---

## V2 — Usable automation

Goal:
Make the tool practical for day-to-day use.

Features:
- Alpha Vantage fallback integration.
- Local growth estimate cache to save API calls.
- CSV fallback if no reliable estimate exists.
- Growth Engine decision logic:
  - dividend formula
  - historical growth
  - analyst/API growth
  - cached growth
  - manual fallback
- Valuation lifecycle:
  - valuation date
  - next earnings date
  - valid until next earnings
  - status: VALID / EXPIRED
- Trading212 / HL buy-price alert export.
- Provider architecture before V2 grows further.
- ROADMAP.md and ARCHITECTURE.md created.

---

## V2.1 — Research and intelligence

Goal:
Improve growth assumptions and company understanding.

Features:
- 3Y / 5Y / 10Y revenue, EPS, and FCF growth.
- Growth trend classification:
  - accelerating
  - stable
  - decelerating
- Growth confidence score.
- Business Quality Score with explained components.
- Backtested scoring weights.
- AI research report:
  - how company makes money
  - competitors
  - moat
  - CEO / mission / goals
  - risks
  - debt
  - margins
  - ROIC / ROE
  - debt-to-equity
  - payout ratio
  - cash flow quality
  - profitability outlook
- “Why is it cheap?” explanation.
- Value trap detection.
- Earnings-window caution.
- Feature Gap Log.
- Break-test every major version.
- Confidence score for valuations.

---

## V2.2 — Sell framework

Goal:
Make selling follow the same philosophy as buying.

Sell / trim when:
- Stock is materially overvalued versus updated fair value.
- Investment thesis breaks.
- Position becomes too concentrated.

Avoid:
- Fixed “sell at 200–300%” rule.

---

## V3 — Data-source independence

Goal:
Avoid being locked into Yahoo, Alpha Vantage, Finnhub, or any single provider.

Features:
- YahooProvider
- AlphaVantageProvider
- LocalDatabaseProvider
- FutureProvider
- Store historical data locally over time.
- Provider-swappable architecture.
- Prepare for proper backtesting.
- Possible SEC / company filing parser later.

---

## V3.1 — Backtesting

Goal:
Prove whether formula changes improve results.

Features:
- Test V1, V2, and V2.1 against historical years.
- Compare buy signals against later returns.
- Identify where V1 missed major compounders.
- Test adaptive margin of safety.
- Test Business Quality Score weights.
- Track performance versus S&P 500 / FTSE / global index.

---

## V4 — Product / SaaS

Goal:
Turn Sunny Formula into a real product.

Approach:
- Web app / PWA first.
- Native mobile app only if user demand proves it.
- Before UI, compare Lovable, Bolt, Replit, Vercel v0, Cursor + React, or best available tool at that time.

Features:
- User accounts
- Watchlists
- Saved valuations
- Reports
- Alerts
- Backtesting dashboard
- Portfolio dashboard
- Decision log
- Subscription model