from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StockData:
    ticker: str
    current_price: Optional[float]
    eps: Optional[float]
    pe_ratio: Optional[float]
    expected_growth: Optional[float]
    growth_estimate_source: str
    growth_estimate_reason: str
    dividend_yield: Optional[float]
    dividend_growth: Optional[float]
    market_cap: Optional[float]
    dividend_history: dict[int, float] = field(default_factory=dict)
    dividend_growth_rates: dict[str, float] = field(default_factory=dict)

@dataclass
class GrowthResult:
    revenue_cagr: Optional[float]
    eps_cagr: Optional[float]
    fcf_cagr: Optional[float]
    dividend_growth: Optional[float]
    dividend_reliable: bool
    suggested_growth: Optional[float]
    confidence: str
    reason: str


@dataclass
class ValuationResult:
    ticker: str
    current_price: Optional[float]
    eps: Optional[float]
    pe_ratio: Optional[float]
    expected_growth: Optional[float]
    dividend_yield: Optional[float]
    dividend_growth: Optional[float]
    total_growth_used: Optional[float]
    fair_value: Optional[float]
    buy_price: Optional[float]
    margin_of_safety: Optional[float]
    growth_source: str
    growth_reason: str
    qualifies: bool
    reason: str
    dividend_history: dict[int, float] = field(default_factory=dict)
    dividend_growth_rates: dict[str, float] = field(default_factory=dict)