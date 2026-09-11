PYTHON ?= .venv/bin/python
RELEASE ?= v1.1-submission-results
TESTBED ?=

.PHONY: reproduce verify assets
reproduce:
	$(PYTHON) experiments/reproduce.py --release $(RELEASE) $(if $(TESTBED),--testbed $(TESTBED),)
verify:
	$(PYTHON) experiments/verify_run.py results/$(RELEASE)/data
	HCADSE_RESULTS=results/$(RELEASE)/data $(PYTHON) experiments/verify_manuscript_numbers.py
assets:
	HCADSE_RESULTS=results/$(RELEASE)/data $(PYTHON) experiments/make_paper_assets.py
	HCADSE_RESULTS=results/$(RELEASE)/data $(PYTHON) experiments/make_claims.py
