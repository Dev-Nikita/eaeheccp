"""Level-B high-fidelity evaluator: discrete-event simulation of one design.

Adds fidelity the closed-form model does not have: multi-server (n-node) queues
with finite servers instead of an aggregate-capacity M/M/1 term, explicit link
contention (a link is a server, not a fixed delay), and stochastic service
times. Used (i) as the *expensive* evaluator in the cost-crossover study and
(ii) as an internal reference for the accuracy of the analytical model.
"""
from __future__ import annotations
import heapq, math, random
from typing import Dict, List, Tuple
from .model import POLICIES, WAN_B, WAN_PROP
from .evaluate import MB_TO_MB


class MultiServer:
    """FCFS queue with `n` identical servers."""
    __slots__ = ("n", "free", "q", "busy_until")

    def __init__(self, n: int):
        self.n = n
        self.free = n
        self.q: List[tuple] = []

    def submit(self, t, svc, req, out):
        if self.free > 0:
            self.free -= 1
            heapq.heappush(out, (t + svc, req, self))
        else:
            self.q.append((svc, req))

    def release(self, t, out):
        if self.q:
            svc, req = self.q.pop(0)
            heapq.heappush(out, (t + svc, req, self))
        else:
            self.free += 1


def simulate(x: dict, wl, n_req: int = 4000, warmup: int = 400,
             seed: int = 0) -> Dict[str, float]:
    rng = random.Random(seed)
    t1, t3 = POLICIES[x["policy"]]
    tiers = (t1, "gw", t3)
    C = {"edge": x["edge_cls"].C, "gw": x["gw_cls"].C, "cloud": x["cloud_cls"].C}
    servers = {"edge": MultiServer(x["n_e"]), "gw": MultiServer(x["n_g"]),
               "cloud": MultiServer(4)}
    lk = x["link_cls"]
    links = {"access": MultiServer(x["n_e"] if t1 == "edge" else x["n_g"]),
             "wan": MultiServer(2)}

    s = [st.s_in for st in wl.stages]
    # request route: (kind, resource, work) with kind in {link, compute}
    route: List[tuple] = [("link", "access", s[0])]
    route.append(("compute", tiers[0], wl.stages[0].w * x["rep"]))
    if t1 == "edge":
        route.append(("link", "access", s[1]))
        if x["rep"] > 1:
            route.append(("link", "access", (x["rep"] - 1) * wl.s_sync))
    route.append(("compute", "gw", wl.stages[1].w))
    route.append(("link", "wan" if t3 == "cloud" else "access", s[2]))
    route.append(("compute", tiers[2], wl.stages[2].w))

    lam = wl.Lambda
    ev: List[tuple] = []          # (time, req_id, resource-or-None)
    arrivals = []
    t = 0.0
    for i in range(n_req):
        t += rng.expovariate(lam)
        arrivals.append(t)
    state = {i: 0 for i in range(n_req)}
    start = {}
    done: List[float] = []

    def svc_time(step) -> float:
        kind, res, work = step
        if kind == "compute":
            mean = work / C[res]
        else:
            B = lk.B if res == "access" else WAN_B
            mean = work * MB_TO_MB / B
        return rng.expovariate(1.0 / mean) if mean > 0 else 0.0

    def prop_delay(step) -> float:
        return lk.prop if step[1] == "access" else WAN_PROP

    def dispatch(now, i, out):
        k = state[i]
        if k == len(route):
            done.append((now - start[i], start[i]))
            return
        step = route[k]
        res = servers[step[1]] if step[0] == "compute" else links[step[1]]
        extra = 0.0 if step[0] == "compute" else prop_delay(step)
        res.submit(now + extra, svc_time(step), i, out)

    pending = list(enumerate(arrivals))
    idx = 0
    now = 0.0
    while idx < len(pending) or ev:
        if ev and (idx >= len(pending) or ev[0][0] <= pending[idx][1]):
            now, i, res = heapq.heappop(ev)
            res.release(now, ev)
            state[i] += 1
            dispatch(now, i, ev)
        else:
            i, now = pending[idx]; idx += 1
            start[i] = now
            dispatch(now, i, ev)
        if now > 4.0 * n_req / lam:     # unstable configuration guard
            return {"mean": math.inf, "p50": math.inf, "p95": math.inf,
                    "completed": len(done)}
    lat = [d for d, st_ in sorted(done, key=lambda z: z[1])][warmup:]
    if not lat:
        return {"mean": math.inf, "p50": math.inf, "p95": math.inf, "completed": 0}
    ls = sorted(lat)
    return {"mean": sum(ls) / len(ls),
            "p50": ls[len(ls) // 2],
            "p95": ls[int(0.95 * (len(ls) - 1))],
            "completed": len(ls)}
