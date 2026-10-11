# What we actually built — NestProof

**Updated: 10 October 2026.** Start with [the concise Track C submission](docs/TRACK_C_SUBMISSION.md) and [final verification](docs/FINAL_VERIFICATION.md). Current build: 74 automated tests and 3 grouped browser checks pass; 64/64 development labels, 48/48 development pairs and 30/30 fresh synthetic challenge pairs. These are developer-authored tests, not independent bank-document accuracy. Earlier measurements below are historical.

This is **Document Intelligence + Evaluation & Reliability**, not a WealthGPT chatbot. The frontend now includes targeted disambiguation, preview/confirmation, history/undo, downloadable JSON decision receipts and an Evidence lab with policy and challenge results. No guaranteed win or 99+ score is claimed.

## The product

NestProof is a local evidence-review workspace for fixed-deposit imports. Its central demonstration is simple: a statement with a masked deposit reference cannot establish a duplicate. The system asks for that reference, records the user's answer and provenance, checks the constraints again, and previews the ledger effect before accepting a decision.

A statement that describes an already recorded deposit should not add its principal twice. A different deposit should add a separate position. An earlier statement should remain in history without replacing a newer observation. Two principal amounts for the same identity and date require an explicit user choice.

Incoming documents are matched against accessible accepted ledger observations, not against the upload queue. A unique match opens a ledger-backed review; a complete identity with no match enters the first-observation flow; incomplete identities with no unique match remain unresolved.

## Preview

Run the README commands and open **http://127.0.0.1:8765**. GitHub stores the source; it does not host this Python application. The local preview works while the server is running.

The interface contains:

- **Import review:** document queue, side-by-side field comparison, source text with page/line references, targeted clarification and a confirmation preview.
- **Ledger & history:** accepted positions, effective-date and revision queries, decision history and undo of the latest unchanged decision.
- **FD Maturity Tracker:** accepted deposit due dates, days remaining and holder/status filters; deterministic, not predictive AI.
- **Evidence lab:** results loaded from the actual evaluation JSON, baseline comparisons and limitations.
- **How it works:** processing stages and supported scope.

The visual design uses a cream background, dark green navigation, document cards, amber unresolved states and explicit before/after amounts. It is a working interface backed by persistent API state, not a screenshot or static mockup.

![Actual NestProof evidence review and confirmation preview](docs/NESTPROOF_PREVIEW.jpg)

## Five-minute live demonstration

1. Start with a new, otherwise-empty local database. It is initialized with the synthetic workspace, including a shared deposit principal of ₹4,00,000. All sample PDFs pass through the parser; outcomes are not assigned to fixture names.
2. Choose **Masked deposit summary**. The incoming reference is unresolved. Enter `FD-1007` and a provenance note such as `Verified against the synthetic original certificate`.
3. Apply the evidence. The result should identify the already represented deposit. Preview shows ₹4,00,000 → ₹4,00,000. Check the confirmation box and record the decision. This is avoided double counting, not recovered money.
4. Open **Ledger & history**. Inspect the new revision and undo it. The original revision remains available.
5. Review **New deposit statement**. Its distinct reference supports a separate deposit; the preview shows ₹4,00,000 → ₹5,80,000 if the starting ledger has no other committed additions.
6. Review **Conflicting principal statement**. The app requires a deliberate choice between the existing and incoming same-date observations. It will not silently resolve the conflict.
7. Review **Instruction attack sample**. Instruction-like content is quarantined; no change can be committed. This is a narrow pattern detector, not a comprehensive prompt-injection defense. There is no LLM agent executing document instructions.
8. Switch the synthetic persona to Ravi. His private document becomes visible. The server checks access on document reads, source downloads, comparisons, commits and historical ledger views.
9. Open **Evidence lab** and explain both improvements and failures. Invite the reviewer to upload a synthetic digital document of their own.

## Implemented engineering

