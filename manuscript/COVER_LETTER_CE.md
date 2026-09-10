# Cover letter — Communications Engineering

Dear Editors,

We submit "Exact architecture exploration for heterogeneous edge–cloud cyber-physical
systems" for consideration as an Article in Communications Engineering.

**The engineering advance.** Deciding the architecture of a distributed cyber-physical
system — how many edge nodes and gateways, which hardware and link classes, where each
processing stage runs, how far the ingest stage is replicated — is a multi-objective
decision over millions of candidates in which a single candidate is evaluated by
simulation that can take up to a minute. Engineers therefore work under a budget of
expensive evaluations, and today they must choose between exhaustive search, which pays
for every candidate, and evolutionary search, which fits a budget but cannot say which
trade-offs it missed. Exact methods that discard provably useless regions before
evaluating them exist, but all of them assume objectives that accumulate monotonically
with each decision. End-to-end latency does not: it depends on the utilisation of a tier,
which several decisions fix jointly. We show that exactness is nevertheless attainable for
such objectives, and that this converts the problem from "too expensive to explore" to
"explorable in a few dozen evaluations".

**Why it matters beyond one optimisation benchmark.** The result is not a faster
optimiser; it is a change in what an engineering team can afford to ask. On design spaces
of up to 8.3e7 architectures the method calls the expensive evaluator 16–61 times and
still returns the complete set of optimal trade-offs wherever exhaustive enumeration can
confirm it. Because the exploration never materialises the space, the largest search takes
under four seconds and under 100 KiB of traced memory. The mechanism — relax each term of
an objective separately, and order the decisions so that the load-dependent term becomes
exactly computable early — is not tied to our template: it applies wherever a subset of
decisions determines a utilisation-dependent term, which covers service placement across a
computing continuum, robotic sensing and control pipelines, and industrial edge
deployments with mixed hardware tiers.

**Evidence.** We prove the pruning rules safe and verify them by machine: bound
admissibility is checked exhaustively, and for every discarded partial design all of its
completions are enumerated and tested against the claim that discarded it. We compare
against exhaustive enumeration, random search, budget-matched NSGA-II over 20 seeds, and
an independent exact SMT-based solver. We then deployed the architectures as containers
with per-node network shaping and measured 36 architectures over 108 runs with the
analytical model frozen beforehand: the predicted ordering matches the measured ordering
for 88.6–91.3% of clearly separated architecture pairs within a workload.

**What we do not claim.** We state where the method does not help — cheap evaluators,
objectives without derivable bounds, and near-saturation regimes where neither model nor
deployment is stable — and we distinguish the exactness of the exploration with respect to
its model from the fidelity of that model to hardware. Every figure and numeric table in
the paper is regenerated from the raw result files by a single script.

The manuscript is original, is not under consideration elsewhere, and the authors declare
no competing interests. We have no preferred or excluded reviewers to name.

Sincerely,
Nikita Tarasov and Vasyl Tomyuk
Lviv Polytechnic National University, Lviv, Ukraine
