# Research Checklist

Load with [research command](commands/research.md) when filling company profiles. Missing required field → keep section, mark `unknown` + reason.

## Queries

```
web_search: "<co> what does it do|products|10-K business"
web_search: "<product> market size|TAM billion|growth drivers"
web_search: "<co> competitors|vs <peer>"
web_search: "<co> pipeline|upcoming products|FDA|earnings transcript"
web_search: "<SYM> analyst rating target|valuation metrics"
web_search: "<co> risk factors|regulatory challenges"
thai: "<co> ข่าวหุ้น ล่าสุด"
```

## Sections

| # | Fields | Source | Cmd |
|---|--------|--------|-----|
| 1 Basic | ticker, name, exchange, sector, country; website?, logo? | user, Yahoo/SEC | `dr fundamentals <SYM>` |
| 2 Business | description, products, moat; segments? | 10-K Item 1, web | web_search |
| 3 Market | TAM, TAM source, growth drivers, trends | web | web_search |
| 4 Competitors | 2–3 peers, advantage, disadvantage | web + analysis | web_search |
| 5 Pipeline | upcoming products, key dates, pipeline market size | 10-K, earnings, web | web_search |
| 6 Financials | price, 52W, revenue/growth, margin, D/E, health grade | Yahoo, SEC XBRL | `dr fundamentals`, `dr health` |
| 7 Valuation | P/E, P/BV, analyst consensus/target? | Yahoo, web | web_search |
| 8 Risks | 10-K Item 1A risks, regulatory, competitive | SEC, web | web_search |
| 9 Thesis | bull 2–3, bear 2–3, verdict, reasoning, action | synthesis | — |
| 10 Mgmt | CEO, governance, insider, institutional? | SEC proxy/4/13F | mark unknown if missing |
| 11 Quality | facts[], calculated[], estimates[], unknowns[], updated, source log | research notes | label per [DESIGN](DESIGN.md) |

## JSON top-level keys

`ticker`, `name`, `exchange`, `sector`, `industry`, `country`, `website`, `logo`, `business`, `market`, `competitors`, `pipeline`, `catalysts`, `financials`, `position` (if held), `risks`, `management`, `thesis`, `data_quality`, `research_log`, `meta`

`meta`: `first_researched`, `updated_at`, `research_depth`, `confidence`