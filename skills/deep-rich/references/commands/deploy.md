# deploy

Cash deployment — where to put idle cash based on drift and market conditions.

## When to use

- When user has extra cash (salary, bonus, sold something)
- When user asks "what should I buy" / "where should I put my cash"
- During weekly review (as part of review workflow)

## Workflow

### Step 1: Check cash position

```bash
cd "$DEEP_RICH_HOME"
python3 scripts/dr.py portfolio
python3 scripts/dr.py deployment
```

Calculate:
- Total cash
- Emergency floor (฿300k)
- Deployable cash (cash - floor)

### Step 2: Check drift

From portfolio output, identify underweight classes:
- Cash > target → deploy excess
- Any class < target → candidate for deployment

### Step 3: Apply deployment rules

| Rule | Description |
|------|-------------|
| Emergency floor | Never deploy below ฿300k |
| Proportional to drift | More underweight = more allocation |
| Exclude Gold | Passive, no rebalancing |
| Exclude Cash | It's the source, not a target |

### Step 4: Consider market conditions

If user mentions a specific opportunity:
```
web_search: "[opportunity] Thailand stocks"
web_search: "[opportunity] investment thesis"
```

If no specific opportunity, use mechanical allocation.

### Step 5: Synthesize

```
══════════════════════════════════════════════════════════════════════
  🚀 Deployment Plan
══════════════════════════════════════════════════════════════════════

  Cash: ฿X
  Emergency floor: ฿300,000
  Deployable: ฿Y

  ── Allocation ────────────────────────────────────────────────────
  Thai SET:    ฿X → [specific stocks or general]
  US Market:   ฿Y → [specific stocks or general]
  Crypto:      ฿Z → BTC/ETH

  ── Suggested Stocks ──────────────────────────────────────────────
  [If user mentioned opportunity: specific stocks]
  [If mechanical: current holdings or new research]

  ── Timeline ──────────────────────────────────────────────────────
  Deploy gradually over 3-6 months via dollar-cost averaging.
```

## Example: Mechanical deployment

```
══════════════════════════════════════════════════════════════════════
  🚀 Deployment Plan
══════════════════════════════════════════════════════════════════════

  Cash: ฿991,789
  Emergency floor: ฿300,000
  Deployable: ฿691,789

  ── Allocation (proportional to drift) ────────────────────────────
  Thai SET:    ฿397,640 (drift -19.0%, most underweight)
  US Market:   ฿211,966 (drift -10.1%)
  Crypto:      ฿82,183  (drift -3.9%)

  ── Suggested Stocks ──────────────────────────────────────────────
  Thai SET: KBANK (already owned, +61% gain) or research new?
  US Market: MSFT (owned, +10%) or GOOGL (owned, +183%)
  Crypto: BTC + ETH (split evenly)

  ── Timeline ──────────────────────────────────────────────────────
  Month 1: ฿200k (Thai SET focus)
  Month 2: ฿200k (US Market)
  Month 3: ฿150k (Thai SET + Crypto)
  Month 4: ฿142k (remaining)

  💡 Dollar-cost average to reduce timing risk.
```

## Example: Opportunity-driven deployment

User: "I see data center trend in Thailand. Should I deploy there?"

```
══════════════════════════════════════════════════════════════════════
  🚀 Deployment — Data Center Opportunity
══════════════════════════════════════════════════════════════════════

  Cash: ฿991,789
  Deployable: ฿691,789
  Thai SET target: 25% (currently 6.0%)

  ── Data Center Thesis ────────────────────────────────────────────
  Thailand positioning as Southeast Asia data center hub.
  Key needs: Power (EGCO, GPSC, BGRIM), Infrastructure (AMATA),
  Connectivity (TRUE, ADVANC)

  ── Suggested Allocation ──────────────────────────────────────────
  EGCO: ฿100k — Power generation (data centers need electricity)
  GPSC: ฿80k — Clean power (ESG-friendly data centers)
  AMATA: ฿60k — Industrial estates (data center locations)
  Existing Thai SET: ฿157k — KBANK, etc.

  ── Risk Check ────────────────────────────────────────────────────
  This would bring Thai SET to ~20% (target 25%). Still underweight.
  Concentration: 3 new stocks in same theme. Diversify within theme.

  ── Timeline ──────────────────────────────────────────────────────
  Month 1: ฿100k (EGCO — largest position)
  Month 2: ฿80k (GPSC)
  Month 3: ฿60k (AMATA)
```

## Guards

- **Emergency floor**: Never deploy below ฿300k
- **Dollar-cost average**: Don't deploy everything at once
- **Diversification**: Don't put everything in one theme
- **Research first**: If suggesting specific stocks, run research workflow
- **No FOMO**: Just because there's an opportunity doesn't mean you must act

## Tools used

- `dr.py portfolio` — cash position, drift
- `dr.py deployment` — mechanical allocation
- `dr.py research <SYM>` — if suggesting specific stocks
- `web_search` — if researching an opportunity
