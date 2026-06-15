# Agentic News Discovery

**Use the agent's native tools for news — not `dr.py news` or `scripts/news.py`.** Those RSS/keyword paths are deprecated.

Modern models can search multiple sources, read full articles, and adapt to context. Use that instead of brittle keyword matching.

## Default: `web_search`

```
web_search: "[COMPANY] stock news today"
web_search: "[COMPANY] earnings [QUARTER]"
web_search: "[COMPANY] [EVENT] impact"
```

For Thai stocks:

```
web_search: "[THAI COMPANY] ข่าวหุ้น ล่าสุด"
```

## Deep dive: `agent_browser`

Open specific pages for detailed research:

- Investor relations / earnings press releases
- SEC filings (10-K, 10-Q)
- SET or SEC Thailand filings
- Reddit, Twitter/X for retail sentiment

## When to use each

| Need | Tool |
|------|------|
| Quick pulse check | `web_search` x2-3 |
| Event impact (earnings, WWDC) | `web_search` + synthesis |
| Deep research before buy/sell | `agent_browser` open links |
| Thai stock with limited English | `web_search` + Thai terms |
| Sentiment from discussions | `web_search` for Reddit/Twitter |

## Conviction test (agentic)

`conviction_test.py` tests whether an investment thesis is still valid.

**Keep as script:** price performance (1Y return), P&L from buy price, verdict algorithm (INTACT/DAMAGED/BROKEN/UNCERTAIN).

**Agentic news:** use `web_search` for sentiment, then call `test_conviction_with_sentiment()`:

```
1. web_search: "[SYM] stock news this week"
2. Analyze sentiment natively (context, nuance, risks)
3. Call conviction test with results:
   agentic_sentiment = {
       "overall": "positive",  # positive/negative/neutral/mixed
       "positive_count": 5,
       "negative_count": 1,
       "key_findings": ["AI growth", "earnings beat"],
       "risks_mentioned": ["competition"]
   }
   test_conviction_with_sentiment(SYM, thesis, holding, agentic_sentiment)
```

## Data sources

Price and fundamental feeds are documented in [DATA-SOURCES](DATA-SOURCES.md). Use those for numbers; use agentic tools for news and narrative context.