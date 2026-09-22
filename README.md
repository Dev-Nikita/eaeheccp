
| `hcadse/` | the method (model, bounds, search, baselines, discrete-event evaluator) |
| `experiments/` | e1–e13 experiments and the scripts that generate figures, tables, prose numbers and the submission folders |
| `results/` | raw result files; `results/v1.1-submission-results/` is an older sealed release |
| `testbed/` | containerised deployment (Go services, Docker Compose, tc netem) |
| `tests/` | correctness and regression tests |
| `notes/` | working notes, literature and bibliography audits, theory drafts |

## Rebuild after a change

```bash
python3 experiments/make_paper_assets.py          # figures and tables from results/
python3 experiments/make_claims.py                # numbers used in the prose
python3 experiments/check_claims.py               # every number in the prose is backed by a result
python3 experiments/make_submission_package.py    # refresh SUBMISSION/*/1_Manuscript and 2_Supplementary*
cd SUBMISSION/Communications_Engineering/1_Manuscript && pdflatex main && bibtex main && pdflatex main && pdflatex main
```

Full reproduction from a clean state: see `RUN.md` and `experiments/reproduce.py`.
