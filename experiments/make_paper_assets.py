"""Generate every figure (PDF) and every numeric table (LaTeX) of the manuscript
directly from the result CSVs. No number in the paper is typed by hand."""
import sys, os, csv, statistics as st
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from hcadse.model import (make_space, WORKLOADS, EDGE_CLASSES, GW_CLASSES,
                          CLOUD_CLASSES, LINK_CLASSES, POLICIES, VAR_ORDER)
from hcadse.search import hca_dse

F, T = "manuscript/figures", "manuscript/tables"
os.makedirs(F, exist_ok=True); os.makedirs(T, exist_ok=True)
plt.rcParams.update({"font.size": 8, "font.family": "serif", "axes.grid": True,
                     "grid.alpha": .25, "grid.linewidth": .4, "savefig.bbox": "tight"})
WL = ["telemetry", "control", "sensing"]
CLR = {"telemetry": "#1f4e79", "control": "#c0504d", "sensing": "#e08214"}
R = lambda f: list(csv.DictReader(open(f)))


def tab(name, body, colspec=None, header=None, pre="", post=""):
    """Write a COMPLETE tabular environment: \input inside a tabular is fragile,
    so the generated file is self-contained."""
    if colspec is None:
        open(f"{T}/{name}.tex", "w").write(body)
    else:
        out = (pre + "\\begin{tabular}{" + colspec + "}\n\\toprule\n" +
               header + "\n\\midrule\n" + body + "\n\\bottomrule\n"
               "\\end{tabular}\n" + post)
        open(f"{T}/{name}.tex", "w").write(out)
    print("table", name)


def fig(name, f):
    f.savefig(f"{F}/{name}.pdf"); plt.close(f); print("figure", name)


# ---------------------------------------------------------------- T3 variables
rows = []
sp = {s: make_space(s) for s in ("S1", "S2", "S3", "S4")}
desc = {"n_e": "number of edge nodes", "edge_cls": "edge node class",
        "n_g": "number of gateways", "gw_cls": "gateway class",
        "link_cls": "access link class", "cloud_cls": "cloud instance class",
        "rep": "replication factor of stage 1", "policy": "placement policy"}
for v in VAR_ORDER:
    doms = [len(sp[s].domain(v)) for s in ("S1", "S2", "S3", "S4")]
    rows.append(f"$\\mathit{{{v.replace('_',chr(92)+'_')}}}$ & {desc[v]} & "
                + " & ".join(str(d) for d in doms) + r" \\")
tab("variables", "\n".join(rows) + "\n\\midrule\n\\multicolumn{2}{l}{\\emph{design-space size} "
    r"$|\mathcal{X}|$} & " + " & ".join(f"{sp[s].size:,}".replace(",", r"\,")
                                        for s in ("S1", "S2", "S3", "S4")) + r" \\",
    colspec="llrrrr", header=r"variable & meaning & S1 & S2 & S3 & S4 \\",
    pre="\\scriptsize\n")

# ---------------------------------------------------------------- T4 workloads
rows = []
for n in WL:
    w = WORKLOADS[n]
    s = w.stages
    rows.append(f"{n} & {w.n_dev} & {w.rate:g} & {w.Lambda:g} & "
                f"{s[0].w:g}/{s[1].w:g}/{s[2].w:g} & "
                f"{1000*s[0].s_in:g}/{1000*s[1].s_in:g}/{1000*s[2].s_in:g} & "
                f"{1000*w.deadline:g} & {w.C_max:g}" + r" \\")
tab("workloads", "\n".join(rows), colspec="lrrrrrrr",
    header=(r"workload & $n_d$ & $\lambda$ & $\Lambda$ & $w_i$ [MI] & $s_i$ [kB] & "
            r"$D$ [ms] & $C^{\max}$ \\"), pre="\\scriptsize\n")

