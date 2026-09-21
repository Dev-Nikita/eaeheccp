Dear Editors,

We submit "Exact architecture exploration for heterogeneous edge and cloud cyber-physical
systems" for consideration as an Article in Communications Engineering.

Industrial studies of distributed cyber-physical architectures evaluate one candidate by
simulation or deployment, at seconds to minutes per candidate, while realistic
architecture spaces contain millions of candidates. The budget that binds in practice is
therefore the number of high-fidelity evaluations a team can afford. Evolutionary search
fits that budget but cannot certify which trade-offs it missed. Exact partial-design
pruning could, but it relies on objectives that grow monotonically as decisions are
fixed, and end-to-end latency in a shared edge and cloud infrastructure does not: it
depends on tier utilisation, which several architectural decisions determine jointly.

The manuscript makes exact screening possible for this non-monotone case. Bounds obtained
by relaxing each term of an objective separately, combined with a decision order that
makes the queueing term exactly computable on an incomplete design, allow provably safe
elimination of infeasible and dominated architectures before any expensive evaluation. On
spaces of up to 83 million candidates the method calls the expensive evaluator 16–61
times and reproduces the exhaustive Pareto front wherever exhaustive verification is
tractable.

The evidence is layered: formal proofs with exhaustive machine checks of bound
admissibility; regression against exhaustive enumeration; budget-matched comparison with
random search and NSGA-II over 20 seeds; two exact solver baselines, one of which avoids
evaluator calls altogether; and a containerised deployment of 36 architectures over 108
runs with the model frozen beforehand. In that deployment the predicted order of two
architectures matched the measured order for 88.6–91.3% of pairs separated by more than
25%, and for 53 of 54 pairs separated by more than 50%.

We believe the work fits Communications Engineering because it adds an engineering
capability rather than a faster heuristic: elimination before expensive evaluation that
is certified with respect to the design model, so that a simulator or a test bench is
spent only where an optimal architecture can still be, together with a measured account
of how often those model-based decisions hold on hardware. We keep the claims to what was measured. The front is exact
with respect to the analytical model; the deployment validates latency ordering, not
energy or cost; and the study covers one architecture template, with the conditions
under which the bounds apply to others stated in the Discussion. The regimes in which
the method brings little benefit are reported as well.

All code, raw results and the 108 deployment runs are openly available (Zenodo DOI
10.5281/zenodo.22729667; GitHub Dev-Nikita/eaeheccp), and every number in the paper is
regenerated from them by one script.

The manuscript is original and is not under consideration elsewhere. The authors declare
no competing interests. This work has not been discussed with a Communications
Engineering editor prior to submission.

Sincerely,

Nikita Tarasov, corresponding author, on behalf of both authors (Nikita Tarasov, Roman Zinko)
Lviv Polytechnic National University, Lviv, Ukraine
dev.nikita@outlook.com
