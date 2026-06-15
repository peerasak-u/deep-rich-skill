# risk

What could hurt the portfolio.

## When

- Monthly check; "what's my risk" / "what could go wrong"
- Before large allocation change; after crash/rotation

## Steps

1. `dr portfolio` + `dr health watchlist` + `dr performance`
2. **Conc:** single stock >5% port, >15% class, sector >30%, correlated holdings
3. **Quality:** any F-grade; D-grade >10% port; declining revenue; D/E >2.0
4. **Market:** 52W >90% (overbought?), <10% (value trap?); 20% correction drawdown >15% port
5. Synth: conc → quality → market → risk score + mitigation

## Output skeleton

```
⚠️ Risk Report
Concentration: [flags]
Quality: [F/D holdings, % at risk]
Market: [52W position, correction impact]
Risk Score: 🟢/🟡/🔴 + main risk + suggested mitigation
```

## Guards

[GUARDS](../GUARDS.md) + moderate risk normal; show context; suggest mitigation; respect tolerance.