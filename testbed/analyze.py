"""Gate 10 analysis: accuracy (MAPE) and, more importantly, ranking agreement."""
import sys, os, csv, json, statistics, argparse
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import spearmanr, kendalltau

ap = argparse.ArgumentParser()
ap.add_argument("--input", default="results/e9_testbed_local.csv")
ap.add_argument("--designs", default="testbed/specs/designs_local.json")
ap.add_argument("--tag", default="local")
a = ap.parse_args()

designs = json.load(open(a.designs))
rows = [r for r in csv.DictReader(open(a.input)) if r["ok"] == "True"]
by = {}
for r in rows:
    by.setdefault((r["workload"], int(r["design_idx"])), []).append(r)

out = []
for (w, i), rs in sorted(by.items()):
    med = statistics.median(float(r["p50"]) for r in rs)
    p95 = statistics.median(float(r["p95"]) for r in rs)
    d = [x for x in designs if x["workload"] == w][0] if False else designs[i]
    rho = max(d["rho"].values())
    out.append(dict(workload=w, design=i, kind=rs[0]["kind"], policy=rs[0]["policy"],
                    n_e=rs[0]["n_e"], max_rho=round(rho, 3),
                    L_analytical=float(rs[0]["L_analytical"]), p50_measured=round(med, 6),
                    p95_measured=round(p95, 6), repeats=len(rs),
                    iqr_ms=round(1000 * (max(float(r["p50"]) for r in rs) -
                                         min(float(r["p50"]) for r in rs)), 2),
                    rel_err=round((float(rs[0]["L_analytical"]) - med) / med, 3)))

def stats(sub, label):
    an = [r["L_analytical"] for r in sub]; me = [r["p50_measured"] for r in sub]
    return dict(subset=label, n=len(sub),
                MAPE=round(100 * statistics.mean(abs((x - y) / y) for x, y in zip(an, me)), 1),
                median_AE_ms=round(1000 * statistics.median(abs(x - y) for x, y in zip(an, me)), 2),
                spearman=round(float(spearmanr(an, me).correlation), 3),
                kendall=round(float(kendalltau(an, me).correlation), 3))

summary = []
for w in sorted({r["workload"] for r in out}):
    sub = [r for r in out if r["workload"] == w]
    stable = [r for r in sub if r["max_rho"] <= 0.75]
    summary.append(dict(workload=w, **stats(sub, "all")))
    if len(stable) >= 5:
        summary.append(dict(workload=w, **stats(stable, "rho<=0.75")))
allr = out
summary.append(dict(workload="ALL", **stats(allr, "all")))
summary.append(dict(workload="ALL", **stats([r for r in allr if r["max_rho"] <= 0.75], "rho<=0.75")))
for s in summary:
    print(s)
with open(f"results/e9_summary_{a.tag}.csv", "w", newline="") as f:
    w_ = csv.DictWriter(f, sorted(summary[0])); w_.writeheader(); w_.writerows(summary)
with open(f"results/e9_per_design_{a.tag}.csv", "w", newline="") as f:
    w_ = csv.DictWriter(f, sorted(out[0])); w_.writeheader(); w_.writerows(out)

fig, ax = plt.subplots(figsize=(3.5, 3.2), dpi=200)
for w, mk in zip(sorted({r["workload"] for r in out}), "osv"):
    sub = [r for r in out if r["workload"] == w]
    hi = [r for r in sub if r["max_rho"] > 0.75]; lo = [r for r in sub if r["max_rho"] <= 0.75]
    ax.scatter([r["p50_measured"] * 1e3 for r in lo], [r["L_analytical"] * 1e3 for r in lo],
               s=12, marker=mk, label=w)
    ax.scatter([r["p50_measured"] * 1e3 for r in hi], [r["L_analytical"] * 1e3 for r in hi],
               s=22, marker=mk, facecolors="none", edgecolors="crimson", linewidths=0.8)
lim = [3, 4000]; ax.plot(lim, lim, "k--", lw=0.8)
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(*lim); ax.set_ylim(*lim)
ax.set_xlabel("measured p50 latency [ms]"); ax.set_ylabel("analytical latency [ms]")
ax.set_title("open markers: $\\rho>0.75$", fontsize=6)
ax.legend(fontsize=6); fig.savefig(f"figures/fig7_testbed_{a.tag}.png", bbox_inches="tight")
print(f"written results/e9_summary_{a.tag}.csv, results/e9_per_design_{a.tag}.csv, "
      f"figures/fig7_testbed_{a.tag}.png")
