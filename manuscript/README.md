# LaTeX sources

Two versions share one set of generated figures, tables and numbers.

| Version | Main file | Sections | Supplement |
|---|---|---|---|
| Communications Engineering (active) | `sn_main.tex` | `sections_sn/` | `supplement_sn.tex` |
| JSA (fallback) | `main.tex` | `sections/` | `supplement.tex` |

Generated, do not edit by hand: `figures/`, `tables/`, `generated/`, `generated_numbers.tex`.
Cross-reference macros used by the generated prose: `generated/refdefs.tex` (JSA defaults)
and `generated/refdefs_sn.tex` (Communications Engineering).

The submission-ready copies are written to `../SUBMISSION/` by
`python3 experiments/make_submission_package.py`.
