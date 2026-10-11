# NestProof judge demonstration and pitch

## Thirty second opening

“A family can upload two perfectly readable documents and still get the wrong wealth total. They may describe the same deposit, but one hides the reference. NestProof makes the decision between extraction and the ledger inspectable: show the evidence, ask the missing question, preview the change and keep it reversible. Today you can challenge the decision yourself—even change the principal by one paisa—and see why the system changes its answer while the actual ledger stays untouched.”

## Three minute pitch with live actions

**0:00–0:30 — Establish the consequence.** Deliver the opening. Show the synthetic shared principal and explain that it is recorded deposit principal, not net worth. Two similar amounts alone do not prove identity.

**0:30–1:05 — Resolve missing evidence.** Open Masked deposit summary. Point to the missing reference and source lines. Enter FD-1007 and “Checked the synthetic original certificate.” Show the supported duplicate. Explain that this answer remains a user assertion, not institution verification.

**1:05–1:45 — Invite the challenge.** Expand Challenge this decision. Select Principal and enter 400000.01. The result becomes a same-date conflict. Show the distinct paise and unchanged ledger revision. Select Deposit reference and Remove this field instead. It becomes a review. These are real calls to the production relation function, with no persisted hypothetical correction.

**1:45–2:15 — Show the controlled write.** Preview the actual unmodified duplicate. Point to zero principal change. Check the confirmation box, commit, open history and download the receipt. Undo. Explain revision-bound, single-use previews and current source access.

**2:15–2:45 — Justify AI and evidence.** AI interprets variable labels; rules decide identity and changes. Show Evidence lab. State 74 passing tests and the small authored challenge's 30/30 ML versus 11/30 exact and 12/30 fuzzy results. Immediately explain shared authorship and narrow formats. These numbers do not establish real-bank accuracy.

**2:45–3:00 — Close on integration.** “We propose this review boundary before WealthNest updates canonical holdings. The next milestone is an independently labeled document pilot and measured reviewer effort. Our contribution is a decision the reviewer can inspect, challenge and reverse.”

## Five minute technical walkthrough

1. **Minute 1:** upload `samples/new.pdf` through the interface; inspect source lines and principal/maturity roles. Explain pypdf, local label classifier and deterministic normalization.
2. **Minute 2:** review the masked statement; distinguish extracted facts from user assertions. Explain matching against accepted accessible observations, not the upload queue.
3. **Minute 3:** challenge a resolved pair with one paisa, then missing identity. Explain the read-only endpoint and absence of a preview token. An identity change here is only a pairwise comparison, not a complete ledger search.
4. **Minute 4:** preview, confirm, inspect receipt and undo; explain actor/version/revision binding and SQLite transactions. Mention same-date maturity disagreements require a choice even with unchanged principal.
5. **Minute 5:** show test and evaluation files, one preserved failed experiment and the architecture. Let the judge alter a synthetic source. Accept unresolved output honestly.

## Difficult questions and defensible answers

| Judge question | Evidence-backed answer |
|---|---|
| Why is this innovative? | The focus is targeted clarification, source provenance, reversible decisions and a live sensitivity check in one household-import flow. Reconciliation itself is established prior art. |
| Why use AI? | Variable labels defeat exact dictionaries within the authored set. The local classifier assists interpretation; deterministic code governs values and writes. The baseline comparison is narrow, not universal. |
| Could this be built in a day? | A mockup could. The contribution is the exercised state transitions, access checks, negative cases, evidence attribution and reproducible limitations. Time spent is not a moat. |
| What if the AI is wrong? | Missing/conflicting evidence can block a preview; sources stay inspectable, acceptance requires review and the latest unchanged decision can be undone. Plausible extraction errors can still escape these checks. |
| Is the challenge another AI feature? | No. It transparently reruns the actual deterministic relation logic on hypothetical interpreted facts. It tests sensitivity, not extraction accuracy. |
| Is a user answer verified truth? | No. It is visibly attributed; independently checking that assertion is outside this prototype. |
| How much time or money does it save? | No measured user savings. A synthetic question-policy experiment assumes truthful answers; it is not a usability study. Zero duplicate principal change is not recovered money. |
| Can it handle 10,000 users? | Not demonstrated. Production requires real tenant identity, a managed transactional database, isolated parsing workers, queues, resource limits, encrypted storage and load testing. |
| Why should WealthNest use it? | It offers an inspectable review boundary before holdings updates. Actual product fit must be confirmed with their team and users. |
| Does it run offline? | After dependencies are installed, local parsing, inference, demo data and SQLite do not require an external model API. Initial dependency installation requires package access. |
| Is it WealthGPT? | No. Accepted observations and provenance could later feed it; no chat or retrieval integration is implemented. |
| What is still missing? | Independent validation, real authentication, OCR, broader layouts, authenticity checks, deployment/load evidence and user impact measurement. |

## Local deployment and recovery checklist

- Use Python 3.12, install `requirements.lock.txt`, and run the README checks before presenting. No paid API credentials are needed.
- Use a new unused `NESTPROOF_DB` path, for example `.runtime/judge-session-01.db`. Start uvicorn bound to `127.0.0.1`; use an available port and open that exact address. Do not expose demo persona switching to the internet.
- Preserve existing databases. For a backup, stop the server and copy the database to a new filename; do not replace live user data. Startup only seeds an otherwise-empty workspace.
- Confirm `/api/health`, seven visible starting sources for Ananya and shared principal INR 4,00,000. Confirm local samples are available. Keep synthetic PDF and TXT examples as labeled fallback inputs.
- If the server stops, restart with the same path to retain state. For a fresh demonstration, use another unused path. Never present a reset as undo.
- If a review becomes stale, reopen its document and create a fresh preview. Do not retry commit blindly; inspect history first.
- If the browser session expires, reload and choose the synthetic persona again. No external service fallback is needed for local inference.
- If an unfamiliar source cannot parse, show the explicit failure and continue with a labeled sample. Do not substitute a recording and call it live.
- After the demo, retain only synthetic data. Public deployment is deferred until production access controls, storage protections and operational tests exist.
