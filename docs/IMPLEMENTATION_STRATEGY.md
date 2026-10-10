> Historical implementation plan. For delivered capabilities and measured results, use the [final submission](TRACK_C_SUBMISSION.md) and [verification record](FINAL_VERIFICATION.md). The ranking below records design estimates, not judging results.

# NestProof implementation decision

9 October 2026. This document supersedes proposed implementation choices in the research report where they differ. It does not replace the research or claim an achieved score.

## Selection

| Strategy | Originality /15 | Impact /15 | Fit /15 | AI /15 | Feasibility /10 | Evaluation /10 | Trust /10 | Demo /10 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Evidence-guided import resolution | 11 | 13 | 15 | 12 | 9 | 9 | 8 | 9 | 86 |
| WealthGPT answerability gate | 9 | 13 | 15 | 12 | 9 | 9 | 8 | 8 | 83 |
| Impact-ranked extraction review | 10 | 12 | 14 | 11 | 9 | 9 | 8 | 8 | 81 |
| Household transfer matching | 9 | 12 | 12 | 11 | 8 | 9 | 8 | 8 | 77 |
| Insurance-condition analysis | 11 | 13 | 13 | 13 | 6 | 7 | 6 | 8 | 77 |

Scores are provisional judgments, not experiment results. Criterion-level rationale for these alternatives is in the research report's Part D. Resolution feasibility rises one point only as a design estimate because the new build narrows to labeled digital FD statements. Novelty does not rise: Addepar's 2026 data-operations preview is direct prior art.

The selected signature is a bounded question that resolves a critical missing field, followed by a revision-safe correction preview and undo. This can be tested against hypothetical RAG/agent teams without inventing their actual submissions. A team with better real-world evidence could outperform this submission.

## Implementation choices

- Python FastAPI and SQLite transactions, one local process, no paid API.
- Plain browser JavaScript and CSS, served by the API: one installation and one launch command. React adds little to this bounded interface.
- Train a character/word TF-IDF logistic field classifier on explicit label examples. Preserve text/page evidence; use an abstention threshold selected from calibration data. Compare against exact and fuzzy dictionaries.
- Deterministic owner/account/institution identity, dated observations, principal/maturity separation and Decimal calculations. No investment advice, autonomous actions or invented numbers.
- Digital PDF and text input only; scanned/unreadable PDFs fail explicitly. English field labels and INR fixed deposits only.
- Synthetic demo personas and sessions exercise server-side resource permissions, but are not production authentication. Bind to loopback only.
- Store original observations separately from append-only canonical revisions. A correction must be supported by visible observations or explicitly attributed user input. Refuse to silently override established identifiers.

## Order of work

1. Local extraction/model and relation engine.
2. Persistent API: upload, compare, clarify, preview, commit, reverse, history.
3. Actual PDF fixtures and complete review UI.
4. Disjoint authored label splits and end-to-end synthetic evaluation; meaningful integration tests. Independent external validation remains future work.
5. Browser verification, reproducible instructions, final case study and demo.

## Hard limits

The local classifier is modest supervised ML, not a foundation model or proof of semantic understanding. Label variants authored by the same developer limit independence. No synthetic benchmark establishes financial safety or production product demand. Model scores are not shown as probabilities of financial correctness. Any claimed gain must survive the strong fuzzy baseline and published error analysis.
