# deployment

Allocate excess cash to underweight classes.

```bash
python3 scripts/dr.py deployment
```

Logic: deployable = cash − floor (฿300k default in `config.json`); underweight classes (drift <0) get proportional allocation; exclude Cash + Gold.

Recommend DCA 3–6 months. Guards → [GUARDS](../GUARDS.md).