# ---------------------------------------------------------------- T5 resources
rows = [r"\multicolumn{6}{l}{\emph{compute node classes}} \\"]
for c in EDGE_CLASSES + GW_CLASSES + CLOUD_CLASSES:
    rows.append(f"{c.name} & {c.C:g} & {c.M:g} & {c.P_idle:g} & {c.P_peak:g} & {c.cost:g}" + r" \\")
rows.append(r"\midrule \multicolumn{6}{l}{\emph{link classes} (name, $B$ [Mb/s], "
            r"$\tau$ [ms], $e$ [J/MB], cost)} \\")
for l in LINK_CLASSES:
    rows.append(f"{l.name} & {l.B:g} & {1000*l.prop:g} & {l.e:g} & {l.cost:g} & --" + r" \\")
tab("resources", "\n".join(rows), colspec="lrrrrr",
    header=(r"class & $C$ / $B$ & $M$ / $\tau$ & $P^{\mathrm{idle}}$ / $e$ & "
            r"$P^{\mathrm{peak}}$ & cost \\"), pre="\\scriptsize\n")

# ---------------------------------------------------------------- T6 funnel
d = R("results/e1_pruning.csv")
rows = []
for s in ("S1", "S2", "S3", "S4"):
    for w in WL:
        r = [q for q in d if q["scale"] == s and q["workload"] == w][0]
        red = 100 * (1 - int(r["evals"]) / int(r["raw"]))
        ex = r.get("exh_evals") or ""
        rows.append(f"{s} & {w} & {int(r['raw']):,} & {int(r['pruned_struct']):,} & "
                    f"{int(r['pruned_bound']):,} & {int(r['pruned_dom']):,} & "
                    f"{r['evals']} & {r['feasible']} & {r['pareto']} & {red:.2f} & "
                    + (f"{int(ex):,}" if ex else "--") + " & "
                    + (r.get("recall") or "--") + r" \\")
tab("funnel", "\n".join(rows).replace(",", r"\,"), colspec="llrrrrrrrrrr",
    header=(r"scale & workload & $|\mathcal{X}|$ & structural & feasibility & dominance & "
            r"full & feasible & $|\mathcal{P}|$ & reduction & exhaustive & recall \\"
            "\n" r" & & & pruned & pruned & pruned & evals & & & [\%] & evals & \\"),
    pre="\\scriptsize\n\\setlength{\\tabcolsep}{3.5pt}\n")

# ---------------------------------------------------------------- T7 baselines
d = R("results/e3_baselines.csv")
rows = []
for scale in ("S2", "S3"):
    for w in WL:
        sub = [r for r in d if r["scale"] == scale and r["workload"] == w]
        e = [r for r in sub if r["method"] == "exhaustive"][0]
        h = [r for r in sub if r["method"] == "HCA-DSE"][0]
        rows.append(f"\\multirow{{10}}{{*}}{{{scale}}} & \\multirow{{10}}{{*}}{{{w}}} & "
                    f"exhaustive & {int(e['n_eval']):,} & 1.000 & 1.000 & 0.0000 & {float(e['runtime']):.3f}" + r" \\")
        for m, lab in (("random", "random"), ("nsga2", "NSGA-II")):
            for b in (100, 250, 500, 1000):
                s = [r for r in sub if r["method"] == m and int(r["budget"]) == b and r["seed"]]
                rows.append(f" & & {lab} ($B$={b}) & {b} & "
                            f"{st.median(float(r['recall']) for r in s):.3f} & "
                            f"{st.median(float(r['hv_ratio']) for r in s):.3f} & "
                            f"{st.median(float(r['igd_plus']) for r in s):.4f} & "
                            f"{st.median(float(r['runtime']) for r in s):.3f}" + r" \\")
        rows.append(f" & & \\textbf{{HCA-DSE}} & \\textbf{{{h['n_eval']}}} & "
                    f"\\textbf{{1.000}} & \\textbf{{1.000}} & \\textbf{{0.0000}} & "
                    f"{float(h['runtime']):.3f}" + r" \\")
        rows.append(r"\midrule")