| Capability | What actually runs |
|---|---|
| Document ingestion | PDF text extraction with pypdf; UTF-8 text; 3 MB and 10-page limits; unreadable/scanned files rejected |
| AI interpretation | Local word/character TF-IDF features and logistic regression trained on 85 authored labels; abstention threshold selected on 32 calibration labels |
| Evidence | Original bytes, hash, extracted lines, field source references and explicitly attributed user answers |
| Financial constraints | Ledger-backed matching on normalized holder/account/institution identity, dated observations, distinct principal/maturity fields and Decimal arithmetic |
| Clarification | Candidate-aware field selection, one missing field at a time, at most two accepted answers per supported review; unresolved candidates require clearer evidence |
| Changes | Revision-bound preview, actor-bound single-use commit, SQLite transaction, stale-preview rejection |
| Reversal | Latest unchanged decision can be reversed into a new revision; prior history remains |
| First upload | A complete unflagged document can establish a first observation through preview and confirmation |
| Privacy exercise | Synthetic sessions, private/family scopes, server-side resource checks, CSRF tokens and source revocation API |
| Persistence | Local SQLite database; no external bank or model connection |

Source revocation is available through the API, not a dedicated interface button. Historical views apply current source access. Revocation can conservatively hide observations or block later changes; it is not a production consent-management system. The synthetic persona switch is intentionally accessible and must never be treated as real authentication.

## Current measured evidence

| Evidence | Recorded result | What it establishes |
|---|---|---|
| Automated tests | 74 passed | Supported engine, API, permission and maturity-tracker paths |
| Browser regression | 3 grouped checks passed | Upload, confirmation, commit, history, receipt link and undo |
| Development labels | 64/64 | Regression behavior after iterative fixes |
| Development PDF pairs | ML/rules 48/48; exact/rules and fuzzy/rules 33/48 | Comparison under shared role constraints |
| Fresh synthetic challenge | ML/rules 30/30; exact/rules 11/30; fuzzy/rules 12/30 | Narrow developer-authored challenge, not external validation |
| Clarification simulation | 1.0 questions versus 2.0 fixed order and 3.0 all fields | Constructed cases with truthful answers, not measured human savings |

These sets share an author and narrow document schemas. No real-bank accuracy, user time savings or production safety claim follows from the results. The local model weights were not retrained: recent gains come from deterministic role constraints combined with ML.

See [final verification](docs/FINAL_VERIFICATION.md) for reproduction and limitations. The [original baseline](evaluation/baseline-results.json), [role-guard iteration](evaluation/role-guard-results.json) and [failed capital-only iteration](evaluation/capital-only-experiment.json) preserve the experiment history. The [current result file](evaluation/results.json) is the development regression, not the original failure report.

## What international research became in this build

- **FINBOURNE-inspired temporal separation:** effective dates plus recorded ledger revisions. This is a small SQLite implementation, not a FINBOURNE integration or equivalent platform.
- **Canoe-inspired verification workflow:** source inspection and exception review. No claim of matching Canoe's extraction capabilities.
- **SGFinDex-inspired permission awareness:** private/family resource checks and current-access enforcement. No SGFinDex or Account Aggregator integration.
- **Addepar prior art:** evidence-driven reconciliation is not claimed as globally novel. Differentiation is the bounded clarification and reversible household-import workflow within this narrow prototype.

Source links and original research are in `docs/RESEARCH_AND_DESIGN.md`.

## Honest readiness assessment

This is a working local hackathon prototype, not a production wealth platform. Its strongest evidence is the complete review/commit/undo flow and reproducible error report. Its weakest areas are the small authored dataset, modest label model, synthetic authentication and absence of real-user validation.

No official judging score exists. The submission is best assessed through the runnable workflow, comparison results and explicit limits rather than a speculative numerical rating.

The next evidence needed for a stronger submission is independently labeled bank-document diversity, independent comparison against stronger extraction systems, measured user effort, and feedback from WealthNest on integration. Adding claims or more decorative features would not replace that evidence.
