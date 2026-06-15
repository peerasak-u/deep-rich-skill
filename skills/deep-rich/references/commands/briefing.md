# briefing

Event-driven pulse — what happened to YOUR portfolio. Not weekly review (→ `review`).

## When

- After market events (earnings, WWDC, Fed, geopolitical)
- "what happened" / "any news" / event may affect holdings

## Steps

1. `dr portfolio` — extract owned symbols
2. `dr prices` + `dr performance` — flag moves >5% day or since last check
3. News per [AGENTIC-NEWS](../AGENTIC-NEWS.md) — big movers first, then user event; YOUR holdings only; 2–3 searches/holding; browser only to verify headline
4. Synth order: header → since last check (portfolio Δ) → big moves → news that matters → action needed?

## Output skeleton

```
📰 Briefing — [Event/Date]
Since last check: portfolio ฿±X (±Y%)
Big Moves: [>5% holdings]
News That Matters: [owned symbols only]
Action Needed?: [buy/sell/hold/none + reason]
```

## Guards

[GUARDS](../GUARDS.md) + don't alarm (3% ≠ crisis); filter noise; say clearly if no action; keep quick (~30s read).