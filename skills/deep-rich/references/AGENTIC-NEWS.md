# Agentic News

Use native agent tools for news. Numbers → [DATA-SOURCES](DATA-SOURCES.md); narrative → agent tools.

## Tools

| Need | Tool |
|------|------|
| Quick pulse | `web_search` ×2–3 |
| Event impact | `web_search` + synthesis |
| Deep buy/sell research | `agent_browser` — IR, 10-K/10-Q, SET/SEC Thailand, sentiment |
| Thai limited English | `web_search` + Thai terms |
| Sentiment | `web_search` Reddit/Twitter |

## Queries

```
web_search: "[COMPANY] stock news today"
web_search: "[COMPANY] earnings [QUARTER]"
web_search: "[COMPANY] [EVENT] impact"
web_search: "[THAI COMPANY] ข่าวหุ้น ล่าสุด"
```

## Conviction test

Script keeps: 1Y return, P&L from buy, verdict (INTACT/DAMAGED/BROKEN/UNCERTAIN).

Agentic flow:

1. `web_search: "[SYM] stock news this week"`
2. Analyze sentiment natively
3. `test_conviction_with_sentiment(SYM, thesis, holding, agentic_sentiment)`

`agentic_sentiment` keys: `overall` (positive/negative/neutral/mixed), `positive_count`, `negative_count`, `key_findings[]`, `risks_mentioned[]`