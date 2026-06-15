# research

Buy/sell decision support + reusable company profile.

## When

- "should I buy X" / "is X worth buying" / sell consideration / pre-trade

## Artifacts

1. `.deep-rich/companies/<SYM>.json` — structured profile (reuse across sessions)
2. `company/<sym-lower>.html` — visual report per [DESIGN](../DESIGN.md)

Check existing: `test -f .deep-rich/companies/<SYM>.json`. If `meta.updated_at` <7d → base on it; refresh prices/health/news → regen HTML. Else full refresh JSON then HTML.

Logo: cache `.deep-rich/company-assets/logos/` per [DATA-SOURCES](../DATA-SOURCES.md#company-logos); metadata in JSON; fallback ticker tile.

HTML required for profile requests + post-onboard backfill.

## Checklist

Follow [research-checklist](../research-checklist.md) in order.

## Verdict rules

| Health | Signal | Verdict |
|--------|--------|---------|
| A | Strong fundamentals, growing | **BUY** |
| B | Good, minor concerns | **BUY** if allocation allows |
| C | Mixed | **HOLD/WATCH** |
| D | Significant issues | **AVOID** / sell if held |
| F | Major problems | **SELL** if held / **AVOID** |

Also: revenue declining −; D/E >2 caution; near 52W low = opportunity or trap; near high = momentum or expensive.

## HTML export

```bash
python3 skills/deep-rich/scripts/export_company_profile.py <SYM>
```

Agent fills JSON; script escapes, logos, template → `company/<sym>.html`. See [export](export.md).

Required sections: top bar, pill nav, hero+logo, position (if held), overview, evidence map (!SWS branding), valuation guardrail, future growth (estimates), past performance, financial health, thesis, risks, mgmt/ownership, data quality boundary.

## Synth skeleton

```
🔍 Research: <SYM>
Price $X | 52W $L–$H | Health [grade] | Revenue ±X%
Position (if held) | class allocation
Business | Market/TAM | Competitors | Catalyst
Bull case | Bear case
Verdict: BUY/HOLD/AVOID/SELL — one line
Action: amount or hold reason + allocation fit
📁 .deep-rich/companies/<SYM>.json | 🌐 company/<sym>.html
```

## Log decision

Buy/sell → append `journal.md` + update profile `thesis.suggested_action`, `meta.updated_at`, `research_log`.

## Refresh existing profile

Read JSON → if `updated_at` >7d refresh financials → always refresh prices → check news/earnings → update fields → regen HTML → show paths.