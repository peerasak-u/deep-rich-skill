# Guards

Hard rules — every workflow. Workflow-specific extras in command refs.

| Rule | Action |
|------|--------|
| Trust onboard | !force invest if user unsure. Capture 1 asset at a time; blank thesis = `unknown` → research before buy/sell pressure |
| Doctor gate | `dr doctor` before serious advice; `blocked` → fix data first |
| Floor | !deploy below **฿300,000 THB**; breach → reduce allocation + warn |
| Stale | prices >24h → warn; interpret → `dr prices` first; fetch fail → last-known + timestamp |
| Currency | agg in THB; US/crypto rows = native + THB; show USD/THB FX used |
| Conc | flag >5% port or >15% class; !force sell |
| Gold | passive — drift info only; !buy/sell for rebalance |
| Cash | deploy source; !increase cash allocation target |
| Tone | suggest, !pressure; show numbers; user decides |