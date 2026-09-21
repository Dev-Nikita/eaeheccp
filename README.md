# HCA-DSE — exact architecture exploration for edge and cloud cyber-physical systems

Authors: Nikita Tarasov, Roman Zinko (Lviv Polytechnic National University)

## What to send where

```
SUBMISSION/
  Communications_Engineering/        <- ACTIVE submission (Springer Nature template)
    1_Manuscript/                    main.pdf, main.tex, main.bbl, refs.bib, sn-jnl.cls, sn-nature.bst, figures/
    2_Supplementary_Information/     Supplementary_Information.pdf, supplement.tex, sn-jnl.cls
    3_Cover_letter/                  Cover_letter.docx, Cover_letter.md
    README.txt                       upload list
    SUBMISSION_CHECKLIST.md          status and remaining steps
  JSA/                               <- fallback version, Journal of Systems Architecture (elsarticle)
    1_Manuscript/                    main.pdf, main.tex, main.bbl, refs.bib, figures/
    2_Supplementary/                 supplement.pdf, supplement.tex
    3_Cover_letter/                  Cover_letter.md
    Highlights.txt
```

Everything in `1_Manuscript/` and `2_Supplementary*/` is generated. Do not edit it there.

## Where the sources are

| Folder | Content |
|---|---|
| `manuscript/` | LaTeX sources. Communications Engineering: `sn_main.tex`, `sections_sn/`, `supplement_sn.tex`. JSA: `main.tex`, `sections/`, `supplement.tex`. Shared and generated: `figures/`, `tables/`, `generated/`, `generated_numbers.tex`, `refs.bib`, `sn-jnl.cls`, `sn-nature.bst` |
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
