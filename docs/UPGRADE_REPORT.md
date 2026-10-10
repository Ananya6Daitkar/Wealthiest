# NestProof — verified fixes and evidence gaps

10 October 2026. Built on GitHub commit c79d09b. No earned 99+ score is claimed.

## Changes

1. **Uploads complete in the browser.** The submit handler captures its form before awaiting the upload. It no longer accesses the expired event `currentTarget` after the asynchronous request. The dialog resets, the queue refreshes, and the uploaded document opens automatically.
2. **Ambiguous deposits can be distinguished.** If multiple accepted ledger positions match, the server selects the missing identity field with the greatest number of distinct candidate values (ties prefer account, then owner, then institution). This is a deterministic discrimination heuristic, not learned information gain. The user supplies that field and a source note. The server rechecks access, revision, field eligibility and normalized value. A unique match becomes an ordinary evidence review with the answer recorded as user-supplied and counted toward the two-answer limit.
3. **Unhelpful or unsafe answers do not change the ledger.** Masked references, attempts to override established fields, stale revisions and answers that fail to identify one accepted position are rejected. If one answer cannot distinguish candidates, clearer evidence is still needed; arbitrary candidate selection is not accepted.
4. **Known field-role errors are excluded.** Shared conservative FD-only rules reject labels referring to loans, credit, tax, interest, nominees, aggregates or totals before field classification. The rules apply to all evaluated methods. They fix observed confusions but can reject legitimate formulations containing these words and do not establish broad semantic safety.
5. **The fuzzy baseline is calibrated.** Both fuzzy and ML thresholds use calibration examples and the same 12:1 penalty for a wrong accepted field versus abstention. The selected fuzzy threshold is 0.775. This is a fairer comparison than the former fixed 0.82 threshold.
6. **Demo loading is non-destructive.** Explicit seeding now uses the same empty-workspace check as automatic initialization.
7. **Evaluation is labeled honestly.** Previously inspected examples are now a development regression set. Original results are retained. The UI no longer presents the updated results as untouched held-out validation. Running evaluation no longer regenerates the supplied PDF samples.

## Verification

- `python -m pytest -q`: **49 passed**, one dependency deprecation warning.
- `node --check static/app.js`: passed.
- `python -m evaluation.run`: executed; full failure lists remain in `evaluation/results.json`.
- Actual browser: uploaded `samples/new.pdf` through the file chooser; dialog closed and the uploaded source opened in the first-observation review.
- Actual browser: previewed and confirmed the shared second synthetic deposit; represented principal became ₹5,80,000.
- Actual browser: opened the masked statement with both FD-1007 and FD-2048 accepted; saw the new question; supplied FD-1007 and a provenance note; reached the already-represented proposal with the answer attributed.

API tests also exercise wrong/masked references, stale answers, attempts to override a non-requested field, unchanged ledger state on rejection, and zero-delta commit after successful disambiguation. Browser verification is a manual scripted check, not yet an automated browser CI suite.

## Measured results

| Measure | Original | Current development regression |
|---|---:|---:|
| ML correct labels | 55/64 | 61/64 |
| ML accepted-field precision | 86.5% | 97.8% (45/46) |
| ML field coverage | 95.8% | 95.8% |
| ML correct PDF-pair relations | 39/48 | 39/48 |
| Fuzzy correct labels | 20/64 | 32/64 |
| Fuzzy accepted-field precision | 80.0% | 94.1% (16/17) |
| Fuzzy correct PDF-pair relations | 30/48 | 30/48 |

Coverage includes wrong field assignments on relevant labels and must be read with precision. The ML weights and training examples are unchanged; improvements come from explicit domain exclusions, not a secretly improved model. The current results measure fixes on examples already inspected. They cannot be marketed as independent accuracy or financial correctness. The remaining difficult principal wording still limits pair resolution.

## Repeatable demo

Start a fresh synthetic workspace using a new database path rather than deleting existing work:

```sh
NESTPROOF_DB=.runtime/demo-new-session.db python -m uvicorn nestproof.app:app --host 127.0.0.1 --port 8766
```

Use a new filename for another fresh session. Accept the shared New deposit statement first, then open Masked deposit summary. Supply FD-1007 and an explicit synthetic-source note. Preview should preserve ₹5,80,000 rather than add the original deposit again. Inspect the source lines before confirming. Use Ledger & history to inspect and reverse the latest unchanged decision.

## What is needed to justify exceptional quality

The app is stronger, but no official judging result exists. The remaining gates are independently checked document diversity, stronger contextual extraction, calibrated safety/coverage tradeoffs, a repeatable browser regression suite, and observed user benefit. The prototype still lacks production authentication, OCR, real financial integration and document authenticity verification.

### Proposed usability study — not yet performed

With consent, recruit participants to review a balanced set of synthetic imports manually and with NestProof. Counterbalance order and use different equivalent tasks to reduce learning effects. Measure correct final ledger decisions, time to a correct decision, questions asked, unresolved cases and confidence. Have someone independent adjudicate outcomes. Report individual results, sample size and limitations; never count agent simulations as human user evidence.

Do not increase a judge score merely because a bug was fixed. The current deliverable is verified improvement with explicit limits, not a guarantee of winning.
