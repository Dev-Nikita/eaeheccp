# HCA-DSE — numeric audit of the manuscript against the result files

Date: 2026-09-09. Method: every quantitative claim in `manuscript/sections/*.tex`
and in the abstract was recomputed independently from `results/*.csv`, without
reusing the code that produced those files. The audit is now a script,
`experiments/verify_manuscript_numbers.py`, which prints PASS/FAIL per claim and
exits non-zero on any mismatch. Run it before every rebuild of the manuscript.

## Result

30 of 33 claims matched on the first pass. Three did not, and all three were in
the text rather than in the data. They are fixed.

### 1. Scalability — full evaluations understated as a range (Section 6, RQ5)

*Was:* "the number of full evaluations is essentially flat at 30 to 61".
*Actual:* the minimum over the sweep is **18** (sensing at the 1,296-candidate
scale); 30 is the minimum only if the two smallest sensing points are dropped.
The abstract and conclusion already said "16 to 61" for the funnel experiment,
so the results section contradicted them.
*Now:* "essentially flat, between 18 and 61 across the whole sweep".

### 2. Scalability — visited-state range mixed workloads (Section 6, RQ5)

*Was:* "The number of visited partial states grows from 391 to 16,778, i.e. by a
factor of 43 ... The ratio of visited partial states to raw candidates falls from
0.30 to 1.7e-4."
*Actual:* 391 is sensing at the smallest scale, 16,778 is telemetry at the
largest; the true maximum over all workloads is **16,781** (control). The 0.30
endpoint is sensing's fraction, while the maximum fraction is **0.509**
(control). A referee comparing the sentence with Table 9 would find both
endpoints unreproducible.
*Now:* stated per workload — telemetry grows 659 -> 16,778 (factor 25), the
visited count never exceeds 16,781 over all workloads and scales, and the
fraction falls from 0.51 to 1.7e-4.

### 3. Sensing over-prediction miscounted (Section 6, RQ6)

*Was:* "the model over-predicts latency by roughly 30% on eight of twelve
architectures".
*Actual:* **nine** of the twelve sensing architectures have a measured-to-
predicted ratio between 0.68 and 0.73. The remaining three are exactly the
unstable near-saturation designs (ratios 2.5, 3.6 and 12.3), which makes the
story cleaner, not weaker.
*Now:* "roughly 30% -- a measured-to-predicted ratio of 0.68-0.73 -- on nine of
the twelve architectures, the remaining three being exactly the unstable designs
discussed next".

## What was checked and matched exactly

* Funnel: S3 41-54 evaluations, 99.90% reduction; S4 52-60, 99.98%; exactness
  flags and recall 1.0 on S1-S3.
* Break-even evaluator cost: 1.65-2.29 us on S2 (claimed 1-3 us); negative on S3,
  i.e. HCA-DSE has the lower overhead there (claimed "below 1 us").
* Projected speed-ups at the measured 19.4 ms evaluator cost: 77.5x-143.1x (S2)
  and 544.8x-706.2x (S3); evaluation-count ratios 81.0x-149.5x and 640.0x-842.9x.
* Measured speed-up with the analytical evaluator: 1.32x-3.26x on S2-S3. Note
  that on S1 it is 0.99x-1.31x; the text scopes the claim to S2-S3, which is
  correct but worth keeping explicit.
* Ablation on S3: feasibility-only 7,025-12,700 (2.7x-4.9x), dominance-only
  327-415, combined 41-54 (a further 6.1x-9.7x).
* Scalability: runtime max 2.31 s (< 2.4 s), peak traced memory 86.5 KiB
  (< 90 KiB).
* Baselines on S3 at B=1000: NSGA-II median recall 0.500-0.741, HV 0.944-0.983;
  18.5x-24.4x fewer evaluations for HCA-DSE.
* Statistics on S3 at B=500 and 1000: p = 0.054-0.338, Cliff's delta 0.080-0.300;
  at B=100 random search has the higher median HV in all three workloads.
* Model versus discrete-event simulator: MAPE 39.3 / 44.3 / 14.2 % and Spearman
  0.921 / 0.919 / 0.963 for telemetry / control / sensing.
* Docker testbed, 36 architectures: MAPE 28.7%, median absolute error 7.5 ms,
  pooled Spearman 0.970; pair agreement 98.2% among the 498 pairs separated by
  more than 25% and 96.8% among the 561 pairs separated by more than 10%;
  four non-reproducible architectures, all sensing.
* M/M/1 -> M/D/1: MAPE 28.9% -> 23.7%, rank correlation 0.918 -> 0.889.

## Note on STATUS.md

`STATUS.md` is stale relative to the manuscript in three places and should be
regenerated or deleted before the replication package is archived: it reports the
older simulator-validation figures (42.5 / 50.8 / 20.8 % MAPE) that the M/D/1
correction superseded, the older 557x projection instead of 706x, and a
"remaining before submission" list whose two items are done. The manuscript is
correct; STATUS.md is not.

## Build note

`manuscript/main.pdf` was rebuilt from the corrected sources. The rebuild was
done with TeX Live 2022 (Debian) rather than MacTeX, so the page count differs
by one to two pages from the local build; regenerate on the authoring machine
with `cd manuscript && latexmk -pdf main.tex` before submission. The build is
clean: no errors, no LaTeX warnings, no undefined references or citations.
