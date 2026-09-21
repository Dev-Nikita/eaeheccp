"""E13: how far can a model-based design decision be trusted?

For every pair of deployed architectures of the same workload, the analytical model
predicts which of the two is faster. This script reports the share of pairs whose
measured order (mean latency over three runs, the main-text metric) matches the predicted
order, as a function of how far apart the model places the two architectures. No model
parameter is fitted here: predictions come from the model frozen before deployment.
Pairs are counted within workloads only; the pooled figure sums within-workload pairs.
Intervals are Wilson 95% score intervals on the pair counts; pairs share designs and are
therefore not independent, so the intervals are indicative rather than exact.
"""
import csv, math, os, sys
THRESHOLDS = [0.0, 0.05, 0.10, 0.15, 0.25, 0.50, 1.00]
SRC = os.environ.get('HCADSE_RESULTS', 'results') + '/e9_per_design_mean.csv'

def wilson(k, n, z=1.96):
    if n == 0:
        return float('nan'), float('nan')
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

def counts(sub, thr):
    ok = tot = 0
    for i in range(len(sub)):
        for j in range(i + 1, len(sub)):
            a, b = sub[i], sub[j]
            la, lb = float(a['L_analytical']), float(b['L_analytical'])
            if abs(la - lb) / min(la, lb) <= thr:
                continue
            tot += 1
            ok += (la - lb) * (float(a['p50_measured']) - float(b['p50_measured'])) > 0
    return ok, tot

rows = list(csv.DictReader(open(SRC)))
wls = sorted({r['workload'] for r in rows})
out = []
for subset, keep in (('all', lambda r: True), ('reproducible', lambda r: float(r['spread']) < 1.5)):
    for thr in THRESHOLDS:
        pooled_ok = pooled_tot = 0
        for w in wls + ['pooled']:
            if w == 'pooled':
                ok, tot = pooled_ok, pooled_tot
            else:
                ok, tot = counts([r for r in rows if r['workload'] == w and keep(r)], thr)
                pooled_ok += ok; pooled_tot += tot
            lo, hi = wilson(ok, tot)
            out.append(dict(subset=subset, threshold=thr, workload=w, agree=ok, pairs=tot,
                            agreement=round(ok / tot, 4) if tot else '',
                            ci_low=round(lo, 4) if tot else '', ci_high=round(hi, 4) if tot else ''))
with open('results/e13_reliability.csv', 'w', newline='') as f:
    w_ = csv.DictWriter(f, list(out[0])); w_.writeheader(); w_.writerows(out)
for r in out:
    if r['workload'] == 'pooled':
        print(r)
print('written results/e13_reliability.csv')
