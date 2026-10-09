# NestProof: resolve ambiguous financial imports with the least user effort

**Track C — Artificial Intelligence | Proposal and evaluation scaffold | 9 October 2026**

**Revised design:** targeted clarification, historical context and reversible correction previews. The research document includes a 99/100 aspirational evidence checklist; no achieved 99+ score or measured improvement is claimed.

## Problem

WealthNest’s challenge describes a family dashboard, AI-parsed statement import and a future WealthGPT interface. These depend on a reliable representation of family holdings. When two documents use different labels, dates or identifiers, the same position can look like two assets—or two different positions can look identical.

NestProof proposes an evidence-backed review step before imported observations change canonical holdings. This is an investigated opportunity, **not a reproduced WealthNest defect**. Its frequency and current internal handling still require product validation.

## Investigation

The current [WealthNest homepage](https://wealthnest.ai/) advertises AA/CAS import and family insights. Therefore, another document uploader or overlap dashboard would add little differentiation. Existing products also establish substantial prior art: [Kubera File Import](https://help.kubera.com/article/142-ai-import-files-and-screenshots) supports asset mapping and corrections, and [Addepar](https://addepar.com/blog/inside-addepar-q1-2026) describes traceable, permission-aware portfolio AI.

The narrower opportunity is to combine financial field interpretation, identity and date constraints, evidence review, and a benchmark that exposes harmful merges. [Entity-matching research](https://arxiv.org/abs/2310.11244) supports testing semantic matching; [TimeBench](https://aclanthology.org/2024.acl-long.66/) motivates explicit temporal checks; [financial numerical-reasoning research](https://aclanthology.org/2024.findings-acl.231/) supports keeping calculations outside free-form generation. None establishes product-specific performance.

Additional international research narrows the claim: [Addepar's May 2026 preview](https://addepar.com/blog/key-takeaways-from-addeconf26-that-you-can-use-today) already addresses data-quality investigation and reviewed remediation. [FINBOURNE](https://www.finbourne.com/insight/automating-data-operations-to-enable-growth-how-one-wealth-manager-scaled-efficiently/) documents historical reconciliation; [Canoe](https://canoeintelligence.com/ai/) describes verification and human review; [SGFinDex](https://www.mas.gov.sg/development/fintech/sgfindex) demonstrates consent-controlled retrieval. NestProof adapts these principles to a focused household workflow; it does not claim these components are new.

## Proposed solution

Each imported value becomes an observation with owner, account/folio, instrument, value basis, amount, currency, effective date and exact source evidence. A local model interprets variable labels and layouts. Deterministic code checks identity, time, evidence and numerical consistency. The user reviews a proposed relation before any canonical update; decisions remain reversible.

**Synthetic example:** An FD certificate lists ₹4,00,000 principal and ₹4,32,000 maturity proceeds. A second statement contains a similar owner name, a matching masked suffix and an older date. The system distinguishes principal from maturity value, but refuses to infer identity from a suffix and name alone. It requests stronger evidence rather than inventing a current consolidated figure.

Two different holders owning the same fund are a critical negative control: matching scheme names and amounts must not collapse distinct positions.

The revised workflow asks for the smallest sufficient clarification—for example, the relevant deposit reference instead of another full statement. A bounded constraint-based policy selects questions; AI interprets document fields. Supplied evidence is recorded with its actual provenance. If identity becomes established, show historical context and a supported correction preview before committing. If ambiguity persists, retain review status. Every accepted correction can be reversed.

## Technical approach

`Authorized upload → local parsing → typed extraction → evidence/constraint checks → targeted clarification → historical correction preview → user confirmation → transactional update → undo/history`

The planned MVP uses React, FastAPI, PostgreSQL and local model inference. Freeze scope to synthetic digital FD documents, INR and a small fixed schema; CAS-like support is a stretch after the core works. No autonomous financial actions, public-model upload, vector database or GraphRAG system is needed. Separate financial effective dates from when information was learned; invalidate previews when ledger revisions or permissions change.

The model handles language/layout; code handles authorization, comparisons and arithmetic. Missing identity, conflicting records, unsupported evidence and timeouts result in review. Source observations are preserved separately from accepted canonical positions.

## Evaluation and current implementation status

Delivered: a reproducible 240-case synthetic **text-only** benchmark, an executable deterministic baseline, optional local-model runners and metric-integrity tests. The complete PDF upload/review application is **planned, not built**. Local-model runners have not been evaluated against a running model.

On the 60-case held-out starter split, the measured rule baseline achieved **0.908 macro-F1**, **25/60 correct non-review decisions**, and **35/60 review decisions**. It produced **zero false merges among only 10 same-observation decisions**. Five unfamiliar-label cases were sent to review. These limited, template-generated results do not establish real-world safety or AI superiority. Eight harness tests passed; they are not product validation.

Next compare the rule baseline, a strengthened dictionary/fuzzy baseline, the same local LLM acting directly, and constrained model extraction on identical cases. Measure harmful merges, useful coverage, field accuracy, evidence support, review time, latency and failures. Add unseen PDF layouts and independently authored cases. Publish measured results and errors; do not infer success from the architecture.

New experiment: compare no clarification, complete-document requests, a fixed checklist and targeted clarification with extraction held constant. Measure correct resolution, false resolution, requests and active user time on independently authored cases. A small counterbalanced usability study can explore effort savings; scripted answers cannot substantiate human time savings. These experiments and the revised features are not implemented or measured in the starter benchmark.

## Reliability and privacy

Different verified holders or account references block merging. Dates and valuation bases remain explicit. Exact source citations require support checks, not merely valid links. Access is checked before retrieval and again at evidence and commit boundaries. Documents are untrusted data; the model receives no network or mutation tools. Family membership does not imply permission to see all accounts.

Uncalibrated model confidence is not shown as a probability. User confirmation is recorded as confirmation, not proof of truth. Unknowns remain visible, and accepted decisions can be reversed.

## Expected product impact and next steps

The hypothesis is fewer erroneous canonical additions and less correction effort, improving inputs to both the dashboard and future WealthGPT. No customer savings, production error reduction or adoption gain has been measured.

First validate the current import experience and whether equivalent controls exist. Then build the end-to-end review flow over five focused days, compare against strong baselines, and add a consented shadow evaluation before production automation. The contribution is disciplined AI engineering at a consequential product boundary—not a claim of global novelty.
