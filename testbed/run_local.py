"""Gate 10 (namespace variant): runs the emulated edge/gateway/cloud testbed
inside a private network namespace, without Docker.

    unshare -rn python3 testbed/run_local.py --repeats 3 [--limit N] [--workload W]

Each tier node is a separate OS process pinned to its own CPU (so a node is a
single server, as in the model); links are shaped with `tc netem` on lo using a
prio qdisc with two bands: access links (delay/rate of the link class of the
design) and the WAN hop to the cloud (20 ms / 200 Mbit/s). Shaping is applied in
the forward direction, matching the one-way transfers counted by the model.
"""
import argparse, csv, json, os, signal, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(ROOT, "testbed/bin")
NODE, LOADGEN = f"{BIN}/node-linux-arm64", f"{BIN}/loadgen-linux-arm64"
ACCESS_IP, WAN_IP = "127.0.0.2", "127.0.0.3"
NCPU = os.cpu_count() or 4


def sh(c, check=False):
    r = subprocess.run(c, shell=True, text=True, capture_output=True)
    if check and r.returncode:
        sys.exit(f"{c}\n{r.stderr}")
    return r


def net_setup():
    sh("ip link set lo up", check=True)
    for ip in (ACCESS_IP, WAN_IP):
        sh(f"ip addr add {ip}/8 dev lo")
    sh("tc qdisc del dev lo root 2>/dev/null")
    # 4 bands with a priomap that sends ALL unclassified traffic to band 1:4;
    # only explicitly filtered forward-direction packets reach the shaped bands
    # (a default priomap would silently push ACKs into the WAN band).
    sh("tc qdisc add dev lo root handle 1: prio bands 4 priomap " + " ".join(["3"] * 16),
       check=True)
    sh("tc qdisc add dev lo parent 1:1 handle 10: netem delay 1ms rate 100mbit", check=True)
    sh("tc qdisc add dev lo parent 1:2 handle 20: netem delay 20ms rate 200mbit", check=True)
    # Shape only the forward direction of each hop: packets addressed to a node
    # port. Responses (to ephemeral ports) stay unshaped, so each transfer is
    # delayed exactly once, matching the one-way transfers in the model.
    sh(f"tc filter add dev lo parent 1: protocol ip prio 1 u32 "
       f"match ip dport 9201 0xffff flowid 1:2", check=True)          # WAN hop to cloud
    for port in list(range(9001, 9009)) + list(range(9101, 9105)):
        sh(f"tc filter add dev lo parent 1: protocol ip prio 2 u32 "
           f"match ip dport {port} 0xffff flowid 1:1", check=True)     # access links


def set_access_link(delay_ms, rate_mbit):
    sh(f"tc qdisc change dev lo parent 1:1 handle 10: netem "
       f"delay {delay_ms:.3f}ms rate {rate_mbit:.0f}mbit", check=True)


def hosts_for(d):
    edges = [f"{ACCESS_IP}:{9001+i}" for i in range(d["n_e"])]
    gws = [f"{ACCESS_IP}:{9101+i}" for i in range(d["n_g"])]
    cloud = [f"{WAN_IP}:9201"]
    return {"edge": edges, "gw": gws, "cloud": cloud}


