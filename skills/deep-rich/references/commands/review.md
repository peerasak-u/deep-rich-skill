# review

Weekly portfolio ritual — health check + specific actions.

## When

- Weekly (check `.deep-rich/reviews/` last date)
- "how's my portfolio" / "what should I do" / "review"
- >7 days since last review → remind

## Steps

1. **Gather:** `dr portfolio` | `dr health watchlist` | `dr performance` | `dr deployment`
2. **Profit-take:** [RULES profit table](../RULES.md#profit-taking). Show: gain %/฿ | trim 25/50% proceeds | deploy target | macro | health highlights/warnings | thesis | conviction checklist (thesis valid? margins? catalyst? valuation?)
3. **Loss-cut:** [RULES loss table](../RULES.md#loss-cutting). Show: loss %/฿ | recovery | macro | health | thesis why broken | checklist failures | grade meaning
4. **Drift:** [RULES drift](../RULES.md#drift). 🔴 >15% → rebalance amounts; 🟡 5–15% mention; 🟢 <5% OK. Cash > target → deployable above floor
5. **Synth order:** header (portfolio ฿, vs last week) → profit candidates → loss candidates → drift → numbered actions
6. **HTML:** resolve logos `.deep-rich/companies/<SYM>.json.logo.path` → `.deep-rich/company-assets/logos/<sym>.{png,webp,jpg,svg}`; !hotlink. Use in profit/loss/holdings cards + tables. `dr export-review < review-data.json --open`
7. **Save:** `.deep-rich/reviews/YYYY-MM-DD.md` summary
8. **Journal:** user agrees action → append `.deep-rich/journal.md` (NSL lesson: no journal = no record)

## Review JSON keys

`date`, `portfolio{total_thb,total_usd,all_time_return,fx_rate}`, `profit_take[]`, `loss_cut[]`, `holdings_action[]`, `drift[]{class,current_pct,target_pct}`, `deployment{deployable}`, `actions[]`, `notes[]`

Per-stock memo keys: `symbol`, `gain_pct`, `position_label`, `logo_path`, `logo_source`, `action`, `proceeds`, `reason`, `macro_context[]{claim,source}`, `research{grade,highlights[],warnings[]}`, `conviction{thesis,level,original_date}`, `checklist[]{label,pass}`

## Output skeleton

```
📋 Weekly Review — [Date]
Portfolio ฿X (+Y% all-time) | vs last week ฿±X
Profit-Taking: [>50% with trim suggestion]
Loss-Cutting: [F/D with cut suggestion]
Drift: [class current vs target + deployable cash]
Suggested Actions: [numbered with ฿]
```

## Guards

[GUARDS](../GUARDS.md) + !sell pressure if user wants to hold winner — mention option only.