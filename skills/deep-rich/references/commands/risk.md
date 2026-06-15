# risk

Risk assessment — what could hurt your portfolio.

## When to use

- Monthly (regular risk check)
- When user asks "what's my risk" / "what could go wrong"
- Before making a large allocation change
- After market events (crash, sector rotation)

## Workflow

### Step 1: Gather data

```bash
cd "$DEEP_RICH_HOME"
python3 scripts/dr.py portfolio
python3 scripts/dr.py health watchlist
python3 scripts/dr.py performance
```

### Step 2: Assess concentration risk

| Risk | Check | Threshold |
|------|-------|-----------|
| Single stock | % of total portfolio | > 5% = flag |
| Single stock in class | % of asset class | > 15% = flag |
| Sector concentration | % in same sector | > 30% = flag |
| Correlated holdings | Stocks that move together | High correlation = flag |

### Step 3: Assess quality risk

| Risk | Check | Threshold |
|------|-------|-----------|
| F-grade holdings | Health grade F | Any = flag |
| D-grade holdings | Health grade D | > 10% of portfolio = flag |
| Declining revenue | Revenue YoY | Declining = flag |
| High debt | Debt/Equity | > 2.0 = flag |

### Step 4: Assess market risk

| Risk | Check | Threshold |
|------|-------|-----------|
| 52W position | Near 52W high | > 90% = flag (overbought?) |
| 52W position | Near 52W low | < 10% = flag (value trap?) |
| Drawdown | Max loss if 20% correction | > 15% of portfolio = flag |

### Step 5: Synthesize

```
══════════════════════════════════════════════════════════════════════
  ⚠️ Risk Report
══════════════════════════════════════════════════════════════════════

  ── Concentration Risk ────────────────────────────────────────────
  NVDA: 6.7% of portfolio (threshold: 5%)
  Tech sector: 25% of portfolio (threshold: 30%)

  ── Quality Risk ──────────────────────────────────────────────────
  F-grade holdings: SISB, AAI, NSL (8% of portfolio)
  D-grade holdings: AMPH, TASCO (5% of portfolio)
  Total at-risk: 13% of portfolio

  ── Market Risk ───────────────────────────────────────────────────
  GOOGL: 81% of 52W range (near high)
  ARM: 85% of 52W range (near high)
  If 20% correction: portfolio would drop ฿360k (-20%)

  ── Risk Score ────────────────────────────────────────────────────
  Overall: 🟡 Moderate
  Main risk: Quality risk (13% in D/F-grade stocks)
  Action: Cut F-grade holdings to reduce risk
```

## Example: Tech-heavy portfolio

```
══════════════════════════════════════════════════════════════════════
  ⚠️ Risk Report
══════════════════════════════════════════════════════════════════════

  ── Concentration Risk ────────────────────────────────────────────
  ⚠️ US Tech: 18% of portfolio (NVDA, GOOGL, MSFT, NET, ARM)
     If tech sector drops 30%, portfolio loses ฿54k

  ── Quality Risk ──────────────────────────────────────────────────
  ✅ No F-grade in major positions
  ⚠️ AMPH: D-grade, -61% loss (1.4% of portfolio)

  ── Correlation Risk ──────────────────────────────────────────────
  ⚠️ NVDA, GOOGL, MSFT all move together (AI theme)
     If AI hype fades, all three drop together
     Diversification benefit: low within US Market

  ── Market Risk ───────────────────────────────────────────────────
  GOOGL: 81% of 52W range — near high, could pull back
  NVDA: 72% of 52W range — mid-range
  MSFT: 38% of 52W range — near low, could be opportunity

  ── Risk Score ────────────────────────────────────────────────────
  Overall: 🟡 Moderate
  Main risk: Correlation (tech stocks move together)
  Mitigation: Thai SET is underweight — adds diversification
```

## Guards

- **Don't alarm**: Moderate risk is normal. Only flag real concerns.
- **Show context**: A 5% NVDA position isn't dangerous if the rest is diversified.
- **Suggest mitigation**: Don't just flag risks — suggest how to reduce them.
- **Respect risk tolerance**: Some investors can handle more risk.

## Tools used

- `dr.py portfolio` — current allocation
- `dr.py health watchlist` — quality grades
- `dr.py performance` — gain/loss positions
- Analysis — concentration, correlation calculations
