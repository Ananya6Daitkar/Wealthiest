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

**55 automated tests and 3 grouped browser checks pass.** Current development results are 64/64 field labels and 48/48 document pairs. A fresh developer-authored synthetic challenge produced 30/30 ML relations, versus 11/30 exact/rules and 12/30 calibrated fuzzy/rules. These small synthetic sets are not independently validated real-bank accuracy.

```sh
python -m evaluation.challenge
python -m evaluation.clarification
```

Start with the concise [Track C submission](docs/TRACK_C_SUBMISSION.md), which answers all eight required questions. See [final verification and limitations](docs/FINAL_VERIFICATION.md), [browser test](browser/regression.mjs), and the preserved original and failed intermediate experiments in `evaluation/`.

New: downloadable JSON decision receipts in Ledger & history, including source evidence, provenance, before/after principal and revision. Receipt access follows current source permissions.

**NestProof is document intelligence and review—not a WealthGPT chatbot.**

## Scope

Digital PDFs and UTF-8 text, English labeled fields, INR principal, one deposit per document. No OCR, live bank connection, document authenticity verification, investment recommendations, production identity system or hosted deployment. The original research's 99-point ambition is not an achieved score or a promise of winning.

Implementation handoff: 10 October 2026.