def run_design(d, rep, warmup_ratio=0.1):
    h = hosts_for(d)
    procs = []
    core = 0
    for tier, mips in (("edge", d["mips"]["edge"]), ("gw", d["mips"]["gw"]),
                       ("cloud", d["mips"]["cloud"])):
        for hp in h[tier]:
            port = hp.split(":")[1]
            ip = hp.split(":")[0]
            env = dict(os.environ, MIPS=str(int(mips)), ROLE=tier, PORT=port)
            procs.append(subprocess.Popen(
                ["taskset", "-c", str(core % NCPU), NODE],
                env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
            core += 1
    set_access_link(d["link"]["delay_ms"], d["link"]["rate_mbit"])
    t1, _, t3 = d["tiers"]
    st = d["stages"]
    spec = {"design": d["design"], "entry": h[t1], "rep": d["rep"],
            "steps": [{"hosts": h[t1], "work_mi": st[0]["w"], "pay_mb": st[0]["pay"]},
                      {"hosts": h["gw"], "work_mi": st[1]["w"], "pay_mb": st[1]["pay"]},
                      {"hosts": h[t3], "work_mi": st[2]["w"], "pay_mb": st[2]["pay"]}],
            "lambda": d["lambda_"], "n_req": d["n_req"], "warmup": d["warmup"],
            "first_pay_mb": d["first_pay_mb"], "sync_mb": d["sync_mb"]}
    os.makedirs("/tmp/hcadse_run", exist_ok=True)
    sp = "/tmp/hcadse_run/spec.json"; out = "/tmp/hcadse_run/result.json"
    json.dump(spec, open(sp, "w"))
    if os.path.exists(out):
        os.remove(out)
    t0 = time.time()
    r = subprocess.run([LOADGEN],
                       env=dict(os.environ, SPEC=sp, OUT=out),
                       capture_output=True, text=True, timeout=600)
    for p in procs:
        p.send_signal(signal.SIGKILL)
    for p in procs:
        p.wait()
    res = json.load(open(out)) if os.path.exists(out) else {}
    res["wall"] = round(time.time() - t0, 1)
    if not res.get("n"):
        res["stderr"] = r.stderr[-300:]
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--designs", default=os.path.join(ROOT, "testbed/specs/designs_local.json"))
    ap.add_argument("--out", default=os.path.join(ROOT, "results/e9_testbed_local.csv"))
    ap.add_argument("--workload")
    ap.add_argument("--limit", type=int, default=0, help="max runs in this invocation")
    a = ap.parse_args()
    net_setup()
    designs = json.load(open(a.designs))
    if a.workload:
        designs = [d for d in designs if d["workload"] == a.workload]
    rows = list(csv.DictReader(open(a.out))) if os.path.exists(a.out) else []
    done = {r["key"] for r in rows}
    n_run = 0
    for i, d in enumerate(designs):
        for rep in range(a.repeats):
            key = f"{d['workload']}|{d['design']['policy']}|{i}|{rep}"
            if key in done:
                continue
            if a.limit and n_run >= a.limit:
                print(f"limit reached; {len(rows)} rows in {a.out}"); return
            res = run_design(d, rep)
            row = dict(key=key, workload=d["workload"], kind=d["kind"], design_idx=i,
                       repeat=rep, n_e=d["n_e"], n_g=d["n_g"],
                       policy=d["design"]["policy"], rep_factor=d["rep"],
                       edge_cls=d["design"]["edge_cls"], link_cls=d["design"]["link_cls"],
                       L_analytical=d["L_analytical"], mean=res.get("mean"),
                       p50=res.get("p50"), p95=res.get("p95"), p99=res.get("p99"),
                       n=res.get("n"), errors=res.get("errors"), wall=res.get("wall"),
                       ok=bool(res.get("n")))
            rows.append(row); n_run += 1
            with open(a.out, "w", newline="") as f:
                w = csv.DictWriter(f, sorted(rows[0])); w.writeheader(); w.writerows(rows)
            print(f"[{len(rows)}] {d['workload']}/{d['kind']} n_e={d['n_e']} {d['design']['policy']} "
                  f"rep{rep}: model={d['L_analytical']*1e3:.1f}ms "
                  f"p50={(res.get('p50') or float('nan'))*1e3:.1f}ms "
                  f"p95={(res.get('p95') or float('nan'))*1e3:.1f}ms err={res.get('errors')} "
                  f"({res['wall']}s)", flush=True)
    print(f"finished: {len(rows)} rows -> {a.out}")


if __name__ == "__main__":
    main()
