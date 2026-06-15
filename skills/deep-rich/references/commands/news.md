# news (deprecated)

> **Deprecated.** Do not use `dr.py news` or `scripts/news.py`. Use agentic tools per [AGENTIC-NEWS](../AGENTIC-NEWS.md).

This file remains as a historical reference for the old RSS + keyword-matching approach.

## Replacement workflow

1. `web_search` for recent coverage (see [AGENTIC-NEWS](../AGENTIC-NEWS.md))
2. Native sentiment analysis (context, nuance, risks)
3. For conviction tests: `test_conviction_with_sentiment()` with agentic results

## Why deprecated

- Keyword matching misses context and nuance
- Google News RSS coverage is thin for Thai stocks
- Agentic search + browser tools outperform static RSS for disruption checks