tab("baselines", "\n".join(rows[:-1]).replace(",", r"\,"), colspec="lllrrrrr",
    header=(r"scale & workload & method & evals & recall & HV ratio & IGD$^{+}$ & "
            r"time [s] \\"), pre="\\scriptsize\n")

# ---------------------------------------------------------------- T8 ablation
d = [r for r in R("results/e4_ablation.csv") if r["scale"] == "S3"]
names = {"structural-only": "structural only",
         "struct+feasibility": "structural + feasibility bounds",
         "struct+dominance": "structural + dominance bounds",
         "HCA-full": "\\textbf{HCA-DSE (all layers)}"}
rows = []
for v in ("structural-only", "struct+feasibility", "struct+dominance", "HCA-full"):
    cells = []
    for w in WL:
        r = [q for q in d if q["workload"] == w and q["variant"] == v][0]
        cells += [f"{int(r['nodes']):,}", f"{int(r['evals']):,}", f"{float(r['t'])*1000:.0f}"]
    rows.append(names[v] + " & " + " & ".join(cells) + r" \\")
tab("ablation", "\n".join(rows).replace(",", r"\,"), colspec="lrrrrrrrrr",
    header=(r"& \multicolumn{3}{c}{telemetry} & \multicolumn{3}{c}{control} & "
            r"\multicolumn{3}{c}{sensing} \\" "\n"
            r"\cmidrule(lr){2-4}\cmidrule(lr){5-7}\cmidrule(lr){8-10}" "\n"
            r"variant & states & evals & [ms] & states & evals & [ms] & states & evals & [ms] \\"),
    pre="\\scriptsize\n\\setlength{\\tabcolsep}{3.5pt}\n")

# ---------------------------------------------------------------- T9 scalability
d = R("results/e5_scalability.csv")
rows = []
for raw in sorted({int(r["raw"]) for r in d}):
    cells = []
    for w in WL:
        r = [q for q in d if int(q["raw"]) == raw and q["workload"] == w][0]
        cells += [f"{int(r['nodes']):,}", r["evals"], f"{float(r['runtime']):.2f}"]
    import math
    ex = int(math.log10(raw)); mant = raw / 10 ** ex
    rows.append(f"$\\mathbf{{{mant:.1f}\\times 10^{{{ex}}}}}$ & ".replace("\\mathbf", "")
                + " & ".join(cells) + r" \\")
tab("scalability", "\n".join(rows).replace(",", r"\,"), colspec="lrrrrrrrrr",
    header=(r"& \multicolumn{3}{c}{telemetry} & \multicolumn{3}{c}{control} & "
            r"\multicolumn{3}{c}{sensing} \\" "\n"
            r"\cmidrule(lr){2-4}\cmidrule(lr){5-7}\cmidrule(lr){8-10}" "\n"
            r"$|\mathcal{X}|$ & states & evals & [s] & states & evals & [s] & states & evals & [s] \\"),
    pre="\\scriptsize\n\\setlength{\\tabcolsep}{3.5pt}\n")

# ---------------------------------------------------------------- T10 testbed
d = R("results/e9_summary_docker.csv")
rows = []
lab = {"all": "all", "rho<=0.75": "$\\rho\\le0.75$", "reproducible": "reproducible"}
for w in WL + ["ALL"]:
    for sub in ("all", "rho<=0.75", "reproducible"):
        r = [q for q in d if q["workload"] == w and q["subset"] == sub]
        if not r:
            continue
        r = r[0]
        name = ("\\textbf{all workloads}" if w == "ALL" else w) + f" ({lab[sub]})"
        rows.append(f"{name} & {r['n']} & {r['MAPE']} & {r['median_AE_ms']} & "
                    f"{r['spearman']} & {r['kendall']} & {r['agree_10pct']} & "
                    f"{r['agree_25pct']} & {r['median_repeat_iqr_ms']}" + r" \\")
tab("testbed", "\n".join(rows), colspec="lrrrrrrrr",
    header=(r"subset & $n$ & MAPE & med.\ AE & Spearman & Kendall & pair & pair & repeat \\"
            "\n" r" & & [\%] & [ms] & $\rho$ & $\tau$ & $>10\%$ & $>25\%$ & spread [ms] \\"),
    pre="\\scriptsize\n\\setlength{\\tabcolsep}{3pt}\n")

