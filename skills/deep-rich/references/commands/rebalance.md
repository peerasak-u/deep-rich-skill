# rebalance

Mechanical (hit targets) or rotate (losers → opportunity).

## When

- Quarterly mechanical; drift >15% any class
- User spots opportunity to rotate
- "should I rebalance" / "how do I fix my allocation"

## Modes

| Mode | Command |
|------|---------|
| Mechanical | `dr rebalance mechanical` — sell overweight, buy underweight |
| Rotate | `dr rebalance rotate` — losers → new trend |

## Mechanical

1. `dr portfolio` + `dr health watchlist` + `dr deployment`
2. Sell: class overweight >15%; health F; D + loss >20%
3. Buy: class underweight; cash excess → underweight classes
4. Calc per class: current% vs target%, ฿ delta, trades
5. Synth: sells → buys → net effect → tax/transaction notes

## Rotate

1. User: rotate from [losers] to [opportunity]
2. `dr portfolio` + `dr health watchlist` — F = strong sell; D + loss >20%; underperform >−20%
3. `dr research <SYM>` or `dr fundamentals` + `dr health` on opportunity stocks
4. Calc: sell losers, buy opportunity, check diversification
5. Synth: sell losers → buy opportunity → net effect → thesis → risk check

## Output skeleton

```
⚖️/🔄 Rebalancing — [Mechanical|Rotate]
Sells: [positions + ฿ + reason]
Buys: [positions + ฿ + reason]
Net Effect: [allocation change]
Risk/Tax: [notes]
```

## Guards

[GUARDS](../GUARDS.md) + !over-trade small drifts; tax on sells; diversify themes; new stocks → research first.