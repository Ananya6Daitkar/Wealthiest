# NestProof audit and hackathon readiness

11 October 2026. Scope: review of the tracked application, tests, evaluation harnesses, interface and submission material; targeted engineering and live browser checks. This is not a penetration test, independent model validation or a production readiness certification.

## Verified requirements and estimated rubric

The supplied Track C brief asks where AI creates meaningful WealthNest value and requires problem, AI justification, behavior, data, architecture, evaluation, risks and reliability. The deliverable is a concise case study with supporting implementation. It explicitly encourages solving one meaningful problem well. It does not supply numerical judging weights or mandate a sponsor model. Cohort team eligibility and any later rules must be confirmed through the official submission channel.

## Assessment and reasons we could lose

1. **Need is plausible, not observed.** No authenticated WealthNest workflow study or customer interviews. A judge can reasonably ask whether equivalent review already exists.
2. **Validation is authored in-house.** Labels, synthetic layouts and cases share their author; perfect regression scores are not external evidence.
3. **Scope is narrow.** English labeled digital INR deposits; no scans, multi-asset layouts or authenticity checks.
4. **AI depth is modest.** Local TF-IDF/logistic regression interprets labels. Core safety is deterministic; the new challenge is not another AI model.
5. **Prior art exists.** Reconciliation and review are established. Differentiation is the complete inspectable household workflow, not invention of reconciliation.
6. **Demo personas are not authentication.** The product must remain local with synthetic data.
7. **Scaling is unproven.** One SQLite process, synchronous parsing and state snapshots; no 10,000-user, load or recovery drill is claimed.
8. **Mobile review was dense.** Small source text and cramped paired evidence reduced readability. Source panels now stack with larger text at the mobile breakpoint.
9. **Financial consistency had gaps.** Optional maturity conflicts could be called the same observation; display rounding hid paise. Both were fixed and exercised.
10. **A rehearsed demo is easy to distrust.** Judges now can change one interpreted field and challenge the same relation engine without modifying evidence or accepting a correction.

The three most serious rejection risks remain unobserved user need, non-independent evaluation and limited format coverage. Engineering can expose these boundaries and improve correctness; it cannot substitute for real user research.

## Prioritization

Judging benefit is estimated, not measured. H/M/L are relative within this project.

| Improvement | Expected benefit | Effort | Technical risk | Demo visibility | Confidence |
|---|---|---|---|---|---|
| Maturity disagreement and paise fixes | High correctness benefit | Low | Medium: decision behavior | High | High |
| Read-only decision challenge | High explainability benefit | Medium | Medium: isolation/access | High | High for demonstrability, unmeasured user value |
| Mobile evidence and focus states | Medium usability benefit | Low | Low | High | Medium; no user study |
| Adversarial API and browser checks | High reliability benefit | Medium | Low | Medium | High within tested scope |
| Pitch and recovery runbook | Medium communication benefit | Low | Low | High | Medium |
| Independent document/user pilot | Highest evidence benefit | External time/access | Medium | High | Not completed |
| OCR, chatbot or public deployment | Unclear benefit to selected problem | High | High | High | Deferred |

## Implemented differentiator

**Challenge this decision** appears within a source comparison. It calls `POST /api/comparisons/{cid}/challenge` with one interpreted field, hypothetical value (or removal) and the review version. The server rechecks actor, current source access and ledger revision, copies the interpreted record, normalizes the hypothetical value and invokes the same reconciliation function.

The response labels actual and hypothetical outcomes. It contains no preview ID and persists no evidence, answer, event or ledger update. Existing source flags remain in force. This is sensitivity analysis on the selected pair; it does not rerun PDF extraction, search the whole ledger, certify provenance or establish causal model explanations. Actual conflict choices already made by a reviewer are not automatically applied to the hypothetical result.

The memorable demonstration is a supported duplicate becoming a conflict after a one-paisa hypothetical change, followed by a missing-reference review when that field is removed. The real principal and revision remain unchanged.

## Engineering changes and evidence

- Same identity and statement date with conflicting maturity amount/date now requires an explicit observation choice. Tests cover preview rejection, selected correction and undo with unchanged principal.
- Display keeps up to two decimal places. The browser showed INR 4,00,000.01 distinctly.
- Challenge tests cover principal differences, missing identity, distinct identity, maturity conflict/inconsistency, invalid fields/amounts, stale version/revision, CSRF, another actor and revoked/quarantined sources.
- Navigation invalidates pending source-selection responses. Mobile evidence is stacked; focus outlines and current navigation semantics were added.
- **74 automated tests pass**, up from 64; one existing Starlette/httpx deprecation warning remains. JavaScript syntax passes.
- **3 existing grouped browser checks rerun successfully:** PDF upload, confirmation gating/commit, receipt link/history/undo.
- **2 new live challenge scenarios passed:** one-paisa conflict and removed-reference review, both showing unchanged revision 1.
- Desktop 1280×900 and mobile 390×844 review layouts inspected. The mobile document width equaled the viewport width (390 pixels). This is not exhaustive accessibility or device certification.
- The 30-case challenge rerun remained ML 30/30, exact 11/30, fuzzy 12/30. Original challenge output is preserved; `evaluation/challenge-regression-results.json` is a regression rerun, not another unseen evaluation.

## Estimated score matrix

This is an explicit planning rubric, not WealthNest's official scoring or a prediction of placement. General anchors: 0–2 absent/broken; 3–4 largely proposed; 5–6 working with major gaps; 7–8 coherent and reproducible within a bounded scope; 9–10 independently substantiated and broadly robust. Fractional scores communicate small estimated differences, not statistical precision.

| Dimension | Weight | Before /10 | After /10 | Basis |
|---|---:|---:|---:|---|
| Problem fit | 20 | 9 | 9 | Clear Track C boundary, integration hypothesis |
| Technical execution | 20 | 8 | 8.5 | Maturity conflict correction, isolated challenge |
| Reliability and evaluation | 20 | 8 | 8.5 | Added negative tests; independent validation still absent |
| Product usability and demo | 15 | 8 | 9 | Visible challenge, precise money, mobile review |
| Differentiation | 10 | 7.5 | 8 | Complete inspectable workflow; prior art remains |
| Feasibility and impact evidence | 10 | 7 | 7 | Runnable; no measured user impact |
| Communication | 5 | 9 | 9 | Architecture, explicit scope, pitch/runbook |
| **Weighted total** | **100** | **81.5** | **85.0** | Subjective estimates under this stated rubric |

Earlier conversational estimates used no fixed weighting and should not be compared as measured improvements. More features alone do not justify 99+. Independent document adjudication and observed user tasks are the next meaningful evidence gains.
