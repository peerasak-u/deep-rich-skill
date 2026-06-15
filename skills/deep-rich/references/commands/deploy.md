# deploy

Deploy idle cash from drift + market context.

## When

- Extra cash (salary, bonus, sale)
- "what should I buy" / "where should I put it" / during review

## Steps

1. `dr portfolio` + `dr deployment` — cash, floor ฿300k, deployable = cash − floor
2. Drift — cash > target → deploy excess; class < target → candidate
3. Rules: never below floor; proportional to drift; exclude Gold (passive) + Cash (source)
4. User mentions opportunity → `web_search` theme; else mechanical allocation
5. Synth: cash/floor/deployable → allocation by class → suggested stocks → DCA 3–6 months

## Output skeleton

```
🚀 Deployment Plan
Cash ฿X | Floor ฿300k | Deployable ฿Y
Allocation: Thai SET ฿… | US ฿… | Crypto ฿…
Suggested: [stocks or mechanical]
Timeline: DCA over 3–6 months
```

## Guards

[GUARDS](../GUARDS.md) + DCA (!lump sum); diversify themes; specific stocks → `research` first; !FOMO.