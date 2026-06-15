# research

Decision support for buy/sell — comprehensive stock analysis with verdict. Produces a reusable company profile artifact.

## When to use

- When user asks "should I buy X" / "is X worth buying" / "what do you think about X"
- When user is considering selling a position
- When user mentions a stock they're watching
- Before any buy/sell decision

## Output artifacts

Every research produces two artifacts:

1. `.deep-rich/companies/<SYM>.json` — structured company profile data. This saves research cost: future sessions can read the profile instead of re-searching.
2. `company/<symbol-lower>.html` — user-facing visual company profile, styled with the shared [Deep Rich report design system](../DESIGN.md).

Check if profile data exists before researching:

```bash
test -f .deep-rich/companies/<SYM>.json && cat .deep-rich/companies/<SYM>.json
```

If profile exists and `meta.updated_at` is <7 days old, use it as the base. Refresh prices, health, and recent news before updating the HTML. Otherwise, refresh the JSON first, then regenerate the HTML.

The HTML is not optional when the user asks for a company profile or when post-onboard profile backfill is being tested. It should be the artifact the user opens and reads.

Before generating the HTML, resolve the company logo from the local `.deep-rich` cache. If no trusted logo has been downloaded yet, attempt logo discovery/download using the source priority in [DATA-SOURCES](../DATA-SOURCES.md#company-logos), save it under `.deep-rich/company-assets/logos/`, and record metadata in the profile JSON. If logo discovery fails, use a generated ticker tile and record `logo` as unknown/missing in `data_quality`.

---

## Research Checklist

Follow this checklist in order. Each item has a data source and required fields. If a required field cannot be fetched, keep the field in the JSON/HTML and mark it `unknown` with a short reason; do not silently omit sections.

### 1. Basic Info

| Field | Source | Required |
|-------|--------|----------|
| Ticker | User input | ✅ |
| Company name | SEC EDGAR or Yahoo | ✅ |
| Exchange | Yahoo Finance | ✅ |
| Sector/Industry | Yahoo Finance or SEC | ✅ |
| Country | SEC EDGAR | ✅ |
| Website | SEC EDGAR | Optional |
| Logo source/path | Official website or logo provider; see [DATA-SOURCES](../DATA-SOURCES.md#company-logos) | Optional |

```bash
python3 scripts/dr.py fundamentals <SYM>
```

### 2. The Business — What does this company do?

| Field | Source | Required |
|-------|--------|----------|
| Business description | SEC 10-K (Item 1) or web search | ✅ |
| Key products/services | SEC 10-K or web search | ✅ |
| Revenue segments | SEC 10-K (Item 7) | Optional |
| Competitive moat | Analysis | ✅ |

**Search queries:**
```
web_search: "<company name> what does it do"
web_search: "<company name> products services"
web_search: "<company name> 10-K business overview"
```

If SEC EDGAR works, read the latest 10-K filing for Item 1 (Business) description.

### 3. Market & TAM — How big is the opportunity?

| Field | Source | Required |
|-------|--------|----------|
| Total addressable market (TAM) | Web search | ✅ |
| TAM source | (who estimated) | ✅ |
| Growth drivers | Web search + analysis | ✅ |
| Key trends | Web search | ✅ |

**Search queries:**
```
web_search: "<product/service> market size 2026"
web_search: "<product/service> TAM billion"
web_search: "<industry> growth drivers trends"
```

### 4. Competitors — Who else is in this space?

| Field | Source | Required |
|-------|--------|----------|
| Direct competitors (2-3) | Web search | ✅ |
| Company's advantage | Analysis | ✅ |
| Company's disadvantage | Analysis | ✅ |

**Search queries:**
```
web_search: "<company name> competitors"
web_search: "<company name> vs <competitor>"
```

### 5. Pipeline & Catalysts — What's coming?

| Field | Source | Required |
|-------|--------|----------|
| Upcoming products/launches | SEC 10-K, earnings call, web search | ✅ |
| Key dates (FDA, earnings, etc.) | Web search | ✅ |
| Market size of pipeline products | Web search | ✅ |

**Search queries:**
```
web_search: "<company name> pipeline 2026 2027"
web_search: "<company name> upcoming products launches"
web_search: "<company name> FDA approval timeline"
web_search: "<company name> earnings call transcript"
```

### 6. Financials — The numbers

| Field | Source | Required |
|-------|--------|----------|
| Price, 52W range | Yahoo Finance | ✅ |
| Revenue, growth | SEC XBRL | ✅ |
| Net income, margin | SEC XBRL | ✅ |
| Debt/Equity | SEC XBRL | ✅ |
| Health grade | Health script | ✅ |

```bash
python3 scripts/dr.py fundamentals <SYM>
python3 scripts/dr.py health <SYM>
```

### 7. Valuation — Is it cheap or expensive?

| Field | Source | Required |
|-------|--------|----------|
| P/E ratio | Yahoo Finance | Optional |
| P/BV ratio | Yahoo Finance | Optional |
| Analyst consensus | Web search | Optional |
| Analyst price target | Web search | Optional |

**Search queries:**
```
web_search: "<SYM> analyst rating target price 2026"
web_search: "<SYM> valuation metrics"
```

### 8. Risks — What could go wrong?

| Field | Source | Required |
|-------|--------|----------|
| Key risk factors | SEC 10-K (Item 1A) | ✅ |
| Regulatory risks | Web search | ✅ |
| Competitive risks | Analysis | ✅ |

**Search queries:**
```
web_search: "<company name> risk factors"
web_search: "<company name> regulatory challenges"
```

### 9. Thesis — Your verdict

| Field | Source | Required |
|-------|--------|----------|
| Bull case (2-3 points) | Synthesis | ✅ |
| Bear case (2-3 points) | Synthesis | ✅ |
| Verdict (BUY/HOLD/AVOID/SELL) | Decision rules | ✅ |
| Reasoning | Synthesis | ✅ |
| Suggested action | Synthesis | ✅ |

### 10. Management & Ownership

| Field | Source | Required |
|-------|--------|----------|
| CEO / key executives | SEC filing, annual report, company site | Optional but keep section |
| Board independence / governance notes | SEC proxy, annual report | Optional but keep section |
| Insider ownership / recent insider activity | SEC Form 4 / proxy / reputable data | Optional but keep section |
| Institutional ownership | 13F / reputable data provider | Optional but keep section |

If unavailable, mark as `unknown` and explain which source should be checked next.

### 11. Data Quality & Freshness

| Field | Source | Required |
|-------|--------|----------|
| Facts list | Research notes | ✅ |
| Calculated metrics list | App scripts / visible formulas | ✅ |
| Estimates list | Analyst/management/model sources | ✅ |
| Unknown or missing fields | Research notes | ✅ |
| Last updated | Agent runtime date | ✅ |
| Source log | Commands + URLs/searches | ✅ |

Always separate `facts`, `calculated`, `estimates`, `interpretations`, and `unknowns`. Forecasts, TAM, analyst targets, fair value, future growth, and management guidance are estimates unless independently modeled with visible assumptions.

---

## Decision Rules

| Health | Signal | Verdict |
|--------|--------|---------|
| A | Strong fundamentals, growing | **BUY** — quality at reasonable price |
| B | Good with minor concerns | **BUY** — if allocation allows |
| C | Mixed signals | **HOLD/WATCH** — monitor, don't add |
| D | Significant issues | **AVOID** — don't buy, consider selling if held |
| F | Major problems | **SELL** if held, **AVOID** if not |

Additional signals:
- Revenue declining → negative signal
- High debt (D/E > 2.0) → caution
- Near 52W low → could be opportunity or value trap
- Near 52W high → could be momentum or overvalued

---

## Output: Company Profile Data

Save to `.deep-rich/companies/<SYM>.json`.

The JSON should contain these top-level sections every time:

| Key | Required | Purpose |
|---|---:|---|
| `ticker`, `name`, `exchange`, `sector`, `industry`, `country`, `website` | ✅ | Basic identity |
| `logo` | Optional | Local cached logo path, source URL, confidence, license note |
| `business` | ✅ | Description, products, revenue model, moat |
| `market` | ✅ | TAM/trends/growth drivers, with estimate labels |
| `competitors` | ✅ | Peer landscape |
| `pipeline` / `catalysts` | ✅ | Upcoming product/business events; label estimates |
| `financials` | ✅ | Price, range, revenue, earnings, balance sheet, health |
| `position` | If held | Quantity, cost basis, market value, THB conversion, gain/loss |
| `risks` | ✅ | Business, financial, valuation, data, governance risks |
| `management` | ✅ | Executives/governance/ownership; use `unknown` if unavailable |
| `thesis` | ✅ | Bull case, bear case, verdict, suggested action |
| `data_quality` | ✅ | Facts, calculated, estimates, interpretations, unknowns |
| `research_log` | ✅ | Commands, web searches, source URLs, dates |
| `meta` | ✅ | first researched, updated at, depth, confidence |

Example shape:

```json
{
  "ticker": "AMPH",
  "name": "Amphastar Pharmaceuticals, Inc.",
  "exchange": "NasdaqGS",
  "sector": "Healthcare",
  "industry": "Pharmaceuticals",
  "country": "US",

  "business": {
    "description": "Develops and manufactures injectable and inhalation drugs",
    "products": ["Insulin", "Glucagon", "Respiratory drugs", "AMP-007 (Atrovent)"],
    "revenue_segments": ["Pharmaceutical products"],
    "moat": "Vertical integration in insulin API manufacturing"
  },

  "market": {
    "tam": "$50B+ (GLP-1 market)",
    "tam_source": "Industry reports",
    "growth_drivers": ["Diabetes epidemic", "Obesity treatment", "Generic wave"],
    "trends": ["GLP-1 dominance", "Biosimilar competition"]
  },

  "competitors": [
    {"name": "Teva", "ticker": "TEVA", "advantage": "Larger scale", "disadvantage": "Less focused"},
    {"name": "Viatris", "ticker": "VTRS", "advantage": "Global reach", "disadvantage": "Debt burden"}
  ],

  "pipeline": [
    {
      "name": "AMP-018 (Generic Semaglutide)",
      "target_market": "Ozempic/Wegovy generic",
      "market_size": "$50B+",
      "status": "ANDA filed with FDA",
      "timeline": "2027",
      "notes": "GLP-1 generic, massive market"
    }
  ],

  "financials": {
    "price": 19.39,
    "price_date": "2026-06-09",
    "52w_low": 16.65,
    "52w_high": 31.26,
    "52w_position": 18.8,
    "revenue": 49700000,
    "revenue_growth_yoy": -36.9,
    "net_income": 37300000,
    "margin": 75.1,
    "debt_equity": 0.15,
    "health_grade": "D",
    "health_score": 45
  },

  "risks": [
    "Revenue declining -36.9% YoY",
    "GLP-1 competition from Teva, Viatris",
    "Catalysts are 12+ months away"
  ],

  "catalysts": [
    "AMP-018 GLP-1 ANDA approval (2027)",
    "AMP-007 Atrovent launch (April 2026)",
    "$29.5M share buyback in Q1"
  ],

  "thesis": {
    "bull_case": [
      "GLP-1 generics = massive TAM",
      "Near 52W low = contrarian entry",
      "Conservative balance sheet (D/E 0.15x)"
    ],
    "bear_case": [
      "Revenue collapsing -36.9%",
      "Health grade D",
      "Catalysts 12+ months away"
    ],
    "verdict": "HOLD",
    "verdict_reason": "Thesis valid but risk/reward unfavorable for fresh capital",
    "suggested_action": "Don't add more. Monitor AMP-018 progress."
  },

  "research_log": [
    {
      "date": "2026-06-09",
      "source": "web_search + SEC EDGAR + Yahoo",
      "query": "AMPH GLP-1 pipeline diabetes",
      "findings": "Found AMP-018 (generic semaglutide) targeting 2027"
    }
  ],

  "meta": {
    "first_researched": "2026-06-09",
    "updated_at": "2026-06-09",
    "research_depth": "deep",
    "confidence": "medium"
  }
}
```

---

## Output: Visual Company Profile HTML

Generate `company/<symbol-lower>.html` from the JSON profile using the exporter script:

```bash
python3 skills/deep-rich/scripts/export_company_profile.py <SYM>
```

See [export.md](../commands/export.md) for full command reference and template variable contract.

The agent/LLM is responsible for filling and validating the structured data. The script handles escaping, repeated HTML lists/tables, logo path resolution, and template substitution so style stays consistent.

Use the shared [Deep Rich report design system](../DESIGN.md). The HTML must be a single file with embedded CSS unless the app provides a shared exporter.

Required HTML sections:

| Section | Required content |
|---|---|
| Top bar | Deep Rich brand, artifact type, updated date, source profile path |
| Pill navigation | Anchors for overview, valuation, future growth, past performance, financial health, thesis, risks, data quality |
| Hero / stock card | Company name, ticker, exchange, business one-liner, verdict badge, downloaded local logo from `.deep-rich` or generated ticker tile fallback |
| Position snapshot | If held: quantity, cost basis, current value in native currency and THB, gain/loss |
| Company overview | Business description, products/services, revenue model, moat |
| Evidence map | Non-proprietary visual summary; do not call it Simply Wall St Snowflake scoring |
| Valuation guardrail | Factual multiples and missing valuation data; no fair-value claim unless model is explicit |
| Future growth | Estimate-labeled TAM, guidance, analyst expectations, product pipeline |
| Past performance | Historical revenue, margin, cash flow, price range |
| Financial health | Assets, liabilities, equity, debt/equity, cash/runway where available |
| Thesis | Bull case, bear case, verdict, suggested action |
| Risk analysis | Risk flags, catalysts, monitoring questions |
| Management and ownership | Executives, board, insider/institutional ownership; mark unknown if unavailable |
| Data quality boundary | Facts, calculated fields, estimates, interpretations, unknowns, source log |

Visual consistency rules:

- Match the dashboard light theme from [DESIGN](../DESIGN.md).
- Prefer cards, fact strips, tables, pill badges, and a left-side section navigator for long company profiles.
- Use Chart.js CDN when it makes the report clearer, especially for the evidence/radar map, price range, trend, or peer comparison visuals.
- Use THB for aggregate portfolio/position value and native currency for stock-level prices.
- Use explicit caveats for estimate-heavy sections.
- Do not copy Simply Wall St branding, exact visuals, or proprietary scoring.

---

## Synthesis Template

After completing the checklist and writing both artifacts, present to the user:

```
══════════════════════════════════════════════════════════════════════
  🔍 Research: <SYM>
══════════════════════════════════════════════════════════════════════

  Price: $X | 52W: $L - $H (Y% from low)
  Health: [Grade] | Revenue: +X% | Margin: X%

  ── Your Position ─────────────────────────────────────────────────
  [Current holding, if any]
  [Asset class allocation status]

  ── The Business ──────────────────────────────────────────────────
  [What the company does, products/services]
  [Market size (TAM)]
  [Key competitors]

  ── Catalyst / Thesis ────────────────────────────────────────────
  [Why this stock could work — the story]
  [Product pipeline, upcoming events, market trends]

  ── Bull Case ─────────────────────────────────────────────────────
  [2-3 strengths from data]

  ── Bear Case ─────────────────────────────────────────────────────
  [2-3 risks from data]

  ── Verdict ───────────────────────────────────────────────────────
  [BUY / HOLD / AVOID / SELL] — one sentence reasoning

  ── Suggested Action ──────────────────────────────────────────────
  [Specific amount if buying, or reasoning if holding/avoiding]
  [How it fits your allocation strategy]

  📁 Data saved to .deep-rich/companies/<SYM>.json
  🌐 Report saved to company/<symbol-lower>.html
```

---

## Log Decision

If user decides to buy/sell, log to journal AND update the company profile:

### Journal entry
```bash
# Append to .deep-rich/journal.md
```

### Update profile
```bash
# Update .deep-rich/companies/<SYM>.json
# - thesis.suggested_action
# - meta.updated_at
# - research_log entry
```

---

## Example: Research AMPH (existing holding)

```
══════════════════════════════════════════════════════════════════════
  🔍 Research: AMPH (Amphastar Pharmaceuticals)
══════════════════════════════════════════════════════════════════════

  Price: $19.39 | 52W: $16.65 - $31.26 (18.8% from low)
  Health: 🟠 D | Revenue: -36.9% | Margin: expanding

  ── Your Position ─────────────────────────────────────────────────
  Owned: 39.36 shares (฿25,053)
  Cost basis: $50.81 → Current: $19.39 → Loss: -61.8%
  US Market: 24.8% (target 35%) — underweight

  ── The Business ──────────────────────────────────────────────────
  Develops and manufactures injectable and inhalation drugs.
  Key products: insulin, glucagon, respiratory drugs.
  Vertically integrated — makes own insulin API.
  Moat: Vertical integration in insulin manufacturing.

  ── Market ────────────────────────────────────────────────────────
  GLP-1 (Ozempic/Wegovy): $50B+ global market
  Insulin Aspart: $1.4B market
  Growth drivers: Diabetes epidemic, obesity treatment, generic wave

  ── Pipeline ──────────────────────────────────────────────────────
  AMP-018: Generic semaglutide (Ozempic/Wegovy) — ANDA filed, 2027
  AMP-004: Insulin Aspart biosimilar — $1.4B market, 2027
  AMP-007: Generic Atrovent — launched April 2026, sole generic

  ── Competitors ───────────────────────────────────────────────────
  Teva: Larger scale, but less focused on diabetes
  Viatris: Global reach, but debt burden

  ── Bull Case ─────────────────────────────────────────────────────
  ✅ GLP-1 generics = massive TAM ($50B+)
  ✅ Near 52W low — contrarian entry
  ✅ Conservative balance sheet (D/E 0.15x)
  ✅ $29.5M share buyback — management thinks it's cheap

  ── Bear Case ─────────────────────────────────────────────────────
  🚨 Revenue -36.9% YoY — current business struggling
  🚨 Health grade D — significant issues
  🚨 GLP-1 competition fierce — multiple generics filing
  🚨 Catalysts 12+ months away

  ── Verdict ───────────────────────────────────────────────────────
  HOLD. Thesis valid but risk/reward unfavorable for fresh capital.

  ── Suggested Action ──────────────────────────────────────────────
  Don't add more. Monitor AMP-018 progress.
  If GLP-1 gets delayed/rejected, sell.

  📁 Data saved to .deep-rich/companies/AMPH.json
  🌐 Report saved to company/amph.html
```

---

## Refreshing a Profile

When the user asks to research a stock that already has a profile:

1. Read the existing profile.
2. Check `meta.updated_at` — if >7 days old, refresh financials.
3. Always refresh prices before using position value or gain/loss.
4. Check if there is new news or a recent earnings event.
5. Update changed JSON fields.
6. Regenerate `company/<symbol-lower>.html`:

   ```bash
   python3 skills/deep-rich/scripts/export_company_profile.py <SYM>
   ```
7. Present both artifact paths to the user.

This saves research cost — you don't re-search everything every time, but the visual output stays current and consistent.
