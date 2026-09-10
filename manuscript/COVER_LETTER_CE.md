Dear Editors,

We submit "Exact architecture exploration for heterogeneous edge–cloud cyber-physical
systems" for consideration as an Article in Communications Engineering.

Designing a distributed cyber-physical system requires joint decisions on edge and
gateway provisioning, hardware and link classes, stage placement and replication. A single
candidate is evaluated by simulation or by deployment, so the limiting resource is the
number of high-fidelity evaluations a team can afford rather than the nominal size of the
search space. Exhaustive enumeration returns the complete set of trade-offs at
prohibitive cost, and evolutionary search fits a budget but offers no certificate of what
it missed. The exact partial-design methods closest to our setting typically exploit
objectives that accumulate monotonically as decisions are fixed; contention-dependent
end-to-end latency does not, because tier utilisation is determined jointly by several
architectural choices.

We construct admissible bounds by relaxing the terms of an objective independently, and
order the decisions so that the utilisation-dependent term becomes exactly computable on
an incomplete design. Pruning built on these bounds is provably safe. On spaces of up to
8.3e7 candidate architectures the method requires 16–61 full evaluator calls and
reproduces the exhaustive Pareto front wherever exhaustive verification is still
tractable. Correctness rests on formal proofs, exhaustive machine checks of bound admissibility and
regression against exhaustive enumeration, and is complemented by budget-matched
comparison with random search and NSGA-II over 20 seeds and by an independent exact
baseline built on an SMT solver. A containerised deployment of 36 architectures over 108
runs, with the analytical model frozen beforehand, shows that predicted and measured
orderings agree for 88.6–91.3% of clearly separated architecture pairs within a
workload.

We believe the work suits Communications Engineering because it addresses a general
design bottleneck in heterogeneous distributed infrastructure — screening a very large
architectural space without spending a high-fidelity evaluation on every candidate — and
pairs a formally exact search mechanism with systems-level validation.
It is a design methodology rather than a domain-specific heuristic: the bound
construction applies wherever a subset of architectural decisions jointly determines a
utilisation-dependent objective, and the present study demonstrates it on one
heterogeneous edge–cloud template. We distinguish exactness with respect to the
analytical model from the fidelity of that model to a physical deployment, and the
manuscript reports the regimes in which the method brings little benefit.

The manuscript is original and is not under consideration elsewhere. The authors declare
no competing interests. This work has not been discussed with a Communications
Engineering editor prior to submission.

Sincerely,

Nikita Tarasov, corresponding author, on behalf of the authors
Lviv Polytechnic National University, Lviv, Ukraine
dev.nikita@outlook.com
