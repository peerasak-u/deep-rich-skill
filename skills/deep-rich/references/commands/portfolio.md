# portfolio

Overview + allocation drift.

```bash
python3 scripts/dr.py portfolio
python3 scripts/dr.py portfolio --snapshot   # save to SQLite snapshots
python3 scripts/dr.py portfolio --history    # last 10 snapshots
```

Output: total ฿/$, USD/THB, floor, deployable, per-class value/%/target/drift (🟢<5% 🟡5–15% 🔴>15%).

Live prices: crypto, FX, US, Thai (`.BK`). Drift rules → [RULES](../RULES.md#drift).