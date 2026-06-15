# rebalance

Rebalancing — mechanical (hit targets) or rotate (losers → opportunity).

## When to use

- Quarterly (mechanical rebalancing)
- When drift > 15% in any class
- When user spots an opportunity and wants to rotate
- When user asks "should I rebalance" / "how do I fix my allocation"

## Two modes

### Mechanical mode

Standard rebalancing — sell overweight, buy underweight, hit targets.

```bash
dr.py rebalance mechanical
```

### Rotate mode

Opportunistic — rotate from losers to a new trend.

```bash
dr.py rebalance rotate
```

---

## Mechanical Mode Workflow

### Step 1: Gather data

```bash
cd "$DEEP_RICH_HOME"
python3 scripts/dr.py portfolio
python3 scripts/dr.py health watchlist
python3 scripts/dr.py deployment
```

### Step 2: Identify sell candidates

| Condition | Action |
|-----------|--------|
| Class overweight by >15% | Trim to target |
| Holding has health grade F | Cut losses |
| Holding has health grade D + loss >20% | Seriously consider cutting |

### Step 3: Identify buy candidates

| Condition | Action |
|-----------|--------|
| Class underweight | Buy to target |
| Cash excess | Deploy to underweight classes |

### Step 4: Calculate trades

For each class:
- Current % vs Target %
- Difference in ฿
- What to sell/buy

### Step 5: Synthesize

```
══════════════════════════════════════════════════════════════════════
  ⚖️ Rebalancing Plan — Mechanical
══════════════════════════════════════════════════════════════════════

  ── Sells ─────────────────────────────────────────────────────────
  [Overweight positions to trim]

  ── Buys ──────────────────────────────────────────────────────────
  [Underweight classes to add to]

  ── Net Effect ────────────────────────────────────────────────────
  [How allocation changes]

  ── Tax/Transaction Considerations ────────────────────────────────
  [Any notable costs or tax implications]
```

---

## Rotate Mode Workflow

### Step 1: User provides opportunity

User says: "I want to rotate from [losers] to [opportunity]"

### Step 2: Identify sell candidates

```bash
python3 scripts/dr.py portfolio
python3 scripts/dr.py health watchlist
```

| Condition | Action |
|-----------|--------|
| Health grade F | Strong sell candidate |
| Health grade D + loss >20% | Sell candidate |
| Underperforming (> -20% from cost) | Consider selling |

### Step 3: Research opportunity

```bash
python3 scripts/dr.py research <opportunity stocks>
```

Or if user provides specific stocks:
```bash
python3 scripts/dr.py fundamentals <SYM>
python3 scripts/dr.py health <SYM>
```

### Step 4: Calculate rotation

- How much to sell from losers
- How much to buy into opportunity
- Check it doesn't break diversification

### Step 5: Synthesize

```
══════════════════════════════════════════════════════════════════════
  🔄 Rebalancing Plan — Rotate
══════════════════════════════════════════════════════════════════════

  ── Sell (Losers) ─────────────────────────────────────────────────
  SISB: ฿10,890 (Health: F, -43%)
  AAI: ฿7,080 (Health: F, -37%)
  Total recovered: ฿18,970

  ── Buy (Opportunity) ────────────────────────────────────────────
  EGCO: ฿10,000 — Data center power play
  GPSC: ฿8,970 — Clean power for data centers

  ── Net Effect ────────────────────────────────────────────────────
  Thai SET: 6.0% → 6.5% (still underweight, but better quality)
  Removed: 2 F-grade stocks
  Added: 2 B-grade stocks in growth theme

  ── Thesis ────────────────────────────────────────────────────────
  Rotating from failing Thai SET holdings into data center theme.
  Keeps Thai SET allocation, improves quality.
```

## Example: Rotate to data center trend

```
══════════════════════════════════════════════════════════════════════
  🔄 Rebalancing Plan — Data Center Rotation
══════════════════════════════════════════════════════════════════════

  ── Sell (Losers) ─────────────────────────────────────────────────
  SISB: ฿10,890 (Health: F, -43%) — hospital chain, no data center link
  AAI: ฿7,080 (Health: F, -37%) — airline, no data center link
  TASCO: ฿13,800 (Health: D, -14%) — asphalt, weak thesis
  Total recovered: ฿31,770

  ── Buy (Data Center Theme) ──────────────────────────────────────
  EGCO: ฿15,000 — Power generation (data centers need electricity)
  GPSC: ฿10,000 — Clean power (ESG data centers)
  AMATA: ฿6,770 — Industrial estates (data center locations)

  ── Net Effect ────────────────────────────────────────────────────
  Thai SET: 6.0% → 7.8%
  Removed: 3 weak holdings (F, F, D grade)
  Added: 3 quality holdings (B, B, B grade) in growth theme

  ── Risk Check ────────────────────────────────────────────────────
  ✅ Still within Thai SET allocation
  ✅ Diversified within theme (power, clean power, infrastructure)
  ✅ All new holdings are B-grade (good quality)
  ⚠️ Concentrated in one theme — monitor data center trend
```

## Guards

Enforce [GUARDS](../GUARDS.md).

Workflow-specific:

- **Don't over-trade**: Rebalancing has costs. Don't do it for tiny drifts.
- **Tax awareness**: Selling triggers capital gains (in some jurisdictions)
- **Diversification**: Don't concentrate everything in one theme
- **Research first**: If rotating into new stocks, research them

## Tools used

- `dr.py portfolio` — current state, drift
- `dr.py health watchlist` — identify sell candidates
- `dr.py deployment` — target allocation
- `dr.py research <SYM>` — research buy candidates
- `web_search` — research opportunities
