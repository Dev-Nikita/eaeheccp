# Cover letter — Journal of Systems Architecture

Dear Editors,

Please consider the enclosed manuscript, "Hierarchical Constraint-Aware Design-Space
Exploration for Heterogeneous Distributed Cyber-Physical Systems", for publication in the
Journal of Systems Architecture as a regular paper.

**Problem.** Architecting a distributed cyber-physical system requires joint decisions on
the number and class of edge and gateway nodes, on the placement of application stages, on
replication and on communication links, under conflicting latency, energy, cost and
network-volume objectives. The resulting design space grows combinatorially, and — as the
recent survey by Herget et al. (Euromicro DSD 2022) states — "efficient and scalable DSE
technology for dCPS is more or less non-existing". What makes the distributed setting
different from classical MPSoC exploration is not only the size of the space but the cost
of one design-point evaluation, reported as up to a minute per point in the industrial
CompDSE methodology (IET CPS, 2025).

**Contribution.** We present HCA-DSE, which removes structurally ill-formed, provably
infeasible and provably dominated regions of the architecture space before any full
evaluation. The technical core is a family of admissible bounds for *contention-dependent*
objectives. Existing exact exploration methods — symbolic exploration under
assignment-monotone objectives, and integer-programming formulations of task allocation —
assume that every decision only adds to the objective. End-to-end latency in a distributed
CPS violates that assumption: it depends on tier utilisation, which is determined jointly
by node counts, node classes, replication and placement. We combine a term-wise relaxation
with a decision ordering that makes the queueing term exactly computable on a partial
design, prove that the exact Pareto front is preserved, and verify both the bound
admissibility and the front equality exhaustively by machine.

**Why JSA.** The paper is a design-automation contribution for distributed and embedded
software architectures: it concerns architecture exploration, real-time constraints,
resource allocation across an edge-cloud continuum, and the interaction between analytical
models and measured deployments — all central to the scope of the journal, and adjacent to
work the journal has published on design-time optimisation of distributed edge
applications.

**Results.** On four design-space scales, three workload classes and spaces of up to
8.3e7 candidate architectures, HCA-DSE performs 26 to 61 full evaluations while
reproducing the exhaustive Pareto front exactly wherever exhaustive enumeration is
tractable (recall and precision of 1.0). Budget-matched NSGA-II requires 1000 evaluations
for a median Pareto recall of 0.50-0.91. A containerised edge-gateway-cloud testbed with
per-node link shaping (36 architectures, 108 measured runs) shows that the analytical
model orders architectures consistently with measurements in 98% of the pairs it separates
by more than 25%.

**Reproducibility and honesty of reporting.** Every figure and every numeric table in the
paper is generated from the raw result files by a single script; no number is transcribed
by hand. We report where the method does *not* help (cheap evaluators, where the wall-clock
gain is only 1.3-3.3x), where the model is weakest (data-intensive workloads, 50% MAPE),
and which measurements were not reproducible (four near-saturation configurations). We
also state explicitly that the exactness guarantee applies to the analytical model, not to
the deployed system.

The manuscript is original, is not under consideration elsewhere, and has not been
published previously. The author declares no competing interests.

Sincerely,
Nikita Tarasov
Lviv Polytechnic National University, Lviv, Ukraine
7nikitan@gmail.com
