# news

News & disruption check — recent news coverage and sentiment analysis for a company.

## Usage

```bash
python3 scripts/dr.py news <SYMBOL>
python3 scripts/news.py <SYMBOL> [--json]
```

## Examples

```bash
# US stock news
python3 scripts/dr.py news MSFT
python3 scripts/dr.py news NVDA

# Thai stock news
python3 scripts/dr.py news KBANK

# JSON output
python3 scripts/news.py MSFT --json
```

## Output Example

```
══════════════════════════════════════════════════════════════════════
  📰 MSFT — News & Disruption Check
  Company: Microsoft
══════════════════════════════════════════════════════════════════════

  Overall Sentiment: 🟢 Positive
  Articles Found:    15
  Positive:  🟢 10   Negative:  🔴 2   Neutral:  ⚪ 3

  ── Key Signals ───────────────────────────────────────────────────
  🟢 ai
  🟢 earnings
  🟢 buy
  🟢 cloud
  🔴 sell

  ── Recent News ───────────────────────────────────────────────────
   1. 🟢 Microsoft earnings press release available on Investor Relatio...
      Microsoft Source  •  29 Apr 2026

   2. ⚪ Microsoft calls for $190 billion in 2026 capital spending on s...
      CNBC  •  29 Apr 2026

   3. 🟢 Analysts Say Buy Microsoft Stock (MSFT) after Build 2026 Reinf...
      TipRanks  •  04 Jun 2026

  ── Disruption Assessment ──────────────────────────────────────────
  ✅ POSITIVE MOMENTUM — Strong positive coverage

══════════════════════════════════════════════════════════════════════
```

## Sentiment Icons

| Icon | Sentiment | Meaning |
|------|-----------|---------|
| 🟢 | Positive | More positive keywords than negative |
| 🔴 | Negative | More negative keywords than positive |
| ⚪ | Neutral | Balanced or no clear signals |

## Disruption Assessment

| Assessment | Criteria |
|------------|----------|
| 🚨 HIGH NEGATIVE PRESSURE | Negative articles > 2x positive |
| ⚠️ ELEVATED CONCERN | Negative articles > positive |
| ✅ POSITIVE MOMENTUM | Positive articles > 2x negative |
| ⚪ MIXED SIGNALS | Balanced coverage |

## Negative Signal Keywords

The system scans for these disruption signals:

| Category | Keywords |
|----------|----------|
| Layoffs | layoff, laid off, firing, job cuts, restructuring |
| Legal | lawsuit, sued, legal action, settlement, investigation |
| Financial | decline, loss, losses, debt, bankruptcy |
| Competition | competition, competitor, market share, disruption |
| Regulatory | regulation, regulatory, ban, fine, penalty |
| Security | hack, breach, security, vulnerability |
| Product | recall, defect, safety |
| Analyst | downgrade, sell, bearish |

## Positive Signal Keywords

| Category | Keywords |
|----------|----------|
| Performance | growth, profit, revenue, earnings, beat |
| Innovation | innovation, launch, new product, partnership |
| Corporate | expansion, acquisition, merger |
| Analyst | upgrade, buy, bullish, outperform |
| Shareholder | dividend, buyback, shareholder |
| Technology | ai, artificial intelligence, cloud |

## Data Source

- **Google News RSS** — Searches for `<company name> stock` and `<company name> earnings`
- No API key required
- Returns up to 15 recent articles

## Notes

- Sentiment is keyword-based (simple but effective for quick scan)
- Thai companies may have fewer English-language results
- For deeper analysis, read the full articles via the provided links
- Disruption signals are flagged automatically in the output
