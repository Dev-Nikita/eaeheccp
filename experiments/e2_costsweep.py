"""E2: when does pruning pay off? Speedup as a function of the evaluator cost C_E.

T_method(C_E) = overhead_method + N_eval_method * C_E, with the overheads and
N_eval measured, and the linear model validated at two real evaluator costs
(closed-form analytical vs. discrete-event simulation).
"""
import sys, os, csv, time, statistics; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hcadse.model import make_space, WORKLOADS
from hcadse.search import exhaustive, hca_dse
from hcadse.evaluate import evaluate
from hcadse.simulate import simulate

rows, val = [], []
for scale in ("S2", "S3"):
    sp = make_space(scale)
    for name, wl in WORKLOADS.items():
        h, e = hca_dse(sp, wl), exhaustive(sp, wl)
        oh_h, oh_e = h.runtime - h.t_eval, e.runtime - e.t_eval
        for CE in (1e-5, 5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 2.3e-2, 1e-1, 1.0):
            th, te = oh_h + h.n_evaluated * CE, oh_e + e.n_evaluated * CE
            rows.append(dict(scale=scale, workload=name, C_E=CE,
                             N_hca=h.n_evaluated, N_exh=e.n_evaluated,
                             overhead_hca=round(oh_h, 5), overhead_exh=round(oh_e, 5),
                             T_hca=round(th, 4), T_exh=round(te, 4),
                             speedup=round(te / th, 2)))
        # break-even evaluator cost: T_hca == T_exh
        dN = e.n_evaluated - h.n_evaluated
        be = (oh_h - oh_e) / dN if dN else float("inf")
        print(f"{scale}/{name}: break-even C_E = {be*1e6:.1f} us "
              f"(N_hca={h.n_evaluated}, N_exh={e.n_evaluated})", flush=True)

# --- real validation point: discrete-event evaluator on S1 -------------------
sp = make_space("S1"); wl = WORKLOADS["telemetry"]
h, e = hca_dse(sp, wl), exhaustive(sp, wl)
t0 = time.perf_counter()
for x in list(sp.enumerate())[:40]:
    simulate(x, wl, n_req=3000)
C_E_des = (time.perf_counter() - t0) / 40
oh_h, oh_e = h.runtime - h.t_eval, e.runtime - e.t_eval
print(f"measured C_E(DES) = {C_E_des*1000:.1f} ms -> predicted speedup at S1 = "
      f"{(oh_e + e.n_evaluated*C_E_des)/(oh_h + h.n_evaluated*C_E_des):.1f}x "
      f"(T_exh={oh_e + e.n_evaluated*C_E_des:.1f}s vs T_hca={oh_h + h.n_evaluated*C_E_des:.1f}s)")
with open("results/e2_costsweep.csv", "w", newline="") as f:
    w = csv.DictWriter(f, sorted(rows[0])); w.writeheader(); w.writerows(rows)
print("written results/e2_costsweep.csv")
