"""Search strategies: exhaustive ground truth, HCA-DSE, random baseline."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import random, time
from .model import DesignSpace, VAR_ORDER
from .evaluate import evaluate
from .bounds import lower_bounds, infeasible_by_bounds, dominated_by_bounds
from .bounder import Bounder


# ---------------------------------------------------------------------------
# structural validity (Stage 1)
# ---------------------------------------------------------------------------

def structurally_valid(partial: dict) -> bool:
    if "n_g" in partial and "n_e" in partial and partial["n_g"] > partial["n_e"]:
        return False
    if "rep" in partial and "n_e" in partial and partial["rep"] > partial["n_e"]:
        return False
    if "rep" in partial and "policy" in partial and partial["policy"] == "cloud-first" \
            and partial["rep"] > 1:
        return False  # no edge instances to replicate
    return True


def pareto_front(points: List[Tuple[dict, tuple]]) -> List[Tuple[dict, tuple]]:
    out = []
    for xa, fa in points:
        dom = False
        for xb, fb in points:
            if all(fb[i] <= fa[i] for i in range(len(fa))) and \
               any(fb[i] < fa[i] for i in range(len(fa))):
                dom = True
                break
        if not dom:
            out.append((xa, fa))
    return out


@dataclass
class SearchStats:
    method: str
    n_raw: int = 0
    n_structural: int = 0
    n_feasible_bound: int = 0
    n_evaluated: int = 0
    n_feasible: int = 0
    runtime: float = 0.0
    pruned_structural: int = 0
    pruned_bound: int = 0
    pruned_dominance: int = 0
    n_nodes: int = 0          # partial states visited (never materialises |X|)
    t_bounds: float = 0.0
    t_eval: float = 0.0
    t_dominance: float = 0.0
    t_pareto: float = 0.0
    front: List[Tuple[dict, tuple]] = field(default_factory=list)


def exhaustive(space: DesignSpace, wl) -> SearchStats:
    t0 = time.perf_counter()
    s = SearchStats("exhaustive", n_raw=space.size)
    pts = []
    for x in space.enumerate():
        if not structurally_valid(x):
            s.pruned_structural += 1
            continue
        s.n_structural += 1
        s.n_evaluated += 1
        te = time.perf_counter()
        r = evaluate(x, wl)
        s.t_eval += time.perf_counter() - te
        if r.feasible:
            s.n_feasible += 1
            pts.append((x, r.objectives))
    tp = time.perf_counter()
    s.front = pareto_front(pts)
    s.t_pareto = time.perf_counter() - tp
    s.runtime = time.perf_counter() - t0
    return s


def hca_dse(space: DesignSpace, wl, use_bounds=True, use_dominance=True,
            use_structural=True, record_pruned=None) -> SearchStats:
    """Hierarchical constraint-aware DFS over the prefix tree."""
    t0 = time.perf_counter()
    s = SearchStats("hca-dse", n_raw=space.size)
    archive: List[tuple] = []          # non-dominated evaluated objective vectors
    pts: List[Tuple[dict, tuple]] = []
    bd = Bounder(space, wl)

    def archive_add(f: tuple):
        for g in archive:
            if all(g[i] <= f[i] for i in range(4)) and any(g[i] < f[i] for i in range(4)):
                return
        archive[:] = [g for g in archive
                      if not (all(f[i] <= g[i] for i in range(4)) and
                              any(f[i] < g[i] for i in range(4)))]
        archive.append(f)

    def subtree_size(depth: int) -> int:
        n = 1
        for v in VAR_ORDER[depth:]:
            n *= len(space.domain(v))
        return n

    def rec(depth: int, partial: dict):
        s.n_nodes += 1
        if depth == len(VAR_ORDER):
            s.n_evaluated += 1
            te = time.perf_counter()
            r = evaluate(partial, wl)
            s.t_eval += time.perf_counter() - te
            if r.feasible:
                s.n_feasible += 1
                pts.append((dict(partial), r.objectives))
                archive_add(r.objectives)
            return
        var = VAR_ORDER[depth]
        for val in space.domain(var):
            nxt = dict(partial); nxt[var] = val
            if use_structural and not structurally_valid(nxt):
                s.pruned_structural += subtree_size(depth + 1)
                if record_pruned is not None:
                    record_pruned.append(("structural", dict(nxt)))
                continue
            if use_bounds or use_dominance:
                tb = time.perf_counter()
                lb = bd.bounds(nxt)
                s.t_bounds += time.perf_counter() - tb
                if use_bounds and infeasible_by_bounds(lb, wl):
                    s.pruned_bound += subtree_size(depth + 1)
                    if record_pruned is not None:
                        record_pruned.append(("feasibility", dict(nxt)))
                    continue
                td = time.perf_counter()
                dom = use_dominance and dominated_by_bounds(lb, archive)
                s.t_dominance += time.perf_counter() - td
                if dom:
                    s.pruned_dominance += subtree_size(depth + 1)
                    if record_pruned is not None:
                        record_pruned.append(("dominance", dict(nxt)))
                    continue
            rec(depth + 1, nxt)

    rec(0, {})
    tp = time.perf_counter()
    s.front = pareto_front(pts)
    s.t_pareto = time.perf_counter() - tp
    s.runtime = time.perf_counter() - t0
    return s


def random_search(space: DesignSpace, wl, budget: int, seed: int = 0) -> SearchStats:
    rng = random.Random(seed)
    t0 = time.perf_counter()
    s = SearchStats("random", n_raw=space.size)
    pts = []
    for _ in range(budget):
        x = {v: rng.choice(space.domain(v)) for v in VAR_ORDER}
        s.n_evaluated += 1
        if not structurally_valid(x):
            continue
        r = evaluate(x, wl)
        if r.feasible:
            s.n_feasible += 1
            pts.append((x, r.objectives))
    s.front = pareto_front(pts)
    s.runtime = time.perf_counter() - t0
    return s