# ================================================================= FIGURES
# F: funnel
d = R("results/e1_pruning.csv")
f, ax = plt.subplots(figsize=(5.4, 2.3))
x = 0; ticks = []
for s in ("S1", "S2", "S3", "S4"):
    for w in WL:
        r = [q for q in d if q["scale"] == s and q["workload"] == w][0]
        raw = int(r["raw"]); a = raw - int(r["pruned_struct"])
        b = a - int(r["pruned_bound"]); c = int(r["evals"])
        for val, col in ((raw, "#d9d9d9"), (a, "#a6bddb"), (b, "#3690c0"), (c, "#023858")):
            ax.bar(x, val, color=col, width=.8)
        ticks.append((x, f"{s}\n{w[:4]}")); x += 1
    x += .6
ax.set_yscale("log"); ax.set_xticks([t[0] for t in ticks])
ax.set_xticklabels([t[1] for t in ticks], fontsize=5.5)
ax.set_ylabel("architectures (log scale)")
ax.set_ylim(top=10 ** 6.6)
ax.legend(["raw design space", "after structural pruning", "after feasibility bounds",
           "fully evaluated"], fontsize=5.5, ncol=4, loc="upper center",
          frameon=False, borderpad=0.1, columnspacing=1.0)
fig("funnel", f)

# F: cost crossover
d = R("results/e2_costsweep.csv")
f, ax = plt.subplots(figsize=(3.3, 2.4))
for s, ls in (("S2", "--"), ("S3", "-")):
    for w in WL:
        sub = sorted([r for r in d if r["scale"] == s and r["workload"] == w],
                     key=lambda r: float(r["C_E"]))
        ax.plot([float(r["C_E"]) for r in sub], [float(r["speedup"]) for r in sub],
                ls, color=CLR[w], lw=1, marker="o", ms=2, label=f"{s}, {w}")
ax.axvline(19.4e-3, color="k", lw=.7, ls=":")
ax.text(2.2e-2, 1.6, "measured DES\nevaluator", fontsize=5)
ax.axhline(1, color="grey", lw=.5)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("evaluation cost $C_E$ [s]"); ax.set_ylabel("speed-up over exhaustive")
ax.legend(fontsize=5, ncol=2)
fig("crossover", f)

# F: scalability
d = R("results/e5_scalability.csv")
f, ax = plt.subplots(figsize=(3.3, 2.4))
for w in WL:
    sub = sorted([r for r in d if r["workload"] == w], key=lambda r: int(r["raw"]))
    X = [int(r["raw"]) for r in sub]
    ax.plot(X, [int(r["nodes"]) for r in sub], "-o", ms=2.5, lw=1, color=CLR[w],
            label=f"{w}: partial states")
    ax.plot(X, [int(r["evals"]) for r in sub], "--s", ms=2.5, lw=1, color=CLR[w],
            label=f"{w}: full evaluations")
ax.plot(X, X, color="k", lw=.8, label="exhaustive")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel(r"raw design space $|\mathcal{X}|$"); ax.set_ylabel("count")
ax.legend(fontsize=5, ncol=1)
fig("scalability", f)

