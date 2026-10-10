# NestProof

**Review financial evidence before changing the ledger.**

A working local WealthNest.AI Track C prototype for English digital fixed-deposit documents. Upload PDF/TXT evidence, inspect extracted fields, resolve a missing reference, preview the represented principal change, confirm it, and inspect or undo the decision.

## Run locally

Python 3.12 is the tested runtime. No model API key or paid service is needed.

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock.txt
python -m uvicorn nestproof.app:app --host 127.0.0.1 --port 8765
```

Open **http://127.0.0.1:8765**. A new, otherwise-empty database is initialized with the synthetic starting records; the persona selector is a demonstration mechanism, not production authentication. Keep the server bound to loopback and use synthetic documents.

![Actual NestProof evidence review and confirmation preview](docs/NESTPROOF_PREVIEW.jpg)

## What is included

- [What we built, demo walkthrough and measured limitations](WHAT_WE_BUILT.md)
- [Research and design](docs/RESEARCH_AND_DESIGN.md)
- [Research-stage case study](docs/CASE_STUDY.md)
- [Implementation decisions](docs/IMPLEMENTATION_STRATEGY.md)
- [Actual evaluation results, including every failed case](evaluation/results.json)
- [Synthetic PDF samples](samples/)

The current implementation uses FastAPI, SQLite, a local TF-IDF/logistic-regression field classifier, deterministic reconciliation rules, and a browser interface. Source values are extracted and validated rather than generated. Changes require an explicit preview and confirmation. State persists in `.runtime/nestproof.db` (excluded from Git).

## Verify

```sh
python -m pytest -q
python -m evaluation.run
```

49 automated tests pass. Browser verification also covered uploading a PDF and resolving a masked reference against two accepted deposits.

On the inspected developer-authored regression set, ML plus shared field-role exclusions correctly interprets 61/64 labels, with 97.8% accepted-field precision. Document-pair correctness remains 39/48. The fuzzy baseline now selects its threshold on calibration data with the same error cost as ML. These are development regression results, not independent validation or production accuracy. The prior results are preserved in [baseline-results.json](evaluation/baseline-results.json).

See [the upgrade report](docs/UPGRADE_REPORT.md) for fixes, verification, remaining failures and an honest evidence standard.

## Scope

Digital PDFs and UTF-8 text, English labeled fields, INR principal, one deposit per document. No OCR, live bank connection, document authenticity verification, investment recommendations, production identity system or hosted deployment. The original research's 99-point ambition is not an achieved score or a promise of winning.

Implementation handoff: 10 October 2026.
