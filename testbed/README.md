# Gate 10 — physical edge/gateway/cloud testbed

```bash
python3 testbed/select_designs.py          # 36 архитектур (Pareto/dominated/boundary)
python3 testbed/run_testbed.py --repeats 3 # ~40-60 мин, пишет results/e9_testbed.csv
python3 testbed/analyze.py                 # MAPE, Spearman, Kendall, figures/fig7_testbed.png
```