# F: HV vs budget
d = R("results/e3_baselines.csv")
f, axes = plt.subplots(1, 3, figsize=(5.6, 1.9), sharey=True)
for ax, w in zip(axes, WL):
    bs = [100, 250, 500, 1000]
    for m, c, off in (("random", "#bdbdbd", -0.18), ("nsga2", "#3690c0", 0.18)):
        data = [[float(r["hv_ratio"]) for r in d if r["scale"] == "S3" and r["workload"] == w
                 and r["method"] == m and int(r["budget"]) == b and r["seed"]] for b in bs]
        ax.boxplot(data, positions=[i + off for i in range(len(bs))], widths=.3,
                   patch_artist=True, boxprops=dict(facecolor=c, lw=.4),
                   medianprops=dict(color="k", lw=.7), whiskerprops=dict(lw=.4),
                   capprops=dict(lw=.4), flierprops=dict(ms=1))
    h = [r for r in d if r["scale"] == "S3" and r["workload"] == w and r["method"] == "HCA-DSE"][0]
    ax.axhline(1.0, color="#c0504d", lw=1)
    ax.set_xticks(range(len(bs))); ax.set_xticklabels(bs, fontsize=6)
    ax.set_title(f"{w} — HCA-DSE: {h['n_eval']} evals, HV$=1$", fontsize=6)
    ax.set_xlabel("evaluation budget", fontsize=7)
axes[0].set_ylabel("HV ratio", fontsize=7)
fig("hv_budget", f)

# F: ablation
d = [r for r in R("results/e4_ablation.csv") if r["scale"] == "S3"]
f, ax = plt.subplots(figsize=(3.3, 2.2))
vs = ["structural-only", "struct+feasibility", "struct+dominance", "HCA-full"]
for i, w in enumerate(WL):
    ys = [int([r for r in d if r["workload"] == w and r["variant"] == v][0]["evals"]) for v in vs]
    ax.bar([j + (i - 1) * .27 for j in range(len(vs))], ys, width=.26, color=CLR[w], label=w)
ax.set_yscale("log"); ax.set_xticks(range(len(vs)))
ax.set_xticklabels(["structural\nonly", "+ feasibility\nbounds", "+ dominance\nbounds",
                    "HCA-DSE\n(all)"], fontsize=5.5)
ax.set_ylabel("full evaluations (S3)"); ax.legend(fontsize=6)
fig("ablation", f)

# F: Pareto front projections (S3, telemetry)
front = hca_dse(make_space("S3"), WORKLOADS["telemetry"]).front
L = [f_[0] * 1e3 for _, f_ in front]; E = [f_[1] / 3.6e6 for _, f_ in front]
C = [f_[2] for _, f_ in front]; D = [f_[3] for _, f_ in front]
f, axs = plt.subplots(1, 2, figsize=(5.4, 2.1))
sc = axs[0].scatter(L, C, c=D, s=18, cmap="viridis")
axs[0].set_xlabel("latency [ms]"); axs[0].set_ylabel("cost [units]")
f.colorbar(sc, ax=axs[0], label="network volume [MB/s]")
sc = axs[1].scatter(L, E, c=C, s=18, cmap="plasma")
axs[1].set_xlabel("latency [ms]"); axs[1].set_ylabel("energy [kWh per hour-equivalent]")
f.colorbar(sc, ax=axs[1], label="cost [units]")
fig("pareto", f)

# F: model vs measurement (Docker testbed)
d = R("results/e9_per_design_docker.csv")
f, ax = plt.subplots(figsize=(3.2, 2.9))
for w, mk in zip(WL, "ov^"):
    lo = [r for r in d if r["workload"] == w and float(r["spread"]) < 1.5]
    hi = [r for r in d if r["workload"] == w and float(r["spread"]) >= 1.5]
    ax.scatter([float(r["p50_measured"]) * 1e3 for r in lo],
               [float(r["L_analytical"]) * 1e3 for r in lo], s=14, marker=mk,
               color=CLR[w], label=w)
    ax.scatter([float(r["p50_measured"]) * 1e3 for r in hi],
               [float(r["L_analytical"]) * 1e3 for r in hi], s=26, marker=mk,
               facecolors="none", edgecolors="k", linewidths=.7)
lim = [5, 2500]
ax.plot(lim, lim, "k--", lw=.7); ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(*lim); ax.set_ylim(*lim)
ax.set_xlabel("measured median $p_{50}$ latency [ms]")
ax.set_ylabel("analytical latency [ms]")
ax.set_title("open markers: repeat spread $\\geq 1.5\\times$", fontsize=6)
ax.legend(fontsize=6)
fig("testbed", f)
print("done")
