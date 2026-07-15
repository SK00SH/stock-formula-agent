# Sunny Formula Architecture

## Core principle

Sunny Formula must be modular. Future features should be added without rewriting the entire codebase.

Do not tie core logic directly to Yahoo, Alpha Vantage, Finnhub, or any provider.

Use provider-style interfaces:

- price_provider.get_price()
- growth_provider.get_growth()
- financial_data_provider.get_financials()
- earnings_provider.get_next_earnings()

---

## Main modules

### Data Layer

Responsible for fetching and normalising data.

Planned providers:
- YahooProvider
- AlphaVantageProvider
- LocalDatabaseProvider
- FutureProvider

The rest of the system should not care where the data came from.

---

### Growth Engine

Responsible for choosing the growth rate.

Inputs:
- Dividend formula
- Historical growth
- Analyst/API growth
- Cached growth estimates
- Manual CSV fallback

Outputs:
- growth used
- growth source
- growth reason
- confidence score

---

### Valuation Engine

Responsible only for applying the formula.

Inputs:
- EPS
- PE
- chosen growth
- discount rate
- margin of safety

Outputs:
- future price
- fair value
- buy price
- qualifies

---

### Research Engine

Responsible for qualitative and supporting analysis.

Includes:
- business model
- moat
- competitors
- CEO / mission
- risks
- why stock is cheap
- value trap warning
- capital allocation

---

### Quality Engine

Responsible for Business Quality Score.

Inputs may include:
- ROIC
- ROE
- margins
- free cash flow
- debt
- revenue consistency
- EPS consistency
- share dilution
- payout ratio
- external metrics such as Piotroski / Altman where possible

Score must be explainable.

---

### Portfolio / Alert Engine

Responsible for practical use.

Includes:
- watchlist
- buy price export
- Trading212 / HL alert support
- distance from buy price
- valuation status
- next earnings date

---

### Sell Engine

Responsible for sell / trim logic.

Triggers:
- overvaluation
- thesis break
- position concentration

---

### Backtesting Engine

Responsible for testing formula versions against history.

Used to:
- compare V1 vs later versions
- test scoring weights
- test margin-of-safety changes
- avoid overfitting

---

## Design rule

Before adding any feature, ask:

1. Does this help real investing decisions?
2. Can it be added without rewriting unrelated modules?
3. Can it be tested against V1?
4. Can the data source be swapped later?