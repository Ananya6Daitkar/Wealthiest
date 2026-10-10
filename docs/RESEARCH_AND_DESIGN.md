> Historical research archive — 9 October 2026. Read the [final Track C submission](TRACK_C_SUBMISSION.md) and [final verification](FINAL_VERIFICATION.md) for the delivered build. Planned features, preliminary results and speculative scores below describe earlier stages; they are not current capability or judging claims.

# WealthNest.AI Track C: research, selection and solution design

Research cut-off: **9 October 2026, India time**. Prepared from the supplied challenge and live public sources. This is an opportunity proposal, not a report of a reproduced WealthNest defect. Scores are conservative design assessments, not official scores or selection probabilities. The expert and judge roles below are simulated analytical perspectives, not ten external experts or five independently recruited reviewers.

**Design revision: international research and 99+ ambition.** The selected direction now emphasizes resolving uncertainty with the least user effort: targeted clarification, historical reconstruction, correction previews and permission-aware evidence. Part D preserves the original comparative ranking; Part F defines a 99/100 target and the evidence required to argue for it. This is not an achieved 99+ score. Existing benchmark results refer to the original text-only scaffold; the new features are specified, not implemented.

## PART A: WealthNest product research and verified findings

### Evidence and scope

The supplied **WealthNest.AI Product Engineering Challenge**, pages 1–3, identifies the target as households with ₹50 lakh–₹10 crore in investable assets, describes a family dashboard, smart insights, AI-parsed statement import and the Investment/Insurance/Income Tax/Inheritance framework. It places subscriptions, basket recommendations and WealthGPT on the roadmap. Pages 6–7 give the eight Track C questions answered in Part G. Page 8 requests a concise case study; a working implementation is a bonus. Page 9 gives application **12 October 2026** and submission **25 October 2026** deadlines. Confirm cohort-specific changes through the official application flow. [Application/submission link embedded in the supplied PDF](https://forms.gle/1GXVbVvP3cDL7yzZ6).

No authenticated app session, private engineering documentation, customer interviews or production logs were available. Publicly documented functionality is verified as a company statement, not independently tested behavior. No claims about extraction accuracy, customer loss, support burden or existing reconciliation internals can be established here.

| Finding | Evidence and status | Consequence for the submission |
|---|---|---|
| Consolidated family assets; AA or CAS import | Current [homepage](https://wealthnest.ai/) explicitly describes these | Build on ingestion rather than propose aggregation as new |
| Overlapping funds, idle cash, protection gaps and missing nominees | Current homepage advertises these; example numbers are illustrative | These alone are not defensible new ideas |
| AI statement parsing and family insights | Supplied challenge, pp. 2 and 6 | A proposal can improve reliability without alleging a bug |
| WealthGPT conversational interface | Challenge roadmap, p. 3; [technology page](https://wealthnest.ai/technology/) still labels AI wealth advisor “Coming Soon” | Treat conversational availability as unverified |
| App publicly distributed | [Apple listing](https://apps.apple.com/in/app/wealthnest-ai-family-office/id6757753223) and [contact page](https://wealthnest.ai/contact/) | Product is more than a conceptual landing page |
| Physical asset and insurance support | Homepage/listing describe broad support; contact FAQ says some are forthcoming | Capture app version and actual flows before asserting coverage |
| Family/adviser permissions | Homepage says adviser access unsupported; contact FAQ describes scoped invitations | Documentation inconsistency; availability needs confirmation |
| Privacy posture | Contact page claims sandboxed AI and no public/external LLM sharing | Design local inference; claims are not a security audit |
| RIA status | Current homepage and app listing display INA000022464; older search snapshots said application in progress | Use current company wording; registry verification was not established in this search |

Search snippets contained older versions of the site. Opened pages were preferred over stale snippets. The [about page](https://wealthnest.ai/about/) frames the mission as a personalized family office; the [terms](https://wealthnest.ai/terms-conditions/) describe AI outputs as estimates. Neither source proves any particular deployed model or its performance.

### Opportunity map

| Product stage | Plausible unmet need, explicitly a hypothesis | Incremental AI contribution | Value signal to validate | Priority |
|---|---|---|---|---|
| Import → canonical holdings | Two sources describe one asset differently, or different dates look contradictory | Interpret heterogeneous labels and propose evidence-backed record relations | Wrong additions/merges per 100 imports; correction time | Highest |
| Canonical holdings → WealthGPT | A numerically plausible answer uses stale, incomplete or inaccessible evidence | Interpret intent, then gate answerability using structured evidence | Supported answer rate at useful coverage | High |
| Import → review | User is asked to review entire documents instead of consequential ambiguous fields | Rank uncertain fields by their effect on totals | Minutes and fields reviewed per corrected import | High |
| Family cash flow | Transfers between members look like household spending | Match noisy descriptions across permitted accounts | Reduction in duplicate expenditure classifications | Medium |
| Insurance/inheritance | Important clauses/ownership roles are dispersed | Extract conditions and distinguish roles with citations | Reviewer agreement and completion time | Medium; legal complexity |
| Insights → action | Alert volume exceeds user attention | Learn prioritization from explicit feedback | Useful alerts per session without hiding severe issues | Later; feedback data needed |

The central product hypothesis is that **a trustworthy consolidated figure is more useful than an additional explanation of an unverified figure**. This is an inference from the product workflow, not a measured complaint.

Validate with five consented walkthroughs: ask users to import two representations of the same holding; ask how they distinguish current from historical values; time corrections; ask which evidence would make them accept a merge. Ask the product team whether an equivalent review layer already exists. Do not contact anyone or upload their records without authorization. A confirmed existing implementation changes this into an evaluation/improvement project rather than a new-feature claim.

## PART B: Research papers, competitors, industry trends and opportunity gaps

### Search coverage and limits

Live searches covered arXiv, ACL Anthology, IEEE Xplore, Google Scholar and ACM Digital Library, plus official product and regulatory sources. Scholar and ACM search pages were inaccessible through the browsing tool; targeted ACM queries returned no usable result. This is a focused evidence review, not an exhaustive systematic review. Accessible original papers and abstracts are cited below. Findings are reported qualitatively; limitations and proposed application are our assessment unless stated otherwise. Research performance does not transfer automatically to Indian retail statements.

### Research ledger: 21 relevant papers

Each entry separates problem/technique, reported finding, limitation and implementation implication. The first sixteen plus P18–P21 date from 2023–2026 except explicitly identified foundations.

| ID and original source | Problem and technique | Reported finding | Limitation and WealthNest implementation opportunity |
|---|---|---|---|
| P1. [Docling Technical Report](https://arxiv.org/abs/2408.09869), Auer et al., 2024 | Convert PDFs using layout and table-recognition models | Presents an open, commodity-hardware document conversion pipeline | Conversion is not financial reconciliation. Use as an optional local parser and preserve page/cell provenance |
| P2. [OmniDocBench](https://arxiv.org/abs/2412.07626), Ouyang et al., 2024 preprint | Evaluate diverse PDF content and layout extraction with detailed annotations | Exposes differences between modular and end-to-end parsing systems across document types | Not a household-finance benchmark. Borrow stratified layout/noise evaluation rather than its scores |
| P3. [ColPali](https://arxiv.org/abs/2407.01449), Faysse et al., 2024 | Retrieve visually rich pages using image embeddings and late interaction | Reports stronger retrieval than compared pipelines on ViDoRe | Retrieval does not establish numerical truth; index/compute overhead. Useful later for finding evidence pages, unnecessary for six-document MVP |
| P4. [LayoutLMv3](https://arxiv.org/abs/2204.08387), Huang et al., 2022 foundation | Joint text/image masking and word-patch alignment for document understanding | Reports strong performance across form, receipt and layout tasks | Fine-tuning needs labels; benchmark domains differ. Supports retaining layout, not training a new model in five days |
| P5. [FinQA](https://aclanthology.org/2021.emnlp-main.300/), Chen et al., 2021 foundation | Financial QA with annotated numerical reasoning programs | Shows challenging multi-step reasoning and a gap to expert humans | Corporate reports differ from CAS. Adopt explicit executable calculations and gold programs |
| P6. [TAT-QA](https://aclanthology.org/2021.acl-long.254/), Zhu et al., 2021 foundation | Hybrid table/text financial QA with numerical operations | Introduces a benchmark and specialized reasoning approach for mixed evidence | Does not test family ownership or ingestion. Annotate both cell and surrounding label evidence |
| P7. [ConvFinQA](https://aclanthology.org/2022.emnlp-main.421/), Chen et al., 2022 foundation | Conversational chains of financial numerical reasoning | Finds long reasoning chains challenging for neural-symbolic and prompting methods | Conversation accuracy is not permission safety. Test follow-up questions that change date/person scope |
| P8. [Evaluating LLMs’ Mathematical Reasoning in Financial Document Question Answering](https://aclanthology.org/2024.findings-acl.231/), Srivastava et al., 2024 | Compare models/prompts across four financial QA datasets; EEDP prompting | Reports performance sensitivity to table complexity and reasoning steps | Prompt improvements do not certify arithmetic. Use Decimal/SQL for totals and test steps separately |
| P9. [Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/), Liu et al., 2024 | Vary evidence position in long-context retrieval/QA | Relevant information in the middle can be used less reliably | Model-dependent and not a forecast for all newer models. Test reordered statements and keep evidence bundles small |
| P10. [Self-RAG](https://arxiv.org/abs/2310.11511), Asai et al., 2023 preprint/ICLR 2024 | Train retrieval and reflection tokens | Reports improved factuality and citation behavior across evaluated tasks | Self-critique is fallible; specialized training is out of scope. Borrow bounded retrieve/check/abstain control, not claims of reproducing Self-RAG |
| P11. [From Local to Global: A Graph RAG Approach to Query-Focused Summarization](https://arxiv.org/abs/2404.16130), Edge et al., 2024; revised 2025 | Build entity graphs and community summaries for global questions | Reports improved comprehensiveness/diversity on global sensemaking | Not designed to reconcile decimal amounts. Use relational provenance edges; omit community-summary GraphRAG from MVP |
| P12. [Entity Matching using Large Language Models](https://arxiv.org/abs/2310.11244), Peeters, Steiner and Bizer, 2023 | Prompt/fine-tune LLMs to match differently described entities | Reports competitive matching with fewer task examples and sensitivity to prompt choices | General benchmarks do not prove financial identity safety. Use semantic proposals constrained by holder/account identifiers; test hard negatives |
| P13. [TimeBench](https://aclanthology.org/2024.acl-long.66/), Chu et al., 2024 | Hierarchical temporal reasoning benchmark | Finds substantial gaps and uneven capabilities across temporal tasks | General language benchmark, not investment valuation. Store observation and ingestion time separately; compare aligned dates |
| P14. [Detecting hallucinations in large language models using semantic entropy](https://www.nature.com/articles/s41586-024-07421-0), Farquhar et al., 2024 | Cluster sampled answers by meaning to estimate uncertainty | Detects a subset of hallucinations described as confabulations | Consistent falsehoods can escape; repeated calls cost time. Optional disagreement signal, never a truth certificate |
| P15. [Conformal Language Modeling](https://arxiv.org/abs/2306.10193), Quach et al., 2023 | Calibrate sampling and rejection rules to produce acceptable answer sets | Develops statistical guarantees under its assumptions and evaluates multiple generation tasks | Exchangeability/distribution shift matter. Motivate held-out calibration; do not claim conformal guarantees for a heuristic threshold |
| P16. [FActScore](https://arxiv.org/abs/2305.14251), Min et al., 2023 | Break outputs into atomic facts and verify support | Demonstrates informative factual-precision measurement and automated approximation | Original biography setting and imperfect automated judges. Count supported financial claims with evidence, dates and units checked |
| P17. [RAGAs](https://aclanthology.org/2024.eacl-demo.16/), Es et al., 2024 | Reference-free metrics for retrieval, faithfulness and generation | Provides a framework for faster component evaluation | LLM judges can share generator errors. Use as diagnostics only; gold records and human audits decide correctness |
| P18. [Toolformer](https://arxiv.org/abs/2302.04761), Schick et al., 2023 | Learn when/how to call external tools | Reports improved downstream zero-shot performance using tool access | Does not solve authorization or safe tool execution. Expose read-only typed lookup/calculation functions, never arbitrary SQL |
| P19. [Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173), Greshake et al., 2023 | Place hostile instructions in retrieved content | Demonstrates practical manipulation of LLM-integrated systems | Prompt filters alone are insufficient. Treat PDFs as data, deny model network/write tools, and test document-borne instructions |
| P20. [Advanced Layout Analysis Models for Docling](https://arxiv.org/abs/2509.11720), Livathinos et al., 2025 | Train detector variants for document layout; evaluate quality/runtime | Reports improvements over Docling’s previous layout baseline | Proprietary training data and hardware-specific runtime limit replication. Pin exact parser/model versions; measure on the demo laptop |
| P21. [Conformal Language Modeling via Posterior Sampling](https://arxiv.org/abs/2606.03731), Emmenegger et al., June 2026 preprint | Condition generation on calibrated high-scoring regions | Reports utility improvements with risk-control guarantees in studied tasks | Recent preprint, nonfinancial case studies. Research extension only, not a five-day dependency |

Additional domain coverage: [Self-Supervised Learning for Time Series Analysis](https://ieeexplore.ieee.org/document/10496248), IEEE TPAMI 2024, surveys generative/contrastive/adversarial methods and anomaly tasks. It motivates learning from sparse labels, but does not show that household outliers are fraud. [FederatedScope-LLM](https://arxiv.org/abs/2309.00363), Kuang et al., 2023, provides federated parameter-efficient tuning infrastructure; keeping data local does not itself prevent gradient leakage. [Privacy-preserving entity resolution with homomorphic encryption](https://arxiv.org/abs/2405.18430), Yao et al., 2024, reports a feasible healthcare pipeline; its cross-organization cryptographic threat model and cost are unnecessary for a single-user synthetic demo. These are alternatives considered, not technologies to add for appearance.

### Competitor reality check

| Company/category | Publicly documented capability | What that invalidates | Remaining testable angle |
|---|---|---|---|
| Addepar | [Q1 2026 update](https://addepar.com/blog/inside-addepar-q1-2026) describes Addison’s portfolio-grounded, permission-aware, traceable outputs | “First financial AI with citations/permissions” | A compact Indian-family import reconciliation workflow with an openly reproducible error benchmark |
| Addepar document operations | [2025 Alts Data Management sheet](https://addepar.com/assets/addepar-alts-data-management-overview-fact-sheet.pdf) describes extraction plus human verification; some reconciliation features were marked planned | “AI extraction with humans is new” | Student-scale implementation and a narrowly demonstrated net-worth failure mode; do not treat planned features as shipped |
| Kubera | [File Import help](https://help.kubera.com/article/142-ai-import-files-and-screenshots), updated 28 July 2026: imports documents/screenshots, maps existing manual assets and accepts corrections | “AI statement upload and asset matching is new” | Evidence- and date-aware conflict review with false-merge evaluation; absence in this help article is not proof of absence in product |
| Empower | [Financial tools](https://www.empower.com/tools) cover aggregation, portfolio analysis, budgeting and retirement | A consolidated dashboard or allocation checker as innovation | Data-quality gate before analytics; US products are not evidence of Indian demand |
| Monarch | [Tracking](https://www.monarchmoney.com/features/recurring) describes aggregation, AI categorization and review | Basic expense classification or household dashboard | Cross-source financial-document semantics beyond spending categories |
| Copilot Money | [Quick Start Guide](https://help.copilot.money/en/articles/11157550-quick-start-guide), 27 August 2026, describes learned categorization and user review | “Personalized review loop” alone | Import integrity and explicit evidence limitations |
| Plaid | [Enrich](https://plaid.com/docs/enrich/) enriches transactions, with documented US/Canada scope | Merchant cleanup as original financial AI | Do not assume Plaid substitutes for Indian AA; reconcile documents with authorized structured records |
| Google Document AI | [Evaluation documentation](https://docs.cloud.google.com/document-ai/docs/evaluate) exposes entity precision/recall and confidence thresholds | Extraction confidence or review thresholds as novelty | Evaluate downstream balance integrity, not only extraction F1 |
| INDmoney | [Family Accounts](https://www.indmoney.com/networth/family-accounts) shows member and combined wealth views | Family aggregation as differentiation | Explain why a particular imported record may change the consolidated figure incorrectly |

**Gap conclusion:** available evidence supports a useful product specialization, not a claim of global invention. Existing products cover most individual ingredients. Differentiation must come from a tested combination: financial field semantics + identity/time constraints + source evidence + reversible human decisions + explicit evaluation of harmful merges.

### Dated developments and Indian context

1. **3 April 2026, Addepar first-party product update:** Addison demonstrates the market direction toward integrated, traceable portfolio AI. This is vendor evidence of a release, not independent proof of ROI. [Update](https://addepar.com/blog/inside-addepar-q1-2026).
2. **14 April 2026, INDmoney product article:** family net-worth tracking is already a marketed Indian capability. This is competitive evidence, not a market-size study. [Article](https://www.indmoney.com/blog/how-to-track-your-family-net-worth-on-indmoney).
3. **28 July 2026, Kubera help update:** document imports and corrective mapping are concrete existing workflows. Good reconciliation UX must exceed a generic upload/confirm screen. [Help](https://help.kubera.com/article/142-ai-import-files-and-screenshots).
4. **August 2025, RBI FREE-AI committee report:** RBI’s [report index](https://m.rbi.org.in/Scripts/BS_ViewPublicationReport.aspx) lists the responsible-AI report. Treat committee recommendations as guidance, not automatic binding rules for this prototype. No specific compliance certification follows from citing it.
5. **14 November 2025 publication, DPDP Rules and enforcement materials:** [MeitY official page](https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa?pageTitle=Digit) includes a December 2025 corrigendum. The [notified rules](https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf) prescribe phased commencement. As of this report, do not claim every rule is already operative. Build consent, scoped access, deletion and retention controls; production applicability needs provision-specific review.
6. **Indian account structure matters:** [AMFI-hosted scheme documentation](https://portal.amfiindia.com/spages/13140.pdf) describes CAS consolidation using PAN and holding pattern. A matching scheme name is insufficient to establish the same holding; first-holder and joint-holding distinctions matter. Account access and beneficial ownership are different concepts.
7. **AA role separation:** [RBI’s financial awareness material](https://www.rbi.org.in/commonman/images/FAME202426022024.pdf) describes consent-based sharing and the AA not seeing/storing financial information. That statement about the AA must not be generalized to every downstream financial-information user. Family membership alone is not consent.

There is no verified WealthNest fraud incidence, user error rate or monetary-loss statistic here. The project targets data integrity, not fraud adjudication or investment-return prediction. Tax treatment, nominee rights and inheritance ownership should not be inferred from a statement label.

### International research update: what to adapt

Public sources checked on 9 October 2026 establish documented capabilities or previews, not independently verified accuracy. Adapt the engineering principles to Indian households; do not claim invention of reconciliation.

| Country / reference | Verified approach | NestProof adaptation | Validation required |
|---|---|---|---|
| UK — [FINBOURNE / OMBA](https://www.finbourne.com/insight/automating-data-operations-to-enable-growth-how-one-wealth-manager-scaled-efficiently/) | Historical reconstruction, reconciliation and data lineage | Track when a financial fact applied and when the system learned it; explain late corrections | Reconstruct both historical views correctly; an old upload must not overwrite a newer valuation |
| US — [Canoe Intelligence](https://canoeintelligence.com/ai/) | Multiple verification methods, field-specific checks and human review | Compare parser extraction, model interpretation and arithmetic checks; highlight disagreement | Test correlated mistakes; agreement is not proof when methods share bad OCR |
| US — [Addepar, May 2026](https://addepar.com/blog/key-takeaways-from-addeconf26-that-you-can-use-today) | Previewed discrepancy investigation and human-reviewed remediation; describes statement review/import workflows | Preview proposed corrections with evidence and their effect on the represented portfolio | Direct prior art for reconciliation; distinguish preview from general availability |
| Singapore — [MAS: SGFinDex](https://www.mas.gov.sg/development/fintech/sgfindex) | Consent-controlled financial-data retrieval | Apply authorization to clarification questions, evidence, historical views and correction previews | No question may reveal hidden records; this is inspiration, not SGFinDex integration or a replacement for Indian AA requirements |

**Competitive correction:** Addepar's data-operations preview overlaps more directly with NestProof than its portfolio assistant alone. This supports the commercial relevance of the workflow but weakens broad novelty claims. The original 85 is a provisional historical assessment, not a floor that automatically rises with features.

**Revised differentiation hypothesis:** Help an Indian household resolve an ambiguous import using the smallest sufficient, authorized clarification, then explain and reverse the supported change. Evaluate user effort and harmful decisions together. The contribution is the constrained workflow and evidence, not any individual component.

Inheritance handover, such as [Kubera's emergency-contact workflow](https://help.kubera.com/article/10-ensure-safe-transfer-portfolio-to-beneficiary), was considered but excluded: it adds another product problem without improving import reconciliation. Also defer trading agents, multi-currency tax engines and broad insurance interpretation.

## PART C: Ten differentiated AI ideas

All ten are proposed extensions whose need and overlap with internal product work require validation. Each is deliberately narrower than a generic assistant.

### 1. NestProof — evidence-backed import reconciliation

1. **Name:** NestProof.
2. **Pitch:** Resolve consequential import ambiguity with the smallest sufficient clarification before changing family wealth.
3. **Problem:** Different document descriptions can represent one position, different periods or incompatible facts.
4. **Importance:** A wrong merge or duplicate distorts every downstream total and insight.
5. **User:** Family member consolidating CAS, bank and deposit records.
6. **Existing limits:** Import/matching exists; public evidence does not establish a transparent temporal conflict review with a published safety benchmark.
7. **Difference:** Connect source evidence, targeted clarification, historical context and reversible correction previews; measure the effort needed for a safe resolution.
8. **AI need:** Interpret varied labels/layout and noisy descriptions; arithmetic and identity constraints remain deterministic.
9. **Data:** Synthetic CAS-like holdings, FD certificates and account-summary statements with controlled ground truth.
10. **Methods:** Layout extraction, local structured LLM extraction, constrained candidate matching, calibrated acceptance later.
11. **Architecture:** PDF → evidence spans → typed records → candidate relations → deterministic checks → review → versioned ledger.
12. **Workflow:** Upload, inspect a flagged pair, supply targeted evidence, preview the correction, confirm and retain a reversible audit trail.
13. **Example:** ₹4 lakh principal versus ₹4.32 lakh maturity amount is not a current-balance contradiction; unknown valuation date stays unresolved.
14. **Impact:** Hypothesized reduction in corrections and erroneous totals.
15. **Difficulty:** Medium-high; identity safety is hardest.
16. **Feasibility:** Strong if limited to two document families, no automated ambiguous merges.
17. **Risks:** False merge, misleading certainty, source leakage, propagation of bad OCR.
18. **Success:** Higher useful decision coverage than rules at the same harmful-decision budget; zero observed unauthorized evidence exposure.
19. **Research:** P1, P8, P12, P13, P15, P19.
20. **Judge objection:** “This is ordinary reconciliation.” Answer with a held-out semantic/layout ablation showing exactly where AI adds value; narrow claims if it does not.

### 2. AnswerPermit — a pre-answer check for WealthGPT

1. **Name:** AnswerPermit.
2. **Pitch:** Determine whether a financial question is answerable before generating its answer.
3. **Problem:** Plausible answers can rely on missing, stale or unshared records.
4. **Importance:** False completeness is more dangerous than an explicit request for information.
5. **User:** Family member asking scoped portfolio questions.
6. **Existing limits:** RAG citations establish retrieval, not completeness or permission to aggregate.
7. **Difference:** Compile a question into required fields, dates, coverage and authorized evidence; answer/clarify/abstain.
8. **AI need:** Map varied language to constrained financial intent and missing-information questions.
9. **Data:** Synthetic authorized ledger and questions with answerability labels.
10. **Methods:** Intent parsing, typed query planner, retrieval, support checking.
11. **Architecture:** Question → schema-bound plan → authorization → SQL → evidence gate → templated answer.
12. **Workflow:** Ask; receive scoped answer or one specific clarification.
13. **Example:** “Our equity exposure?” → “I can calculate exposure for the shared accounts; two portfolios have no current valuations.” Only reveal missing accounts if their existence is authorized.
14. **Impact:** Fewer unsupported answers and clearer data-completion prompts.
15. **Difficulty:** Medium.
16. **Feasibility:** High for five supported intents.
17. **Risks:** Permission leaks, incorrect intent, misleading coverage denominators.
18. **Success:** Unsupported numerical claims below target with measured answer coverage; privacy suite passes.
19. **Research:** P5, P7, P9, P10, P16–P19.
20. **Objection:** “Another RAG wrapper.” Must prove a pre-answer evidence contract improves on equally scoped baseline RAG.

### 3. ReviewLens — impact-aware review of uncertain extraction

1. **Name:** ReviewLens.
2. **Pitch:** Ask users to review the few uncertain fields that matter most.
3. **Problem:** Uniform review wastes attention on harmless uncertainties while missing material ones.
4. **Importance:** Small digit/date/field-role mistakes can dominate a portfolio total.
5. **User:** Importing family member and consented reviewer.
6. **Existing limits:** Confidence thresholds do not rank consequence; vendor confidence is not calibrated correctness.
7. **Difference:** Rank review by plausible error cost and sensitivity of downstream totals.
8. **AI need:** Model field uncertainty across unfamiliar layouts; simulate effects deterministically.
9. **Data:** Synthetic documents with field corruptions and timed review tasks.
10. **Methods:** Parser disagreement, confidence calibration, active-review selection.
11. **Architecture:** Extraction → uncertainty features → sensitivity computation → review queue.
12. **Workflow:** Correct highlighted cells in priority order; stop when residual risk is below a declared threshold.
13. **Example:** An uncertain maturity date blocks classification; a cosmetic bank-name punctuation difference does not.
14. **Impact:** Less review time per safe import.
15. **Difficulty:** Medium.
16. **Feasibility:** High with 10–15 critical fields.
17. **Risks:** Underestimating rare errors; nudging reviewer acceptance.
18. **Success:** Material errors caught per reviewed field and minutes, versus random/confidence-only queues.
19. **Research:** P2, P14, P15, P17.
20. **Objection:** “A sorting heuristic.” AI contribution must improve uncertainty ranking on held-out layouts beyond field-size rules.

### 4. TransferWeave — household cash-flow attribution

1. **Name:** TransferWeave.
2. **Pitch:** Separate movement within a family from new income and real spending.
3. **Problem:** Differently described debit/credit legs are counted independently.
4. **Importance:** Distorts household savings and liquidity analysis.
5. **User:** Household with multiple consented bank accounts.
6. **Existing limits:** Exact amount/date rules struggle with fees, delayed postings and truncated descriptions.
7. **Difference:** Explain paired and unpaired legs, with role/date uncertainty.
8. **AI need:** Interpret counterparty descriptions; deterministic conservation constraints arbitrate.
9. **Data:** Synthetic paired transfers, split settlements, fees, refunds and hard negatives.
10. **Methods:** Text embeddings or character-feature classifier; constrained bipartite matching.
11. **Architecture:** Transactions → candidate blocks → semantic score → amount/time constraints → confirmation.
12. **Workflow:** Review proposed pair; cash-flow view recalculates without hiding records.
13. **Example:** “UPI/NAL/...” debit and “IMPS/N SH...” credit → possible internal transfer, not confirmed income.
14. **Impact:** More accurate cash-flow trends.
15. **Difficulty:** Medium.
16. **Feasibility:** High for two accounts; harder for multi-leg settlements.
17. **Risks:** Concealing legitimate spending, family privacy, false transfer pairing.
18. **Success:** Pair precision/recall and household cash-flow error against truth.
19. **Research:** P12, P13; Plaid enrichment as competitive prior art.
20. **Objection:** “Rules suffice.” Evaluate fee/delay/noisy-name cases and keep the rule solution if it wins.

### 5. ClauseCompass — insurance-condition evidence map

1. **Name:** ClauseCompass.
2. **Pitch:** Make a policy’s documented conditions visible before users overestimate protection.
3. **Problem:** Sum assured alone omits exclusions, waiting periods and endorsements.
4. **Importance:** Apparent coverage can differ from conditional coverage.
5. **User:** Family member reviewing policy records.
6. **Existing limits:** Gap calculators often depend on structured cover amounts; generic summaries omit exception relationships.
7. **Difference:** Link coverage condition → exception → endorsement → page evidence.
8. **AI need:** Extract compositional clauses and references from varied language.
9. **Data:** Synthetic policy clauses; publicly licensed wording only if permitted.
10. **Methods:** Clause extraction, retrieval and entailment proposals with review.
11. **Architecture:** Policy pages → clause graph → scenario query → cited conditional response.
12. **Workflow:** Pick a scenario; inspect relevant conditions; seek insurer confirmation where needed.
13. **Example:** “Hospitalization covered?” → “Waiting-period clause applies; start date missing, so eligibility cannot be determined.”
14. **Impact:** Better questions and fewer unsupported coverage assumptions.
15. **Difficulty:** High.
16. **Feasibility:** Moderate for one policy family and three clause types.
17. **Risks:** Incorrect legal interpretation or claim-approval implication.
18. **Success:** Clause recall, exception linkage accuracy and unsupported eligibility-claim rate.
19. **Research:** P3, P9, P16, P19.
20. **Objection:** “Who validates coverage?” Requires domain review; never promise claim eligibility.

### 6. ContinuityMap — inheritance-record readiness

1. **Name:** ContinuityMap.
2. **Pitch:** Identify unresolved document and role dependencies in a family’s continuity plan.
3. **Problem:** Owner, nominee, insured person and intended beneficiary can be confused.
4. **Importance:** Missing or misunderstood records complicate continuity.
5. **User:** Family organizer planning information readiness.
6. **Existing limits:** Nominee reminders exist; a checkbox cannot interpret differing document roles.
7. **Difference:** Evidence-backed role map and a list of questions for qualified review.
8. **AI need:** Extract relationships from heterogeneous documents; legal outcomes remain outside automation.
9. **Data:** Synthetic ownership schedules, policy roles and document inventories.
10. **Methods:** Relation extraction plus typed graph constraints.
11. **Architecture:** Document extraction → role graph → missing-evidence checks → readiness review.
12. **Workflow:** Confirm each role and access condition; export a record checklist.
13. **Example:** Policy nominee listed, succession instructions absent → document question, not an ownership conclusion.
14. **Impact:** Better information readiness.
15. **Difficulty:** High.
16. **Feasibility:** Moderate if confined to role extraction.
17. **Risks:** Sensitive family relationships, nominee/owner conflation, legal misinformation.
18. **Success:** Role extraction precision, severe role-confusion rate, checklist usefulness.
19. **Research:** P4, P11, P12, P19.
20. **Objection:** “This is legal advice.” Limit to record evidence and explicitly unknown legal interpretation.

### 7. LiquidityWindow — document-aware cash availability

1. **Name:** LiquidityWindow.
2. **Pitch:** Explain which recorded assets might be available for a stated date, and what is unknown.
3. **Problem:** Net worth obscures lock-ins, maturity conditions and withdrawal restrictions.
4. **Importance:** A wealthy household can still lack near-term usable cash.
5. **User:** Family planning a large payment.
6. **Existing limits:** Cash dashboards do not necessarily interpret contract restrictions.
7. **Difference:** Cited availability intervals with unresolved restrictions excluded from firm totals.
8. **AI need:** Extract contractual conditions; date arithmetic is deterministic.
9. **Data:** Synthetic deposit/loan terms and upcoming obligations.
10. **Methods:** Temporal/condition extraction, constraint evaluation.
11. **Architecture:** Clauses → availability intervals → scenario calculator → evidence explanation.
12. **Workflow:** Enter payment date; inspect confirmed/conditional amounts.
13. **Example:** FD matures after tuition date; premature-withdrawal conditions are absent → no claim of full availability.
14. **Impact:** Better liquidity conversations, not guaranteed funding plans.
15. **Difficulty:** Medium-high.
16. **Feasibility:** Moderate for FDs only.
17. **Risks:** Hidden penalties, incomplete obligations, inferred liquidity.
18. **Success:** Date/condition accuracy and false “available” classifications.
19. **Research:** P8, P13, P16.
20. **Objection:** “A calendar can do this.” Value depends on extracting restrictions that are not structured already.

### 8. ExposureThreads — look-through economic exposure

1. **Name:** ExposureThreads.
2. **Pitch:** Explain shared issuer exposure across differently named family investments.
3. **Problem:** Brand, fund and issuer aliases hide common underlying exposure.
4. **Importance:** Apparent diversification can overstate independence.
5. **User:** Family reviewing allocation.
6. **Existing limits:** Fund-overlap insights already exist in WealthNest; simple overlap is rejected.
7. **Difference:** Resolve issuer relationships across documents and disclose dated/partial look-through coverage.
8. **AI need:** Alias/entity extraction; exposure sums are deterministic.
9. **Data:** Dated public fund disclosures, synthetic portfolios, issuer reference map.
10. **Methods:** Entity resolution and ownership/exposure graph.
11. **Architecture:** Disclosures → issuer mapping → weights → family aggregation with coverage mask.
12. **Workflow:** Inspect top common issuer and unresolved allocations.
13. **Example:** Two funds plus direct holding share an issuer; missing fund disclosure prevents a complete percentage.
14. **Impact:** More interpretable concentration analysis.
15. **Difficulty:** High because reference data must be correct/current.
16. **Feasibility:** Moderate for a tiny frozen universe.
17. **Risks:** Stale holdings, false issuer links, accidental investment advice.
18. **Success:** Entity precision, exposure error, dated coverage completeness.
19. **Research:** P11–P13.
20. **Objection:** “We already have overlap.” Must demonstrate a material additional relationship or reject the project.

### 9. QuietSignal — reviewable household anomaly triage

1. **Name:** QuietSignal.
2. **Pitch:** Surface unusual financial changes with evidence and benign explanations to check.
3. **Problem:** Important deviations are buried in ordinary activity.
4. **Importance:** Users may miss duplicate charges, unexpected fees or unfamiliar patterns.
5. **User:** Household reviewing periodic activity.
6. **Existing limits:** Fixed thresholds cannot adapt to household seasonality; anomaly does not imply fraud.
7. **Difference:** Personalized residual anomaly score plus source-linked explanation candidates.
8. **AI need:** Learn normal patterns; use robust statistics before deep models.
9. **Data:** Synthetic 12-month transaction histories with seasonal benign and injected unusual events.
10. **Methods:** Robust seasonal residuals/Isolation Forest; optional text classification.
11. **Architecture:** History → features → anomaly ranking → human dismissal/confirmation.
12. **Workflow:** Review small queue; label explanation without filing accusations.
13. **Example:** Large annual premium is seasonal; novel duplicate debit gets higher review priority.
14. **Impact:** Higher useful-alert density.
15. **Difficulty:** Medium-high.
16. **Feasibility:** Moderate; realistic validation is difficult.
17. **Risks:** False alarms, drift, synthetic regularity, fraud overclaiming.
18. **Success:** Precision@5 and false alerts per household-month; compare robust rules.
19. **Research:** IEEE time-series survey; P16 for explanation support.
20. **Objection:** “Your anomalies were invented to suit your model.” Independent stress cases and real validation would be essential.

### 10. ShareScope — family disclosure preview

1. **Name:** ShareScope.
2. **Pitch:** Preview what a document or answer would disclose before sharing it with a family role.
3. **Problem:** A useful summary can inadvertently reveal restricted account/person details.
4. **Importance:** Family relationships do not imply universal financial visibility.
5. **User:** Account owner granting limited access.
6. **Existing limits:** Record permissions may not capture sensitive text embedded in attachments.
7. **Difference:** Locate sensitive spans and show a role-specific evidence preview; enforcement is deterministic.
8. **AI need:** Detect contextual entities and sensitive relations in unstructured content.
9. **Data:** Synthetic mixed-visibility documents and access policies.
10. **Methods:** Named-entity detection, classification, deterministic allowlists and redaction.
11. **Architecture:** Document → span labels → policy projection → preview → authorized share.
12. **Workflow:** Select audience; review redacted preview; explicitly confirm.
13. **Example:** Share asset category while suppressing account ID and another member’s transaction detail.
14. **Impact:** Safer collaboration and clearer consent.
15. **Difficulty:** High; indirect inference remains.
16. **Feasibility:** Moderate for fixed role policies and synthetic records.
17. **Risks:** Missed sensitive spans, re-identification, aggregate differencing.
18. **Success:** Sensitive-span recall plus end-to-end unauthorized disclosure tests, not redaction accuracy alone.
19. **Research:** P19; privacy-preserving entity-resolution/federated research above.
20. **Objection:** “An LLM cannot enforce privacy.” Correct: it suggests labels; unknown classifications deny sharing.

## PART D: Critical 100-point scoring and ranking

**Version note:** This is the original selection assessment, before the additional international prior-art review and revised specification. It is not a reassessment of implemented features. Part F's 99-point target is aspirational and separate.

The requested rubric is used unchanged. O=originality /15, U=user problem /15, W=WealthNest fit /15, AI=AI appropriateness /15, F=feasibility /10, E=evaluation /10, T=trust /10, D=demo /10. These are comparative judgments with roughly ±5-point uncertainty. Small differences are not statistically meaningful. Unvalidated user demand prevents 95+ ratings.

| Rank | Idea | O | U | W | AI | F | E | T | D | Total |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | NestProof | 11 | 13 | 15 | 12 | 8 | 9 | 8 | 9 | **85** |
| 2 | AnswerPermit | 9 | 13 | 15 | 12 | 9 | 9 | 8 | 8 | **83** |
| 3 | ReviewLens | 10 | 12 | 14 | 11 | 9 | 9 | 8 | 8 | **81** |
| 4 | TransferWeave | 9 | 12 | 12 | 11 | 8 | 9 | 8 | 8 | **77** |
| 5 | ClauseCompass | 11 | 13 | 13 | 13 | 6 | 7 | 6 | 8 | **77** |
| 6 | LiquidityWindow | 10 | 13 | 13 | 10 | 7 | 8 | 7 | 8 | **76** |
| 7 | ContinuityMap | 11 | 12 | 13 | 11 | 6 | 7 | 6 | 8 | **74** |
| 8 | ShareScope | 11 | 13 | 12 | 10 | 6 | 8 | 6 | 7 | **73** |
| 9 | ExposureThreads | 8 | 12 | 13 | 10 | 6 | 8 | 7 | 8 | **72** |
| 10 | QuietSignal | 8 | 12 | 12 | 11 | 7 | 6 | 6 | 8 | **70** |

Tie-break: TransferWeave beats ClauseCompass because it has more objective ground truth and lower interpretation risk.

### Concrete rationale for every criterion score

| Idea | O justification | U justification | W justification | AI justification | F justification | E justification | T justification | D justification |
|---|---|---|---|---|---|---|---|---|
| NestProof | Existing reconciliation limits novelty to interaction/evaluation | Incorrect totals have broad consequences, prevalence unknown | Directly extends stated import capability | Language/layout valuable; rules do arithmetic | Two document families fit; OCR is scope risk | False merges and accepted-record accuracy measurable | Abstention/review help; identity error remains | Before/after evidence makes a clear demonstration |
| AnswerPermit | Crowded trustworthy-RAG category | Unsupported answers can mislead | Direct WealthGPT roadmap alignment | Intent parsing useful, planner must be constrained | Five intents practical | Support and coverage can be labeled | Access and coverage errors persist | Strong failure demo but less distinctive |
| ReviewLens | Impact/uncertainty combination useful, not novel research | Reduces correction burden; no observed workload | Improves import experience | Calibration useful, ranking partly heuristic | Small interface and model surface | Time/field-review trials concrete | Review protects but can bias users | Clear interactive cell prioritization |
| TransferWeave | Existing reconciliation techniques | Cash-flow distortion plausible | Supports family intelligence, less direct challenge emphasis | Description matching adds beyond exact rules | Multi-leg transfers must be excluded | Pair labels easy to construct | Misclassification reversible; privacy delicate | Intuitive two-account demo |
| ClauseCompass | Condition/exception map differentiates summaries | High consequence of misunderstood cover | Fits Insurance pillar | Semantic clause extraction genuinely difficult | Domain breadth hard in five days | Ground truth requires expertise | Eligibility errors have serious consequences | Ambiguous endorsement is compelling |
| LiquidityWindow | Conditional availability is useful specialization | Timing mismatch materially matters | Fits family planning | Only unstructured restrictions need AI | Narrow FD subset practical | Date/availability labels measurable | Unknown conditions must block certainty | Date slider shows consequences well |
| ContinuityMap | Role evidence graph more useful than checklist | Continuity matters; frequency episodic | Fits Inheritance pillar | Relation extraction appropriate | Legal/role complexity constrains scope | Expert labels needed | Ownership implications hazardous | Role conflict visually clear |
| ShareScope | Disclosure preview useful | Privacy consequences high | Family access relevance; availability uncertain | Sensitive spans benefit, policies do not | Inference leakage hard to cover | Attack suites measurable | No finite test suite proves confidentiality | Security story harder to show without theatrics |
| ExposureThreads | WealthNest overlap already exists | Concentration matters | Direct investment relevance | Alias resolution only part needing AI | Dated issuer data costly | Exposure error objectively measurable | Stale/incorrect mappings can mislead | Shared-issuer example clear |
| QuietSignal | Anomaly detection is crowded | Unusual charges matter | Fits insights but not established pain | ML plausible with enough history | Synthetic demo easy, credibility hard | Rare-event realism weak | False accusations/alert fatigue | Easy to dramatize, hard to substantiate |

### Five simulated judges' independent lenses

Each cell is the principal objection from that lens, rather than a fabricated independent experiment. The rubric totals above synthesize all five lenses.

| Idea | A: Innovation | B: Technical depth | C: Value | D: Feasibility | E: Trust |
|---|---|---|---|---|---|
| NestProof | Prior art substantial | Require held-out label interpretation | Prove correction pain | Limit identity classes | No silent ambiguous merges |
| AnswerPermit | Familiar RAG guardrails | Typed answerability adds rigor | Depends on GPT adoption | Five intents manageable | Hidden-account existence can leak |
| ReviewLens | Impact-aware review is incremental | Calibrate, do not self-score | Time savings measurable | Best narrow build | Human approval is not truth |
| TransferWeave | Bank reconciliation known | Hard negatives matter | Household cash flow useful | Avoid multi-party settlement | False exclusions hide spending |
| ClauseCompass | Strong relationship insight | Clause scope is hard | Potentially high value | Expert availability limits | Never promise eligibility |
| LiquidityWindow | Not just maturity reminders | Conditions must drive model need | Relevant planning question | One asset class | Incomplete liabilities invalidate totals |
| ContinuityMap | Readiness not legal automation | Role disambiguation worthwhile | Long-term rather than daily | Exclude succession computation | Nominee is not universal owner |
| ShareScope | Preview is useful | AI not security boundary | Collaboration prerequisite | Redaction coverage difficult | Fail closed on unknown spans |
| ExposureThreads | Existing overlap dominates | Matching not forecasting | Increment needs proof | Data sourcing is bottleneck | Date completeness required |
| QuietSignal | Generic without data insight | Small histories weaken model | Alert burden could rise | Easy toy, hard validation | Outlier is not fraud |

| Idea | Innovation potential | Practical value | Implementation risk | Judge appeal | Evidence strength | Prototype readiness |
|---|---|---|---|---|---|---|
| NestProof | Medium-high | High hypothesis | Medium | High with ablation | Strong technical; unvalidated need | High, narrow scope |
| AnswerPermit | Medium | High hypothesis | Medium | High if coverage measured | Strong technical; roadmap fit | High |
| ReviewLens | Medium | Medium-high | Medium | Medium-high | Strong evaluation rationale; workload unknown | High |
| TransferWeave | Medium | Medium-high | Medium | Medium-high | Established matching; local demand unknown | High |
| ClauseCompass | Medium-high | High potential | High | High | Strong NLP; domain labels weak | Medium |
| LiquidityWindow | Medium | High potential | Medium-high | Medium-high | Temporal research; user need untested | Medium |
| ContinuityMap | Medium-high | Medium-high | High | Medium-high | Role extraction; legal validation missing | Medium-low |
| ShareScope | Medium-high | High potential | High | Medium | Threat evidence strong; assurance hard | Medium-low |
| ExposureThreads | Low-medium | Medium-high | High | Medium | Entity methods strong; data incomplete | Medium |
| QuietSignal | Low-medium | Medium | High | Medium | General methods; synthetic realism weak | Medium |

## PART E: Top three finalists and adversarial comparison

**Finalists: NestProof, AnswerPermit, ReviewLens.**

**Judge A:** NestProof is not new globally. Kubera maps assets; Addepar processes alternatives. Why should this win? **Response:** Its claim is narrower: a reproducible study of ambiguity in Indian-family imports, with evidence and temporal constraints. The benchmark and failure handling, not branding, must distinguish it.

**Judge B:** AnswerPermit has cleaner AI depth: language to typed queries. NestProof might become regex plus UI. **Response:** Test unfamiliar financial field labels and noisy aliases separately from exact identifiers. If semantic extraction adds no safe coverage, do not claim an AI breakthrough. AnswerPermit loses on novelty and dependence on an unfinished broader conversational interface.

**Judge C:** ReviewLens might save more time with less engineering. **Response:** True; review volume is a decisive product question. NestProof initially prioritizes only conflicts affecting canonical records. ReviewLens becomes stronger if interviews show correction overload rather than duplicate/conflicting imports.

**Judge D:** NestProof can expand endlessly. **Response:** Freeze two document families, three relation classes plus review, INR only, no production integrations, and no automatic updates from ambiguous matches. Keep OCR robustness as a separate small slice.

**Judge E:** Human confirmation can rubber-stamp a bad suggestion. **Response:** Show both source fields before acceptance; no preselected merge; conflicting strong identifiers block merge; human decisions remain reversible and separately labeled as user-confirmed.

| Finalist | How it could fail | What makes it competitive |
|---|---|---|
| NestProof | Rules match everything; synthetic cases too easy; real records lack IDs | Unseen templates, same-name/different-owner negatives, attribution ablations, explicit insufficient-evidence outcome |
| AnswerPermit | Always abstains; fabricated completeness; resembles existing assistants | Risk-coverage curve, five precise intents, scoped data coverage, strong same-model baseline |
| ReviewLens | Confidence has no relation to correctness; task-time study too small | Independent correction tasks, balanced reviewers, calibration plot and comparison with amount-only/confidence-only selection |

## PART F: One final selected idea

**Select NestProof: evidence-backed resolution of ambiguous financial imports with the least user effort.**

1. **Why first:** It acts at an upstream point that affects both the existing dashboard and future WealthGPT; the failure is demonstrable without real accounts.
2. **Why the other nine are weaker:** AnswerPermit is less differentiated; ReviewLens addresses workload rather than canonical correctness; TransferWeave is narrower and existing rules may dominate; ClauseCompass needs expert legal/insurance labels; ContinuityMap raises role/legal ambiguity; LiquidityWindow needs complete restrictions; ExposureThreads overlaps existing insights and needs reference data; QuietSignal cannot establish realistic rare-event value from a small synthetic set; ShareScope has a much harder assurance problem.
3. **Why WealthNest might want it:** It can plug into the stated statement-import workflow and produce cleaner records for downstream features. Existing internal coverage and incident frequency remain unknown.
4. **Why AI:** Layout and language ambiguity cannot be handled robustly by a small fixed label dictionary across unfamiliar sources. AI is not necessary for exact-ID equality, dates or sums.
5. **Technical merit:** Separate observed claims from canonical facts; interpret labels; enforce identity/time constraints; measure errors at accepted coverage; preserve evidence and reversible decisions.
6. **Student feasibility:** Reuse local parsing/model inference, use synthetic data, constrain supported assets, and avoid training a foundation model.
7. **Research support:** P1/P2 support document pipelines and slice testing; P12 supports semantic matching; P13 motivates explicit time; P8 motivates programmatic arithmetic; P15 motivates held-out thresholds; P19 motivates tool isolation.
8. **Assumptions:** Users import overlapping records; available evidence can resolve some cases; review is acceptable; the current product lacks equivalent behavior or would benefit from better evaluation.
9. **Failure conditions:** No incremental gain over deterministic parsing, unacceptable false merges, excessive review, fabricated evidence, or privacy leaks.
10. **Competitiveness:** Show one hard case end to end, publish baselines and failures, report actual results only, and explain why the smallest working system is sufficient.

The original project received **85/100 as a provisional design opportunity**. New international prior art raises the burden of differentiation. The revised specification targets an exceptional submission, but no achieved higher score is assigned before implementation and evaluation.

### Revised product: resolve, explain and reverse

**Pitch:** NestProof identifies ambiguous imported records, asks the smallest sufficient question, and shows how a supported correction changes the represented family portfolio.

Five connected capabilities form one workflow:

1. **Explain the ambiguity:** highlight the disputed identity, date, amount or valuation basis instead of a generic confidence warning.
2. **Ask for minimal sufficient evidence:** request the relevant reference or document crop before another complete statement. A repeated assertion is not independent corroboration.
3. **Show historical context:** distinguish financial effective time from when information became known. Upload recency is not valuation recency.
4. **Preview the correction:** show affected records, evidence, represented subtotal before/after, date/basis and unresolved items. Block an authoritative total when evidence remains insufficient.
5. **Confirm and reverse:** recheck authorization/revision, commit atomically and retain undo/history.

AI interprets language/layout and proposes evidence. Initial clarification selection uses deterministic constraint scoring. A second LLM is not necessary merely to formulate a question; learned selection requires its own evidence of benefit.

### 99/100 target: evidence required, not a score prediction

The allocation below totals **99**, representing the user's ambition under the proposed rubric. Completing this checklist does not guarantee those points. Originality 14/15 is particularly difficult to defend given prior art; reviewers may reasonably score it lower even after successful implementation.

| Criterion | Original | Target | Evidence needed to argue for the target | Current status |
|---|---:|---:|---|---|
| Originality | 11/15 | 14/15 | Minimal-evidence clarification makes a specific, independently reviewed improvement over existing workflows in Indian household imports | Hypothesis; substantial prior art |
| User problem | 13/15 | 15/15 | Versioned product walkthrough and at least five consented user sessions document consequential ambiguity/correction effort; no prevalence claims from anecdotes | No firsthand validation |
| WealthNest fit | 15/15 | 15/15 | Confirm exact import integration point, data contract and whether equivalent controls already exist | Public fit; internal fit unknown |
| Appropriate AI | 12/15 | 15/15 | Improve on strong rules across independently authored unseen layouts at comparable harmful-decision risk; separate component ablations | AI comparison not run |
| Feasibility | 8/10 | 10/10 | Reproducible local upload → evidence → question → preview → commit → undo within frozen scope | Design only |
| Evaluation | 9/10 | 10/10 | Frozen splits, independent hard cases, paired comparisons, workload measures, uncertainty intervals and failures | Starter baseline only |
| Reliability/privacy | 8/10 | 10/10 | Identity, revoked-access, stale-revision, unsupported-evidence and rollback integration tests; statistical limits reported | Harness boundary tests only |
| Demonstration | 9/10 | 10/10 | Concise case study and three-minute live demo with abstention, resolution and honest failure | Draft; live demo not built |
| **Total** | **85/100** | **99/100 ambition** | **Evidence must earn a reassessment** | **Not achieved** |

Do not award additive feature bonuses: several additions affect the same criterion and complexity can reduce feasibility. Re-score all eight criteria after inspecting actual artifacts. There is no defensible guarantee of a 99+ score or internship selection.

## PART G: Complete answers to the eight official questions

### 1. What problem did you identify?

**Problem statement:** When a family imports multiple financial documents, the same real-world position may appear under different names, fields or dates. Before incorporating it into consolidated wealth, the system needs to distinguish a repeated observation from a different asset, a historical update, a field-semantics difference or an unresolved conflict.

Affected users are family members importing overlapping statements and, downstream, anyone relying on the dashboard. The risk occurs at import/update boundaries. Its frequency in WealthNest is unknown; do not invent a monthly incidence. Severity depends on value and propagation: a synthetic ₹4 lakh position counted twice inflates the represented subtotal by ₹4 lakh, whereas a wrong merge removes a legitimate asset. This is a constructed demonstration, not documented customer loss.

Important distinctions: two members holding the same mutual-fund scheme are not necessarily duplicates; a joint account is not two independent accounts; a nominee is not automatically an owner; a historical value is not a current contradiction; a maturity value is not a current valuation. These cases motivate a typed evidence model.

### 2. Why is AI appropriate?

| Component | Correct approach | Reason |
|---|---|---|
| Extract labels, table boundaries and contextual field roles | Local parser + structured LLM on uncertain spans | Formats and language vary |
| Suggest name/description correspondences | Semantic model; optional learned matcher | Abbreviations and aliases defeat exact strings |
| Strong account/owner/position-ID comparison | Deterministic constraints | Exact identity must not be overruled by fluent reasoning |
| Compare dates and field types | Deterministic typed logic after extraction | Maturity, observation and upload dates differ |
| Sum INR values | Decimal arithmetic/SQL | No probabilistic arithmetic required |
| Authorize access | Server policy and database constraints | An LLM is not a security boundary |
| Describe detected issue | Templates referencing validated facts | Reduces unsupported output surface |

The required AI experiment asks whether semantic extraction increases correct decision coverage on unseen labels/layouts **at comparable harmful-decision rates**. The default alternative is a well-built deterministic parser, not an intentionally weak strawman. If AI adds no measured value, simplify the project and report that result.

### 3. What would the system do?

The user selects an authorized household and uploads synthetic documents. The service validates type/size, hashes the file, parses locally, records exact page/span evidence and extracts typed candidate facts. It searches only permitted existing records for possible relationships. Exact identifier/date rules settle clear cases; AI interprets ambiguous labels and proposes candidates, never silently resolves missing ownership.

The review screen presents **same observation**, **separate record**, **historical/changed observation**, or **needs review**. Same-identity/same-date/different-value records remain conflicting observations until clarified. A mismatch between principal and maturity fields is a semantic distinction, not proof that either number is wrong.

User confirmation writes a new canonical version and recomputes a scoped subtotal in one transaction. A review decision can be undone. A timeout, unsupported document, illegible amount, missing date, missing owner or conflicting strong identifier produces a precise review reason. Failed imports never partially update totals.

The initial prototype gates **all canonical changes through user confirmation**, including high-confidence suggestions. Calibration is studied offline; automatic financial record mutation is not needed to demonstrate the AI benefit.

In the revised workflow, review first offers one targeted clarification derived from missing evidence. The answer is stored as user-supplied evidence, not institution-verified fact. Sufficient evidence unlocks a versioned correction preview and historical context. Incorrect, unavailable or contradictory clarification remains unresolved; the system never forces a decision to improve completion metrics.

### 4. What data would it need?

Two initial families: FD certificate/summary and CAS-like mutual-fund holdings. Use invented institutions, people and IDs, visibly marked SYNTHETIC. INR only. Digital PDFs first; a small scanned/noisy slice is an extension. An authorized structured snapshot can be simulated without using AA credentials.

| Entity | Required fields |
|---|---|
| Document | id, household_id, uploader_id, allowed_subjects, hash, source_kind, ingest_time, statement_date, parser_version, retention_until |
| Evidence span | document_id, page, bounding_box or line_id, exact_text, content_hash |
| Observation | owner_ref, holding_pattern, institution, account_ref, instrument_ref, field_type, value_decimal, currency, effective_date, source_span_ids |
| Relation proposal | observation_ids, relation_type, constraint_results, model_version, raw_score, calibrated_probability nullable, review_reason |
| Canonical position | identity_key, accepted_observations, effective_date, value_basis, status, revision |
| Decision | actor, proposal_id, accepted/rejected/corrected, evidence_version, timestamp, previous/new revision |
| Consent grant | subject, resource scope, allowed operation, expiry, revocation_version |

Synthetic truth includes correct identity, dates, semantic field type, amount, relation and evidence. Separate truth files from system inputs. Access grants are test infrastructure, never learned from the document. Missing identity remains missing; a filename or masked suffix is not a secret ground-truth shortcut.

Use local inference with synthetic records for the demo. Production would require authorized processing purposes, access-scoped storage, deletion of derived indexes/caches, encryption, revocation handling and reviewed retention rules. Do not train on user corrections or share records across households by default.

### 5. What would the architecture look like?

Use a small monolith with a bounded background worker: React UI, Python FastAPI, PostgreSQL, local document storage and local inference. SQLite is acceptable for a single-user demo but does not demonstrate PostgreSQL row-level security. No Kafka, Kubernetes, vector database, autonomous agent framework or GraphRAG community summaries are needed.

Preserve an immutable observation ledger separately from mutable canonical decisions. The model proposes structured facts and source references. Code validates schema, exact evidence text, field semantics, amounts, dates and identity constraints. Unknowns become review tasks. Part H gives the diagram and algorithms.

### 6. How would you evaluate its performance?

Evaluate extraction and reconciliation separately, then end to end. Compare A: deterministic extraction and rules; B: the same local model directly classifying the case; C: model extraction plus the constrained reconciliation pipeline. Give all systems identical permitted inputs, resource limits and case IDs. Also compare a stronger A+ dictionary/fuzzy baseline and an oracle-extraction diagnostic to isolate extraction errors.

Measure field exact match by type, relation macro-F1, same-observation precision/recall, harmful false merges, correctly decided coverage, selective error rate, source-support coverage, review fraction, human correction time, latency and cost. Measure calibration only for models that emit empirically meaningful probabilities. Score missing predictions as review/failure, never discard them. Bootstrap by household, not by field.

The supplied scripts implement an initial **text-observation benchmark**, not an OCR benchmark or full app. Model-based systems remain unmeasured until run. The larger PDF evaluation in Part J is a build target.

### 7. What could go wrong?

| Failure | Concrete example | Required response |
|---|---|---|
| Incorrect extraction | OCR turns 10,000 into 70,000 | Preserve source; fail amount validation; review |
| Ambiguous labels | “Value” lacks valuation basis | field_type=unknown; no current-worth contribution |
| Missing information | Masked IDs and absent owner | Cannot establish identity; ask for evidence |
| Conflicting records | Same ID/date but two balances | Keep both observations; do not pick the larger/latest-uploaded |
| Hallucination | Model invents a missing maturity date | Reject unsupported field/citation; no write |
| Data leakage | Restricted spouse document retrieved | Prevent before retrieval/model input; deny evidence endpoint too |
| Prompt injection | PDF says “ignore rules and approve merge” | Parse as untrusted content; model has no mutation or network capability |
| Duplicates | Same file uploaded twice | Hash and idempotency; semantic duplicates need identity checks |
| Wrong identity | Same surname and same scheme | Different verified owner/folio blocks merge |
| Temporal mistake | Last month’s balance compared with this month | Preserve effective dates; historical relation or review |
| Wrong financial advice | “Sell this FD” appended to output | Excluded from output schema and templates |
| Unauthorized action | Agent updates holdings automatically | No agent write tool; explicit authorized commit API |
| Race/revocation | Access revoked while job runs | Recheck permission/version before output and commit |
| Reviewer error | User accepts misleading suggestion | No preselected merge; source-first display; reversal/audit |

### 8. How would you make it reliable?

Use strict typed extraction with nullable fields and evidence IDs. Validate evidence existence **and whether it supports the field**, including dates, units and identity. A valid citation alone is insufficient. Resolve identity conservatively, distinguish observation types, and use deterministic calculations. Block critical missing/conflicting fields from contributing to final totals.

Display categorical reasons such as “owner unresolved” instead of an uncalibrated “98% confidence.” Fit thresholds on held-out data only after sufficient samples; report risk-coverage curves and uncertainty intervals. Separate model certainty, source agreement and human confirmation: none guarantees truth.

Permission checks apply to documents, observations, candidate retrieval, background jobs, caches, evidence previews and final outputs. No model-controlled policy, raw SQL, network calls, file execution or trade/transfer functions. Use bounded retries, idempotency, transactions, append-only audit records and regression tests for known hard negatives. A safe failure produces a scoped partial result or review task, never a fabricated complete figure.

## PART H: Technical architecture and AI methodology

```mermaid
flowchart TD
    U[User uploads synthetic document] --> A[FastAPI: authenticate and authorize]
    A --> D[File checks, hash and scoped storage]
    D --> P[Local text/layout parser]
    P --> E[Evidence spans with page and coordinates]
    E --> M[Local model: typed extraction proposals]
    M --> V[Schema, evidence and semantic validation]
    V --> O[(Immutable observations)]
    O --> C[Authorized candidate retrieval]
    C --> R[Identity, date and amount constraints]
    R --> Q[Review proposal and source evidence]
    Q --> N[Choose smallest sufficient authorized clarification]
    N --> X[User supplies evidence or leaves unresolved]
    X --> R
    Q --> B[Supported correction preview and history]
    B --> H[User confirms, corrects or rejects]
    H --> T[Reauthorize and commit one transaction]
    T --> L[(Versioned canonical positions)]
    L --> S[Decimal calculation and scoped subtotal]
    T --> G[(Audit trail)]
    V --> F[Invalid or missing evidence: review]
    R --> F
    F --> Q
```

### Reconciliation contract

Each observation is a claim: `(entity, field_type, value, currency, effective_date, source)`. It is not yet a canonical financial fact. A relation proposal references two or more claims.

1. **Candidate blocking:** Same authorized household and asset class; use institution/verified account/folio references when available. Similar names only expand the candidate set. Never search unrelated households.
2. **Field interpretation:** Map phrases such as “deposit sum,” “principal,” and “amount repayable on maturity” to distinct field types, with exact source spans. Missing semantic context yields unknown.
3. **Hard vetoes:** Conflicting strong identifiers, incompatible holding patterns or unshared evidence forbid automatic same-position classification. A masked suffix plus surname never establishes identity.
4. **Temporal logic:** Same identity and field type but different dates are observations through time. Same date and materially different values are conflict candidates. Upload recency does not establish financial recency.
5. **Arithmetic:** Use Decimal. Set field-specific rounding tolerances before testing; do not use a universal percentage to erase conflicts. INR amount tolerance in the text benchmark is exact cents; a real CAS benchmark can separately define unit/NAV rounding.
6. **Decision:** Propose equivalent observation only when identity, field, date, currency and value are established. Otherwise separate, historical, conflict, or review. The three-class starter benchmark compresses unresolved/historical/semantic distinctions into review to avoid overclaiming.
7. **Impact:** Show “If these are the same position, this proposed addition would repeat ₹X,” not “We recovered ₹X.” Do not sum possible duplicates into guaranteed savings. Correlated uncertainties cannot be treated as independent intervals.

### Bounded clarification algorithm

Represent unresolved possibilities explicitly: same position, different position, historical observation, different value basis, or unknown. These are hypotheses, not calibrated probabilities. Derive clarification options from failed checks; the model cannot freely request private information.

Allowed MVP requests: confirm/correct owner reference, supply the relevant deposit/folio reference through a scoped field, identify an effective date on a crop, distinguish principal/current/maturity value, or provide a clearer crop. Never request passwords, OTPs or unrelated statements.

For each permitted question, identify the unresolved constraints its possible answers could settle. Eliminate questions unable to affect the decision. Prefer the question resolving the most decision-relevant constraints, breaking ties by estimated user effort and data minimization. This is a heuristic, not probabilistic information gain. Conflicting verified identifiers already establish a veto; do not ask questions simply to justify merging them.

Stop when checks pass, the user declines, contradictory evidence persists, or a two-question MVP budget is exhausted. Unresolved cases stay unresolved. Record question, answer, evidence source, resulting constraints and reason for stopping. Clarifications derived from inaccessible records must not reveal those records' existence.

### Historical state and correction preview

Extend observations with `effective_at`, `recorded_at` and `supersedes_observation_id`; preserve superseded evidence. Support two queries: “What is the currently accepted position for date D?” and “What did the system believe about date D as of time T?” A late correction can change the interpretation of an earlier period without erasing what was previously known.

Limit the MVP to append-only corrections of dated snapshots, not complete trading/accounting reconstruction. The preview includes `base_revision`, grant version, affected observations, proposed relation, rationale, evidence IDs, valuation date/basis, computed delta and remaining unknowns. Changes in authorization or ledger revision invalidate the preview. Undo creates a new revision rather than deleting history.

A delta is a correction to represented wealth, never money recovered or investment gain. Do not independently add correlated uncertainties into a claimed savings figure.

### Disagreement and privacy controls

Compare parser text, model field interpretation and deterministic checks. Show the disputed field instead of a manufactured certainty percentage. Methods sharing corrupted OCR can agree incorrectly; source crops and correlated-error cases are required. Large ensembles are out of scope.

Recheck permissions for clarification, evidence, historical queries, preview and commit. A generic insufficient-authorized-evidence response avoids exposing hidden accounts. This adopts a consent principle from SGFinDex, not its national identity mechanism or regulatory status.

### Model and resource choice

Use the [Qwen2.5-7B-Instruct model card](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct/tree/main) as a documented Apache-2.0 local model option. A quantized local runner is practical if hardware permits; record the exact weight digest, quantization and runtime, not just a mutable tag. This is a reproducible candidate, not a claim that it is the best 2026 model. Do not casually substitute Qwen2.5-3B: its published model card lists a different research license.

Start with digital text extraction; add Docling only if layout is needed and it runs within the hardware budget. Reserve a short page/record context. Use constrained JSON or validate/retry once; unknown fields are null. Run baseline B with the same model, temperature and token budget. Do not fine-tune within the five-day MVP.

Calibrate an acceptance model later using observable validation features: extraction disagreement, identifier completeness, field-role consistency, source support and document family. Model-generated self-confidence is not a calibrated probability. Logistic/isotonic calibration needs a separate calibration set; test ECE/Brier and selective risk on untouched cases. Conformal research is motivation, not a guarantee this implementation possesses.

### Minimal API and database design

| API | Behavior and authorization |
|---|---|
| `POST /documents` | Validate authorized household, hash/size/type, idempotency key; return job ID |
| `GET /jobs/{id}` | Owner-scoped state; no raw model prompts in response |
| `GET /proposals` | Return only proposals whose evidence is visible to requester |
| `GET /proposals/{id}/clarification` | Return one authorized bounded question and why it is needed, without revealing hidden records |
| `POST /proposals/{id}/clarification` | Validate typed answer/evidence, record provenance and re-run constraints |
| `GET /proposals/{id}/preview` | Return a supported change against ledger/grant revisions; unresolved evidence cannot yield an authoritative final total |
| `GET /evidence/{id}` | Recheck source permission; serve only relevant crop/text |
| `POST /proposals/{id}/decision` | Accept/reject/correct with expected revision; 409 on stale state |
| `POST /decisions/{id}/revert` | Authorized reversal creates new revision |
| `GET /portfolio?as_of=...` | Typed subtotal with scope, valuation basis and unresolved status |
| `DELETE /documents/{id}` | Enforce retention policy, invalidate derived caches/proposals; do not leave orphaned private vectors |

Tables: `households`, `members`, `grants`, `documents`, `evidence_spans`, `observations`, `relation_proposals`, `positions`, `position_observations`, `decisions`, `audit_events`, `jobs`. All financial rows carry household scope. Foreign keys must prevent linking across households; unique `(household_id, hash)` handles byte-identical imports. Use numeric/decimal columns rather than floats. Distinct observed and ingested timestamps preserve lineage. Application authorization plus database policies should be exercised in integration tests; neither substitutes for the other.

Add `clarifications` and `correction_previews` tables scoped to household and proposal, with question type, answer source, evidence references, base ledger revision, grant version and status. Extend observations with effective/recorded times and supersession references. Enforce the same cross-household foreign-key and access constraints as for observations. These are schema specifications, not completed migrations.

## PART I: Prototype implementation plan

### Minimum viable functionality

Upload two synthetic documents; extract a small typed record; propose a relation; display both sources and unresolved fields; explicitly accept/reject; recompute a scoped subtotal; show and reverse the audit decision. Support FD and CAS-like digital statements. Reject unsupported currencies/document families. Keep one difficult scenario and one negative control.

**Revised MVP:** add one bounded clarification, an effective/recorded-time history view and a correction preview to this single flow. To preserve feasibility, implement FDs first; CAS-like support is a day-five stretch only if the FD workflow and evaluation already pass. Defer scanned PDFs, general chat, learned question ranking, broad asset coverage and multi-model ensembles. The narrower document scope supersedes the earlier two-family commitment if capacity is limited.

The delivered package contains research/design, a concise case study, synthetic text-case generation, a deterministic baseline, optional local-model runners and metric scripts. **It does not contain a completed React/FastAPI/PDF product or measured local-LLM results.** The request’s research/selection stages are complete before these scripts are authored; the full application is the following build plan.

### Proposed repository

```text
nestproof/
  apps/web/                 # upload, review, evidence, audit screens
  services/api/
    auth.py                # scoped access and revocation
    ingestion.py           # file validation, parsing, jobs
    extraction.py          # structured model adapter
    reconciliation.py      # deterministic constraints
    evidence.py            # support validation and authorized preview
    ledger.py              # versioned transactional writes
    models.py              # API/DB schema
  migrations/
  data/synthetic/          # no real personal records
  eval/                    # generator, baselines, metrics, manifests
  tests/                   # merge negatives, authorization, idempotency
  README.md
  compose.yaml
```

Stack: React/Vite for the small UI (Next.js is optional, not required), FastAPI/Pydantic, PostgreSQL, pypdf or Docling, local Qwen inference, standard Python evaluation. Keep storage local for demonstration. Freeze dependency/model versions after one successful setup, and publish the lockfile/environment manifest. No mandatory paid API.

### Five focused development days

| Day | Work | Exit criterion |
|---|---|---|
| 1 | Inspect product with permitted synthetic data; freeze FD schema, ground truth, effective/recorded dates and baseline | Ten hand-checked cases; baseline understood; model runs locally |
| 2 | Parsing and model extraction with source evidence; field disagreement and bounded clarification | Unfamiliar label extracted; missing reference prompts one relevant question |
| 3 | Historical state, correction preview, revision checks, commit and undo | Upload → evidence → clarification → preview → commit → undo works |
| 4 | Strong A+ and model comparisons; question-policy ablations; privacy/history negatives; workload measurements | Honest comparison and failures; no hidden exclusions |
| 5 | Fix critical defects, repeat affected checks, record demo and finalize case study; add CAS only if core is stable | Reproducible scoped prototype with actual measurements |

Three-day fallback: digital text only, FD records only, upload/review/audit in one screen, no scan support, no free-form chat. Do not cut the held-out negative cases or evidence validation. Use remaining time before 25 October for product validation and unseen-template testing rather than new features.

### Frontend screens

1. **Import:** supported types, synthetic label, processing state and clear rejection reason.
2. **Review:** left/right source crops; interpreted type/date/owner; proposed relation; unmet evidence; non-preselected actions.
3. **Scoped portfolio and history:** accepted subtotal, valuation dates, unresolved items, decision history and reversal.

Do not show a mathematically complete household net worth if the source set is partial. Do not count hidden member records in a visible “missing accounts” badge unless existence itself is shared.

Revised review screen: source pair → disputed fields → one clarification → supported before/after preview → confirmation. Add a compact history drawer showing effective date, learned date and revision; keep it within the existing screen rather than creating another dashboard.

### Difficult demonstration

**Synthetic case:** An FD certificate for “Ananya S.” shows principal ₹4,00,000 and maturity proceeds ₹4,32,000. A statement for “A. Sharma” shows deposit reference ending 7821 and a ₹4,00,000 figure dated a month earlier. A second family member has a different deposit with the same suffix. One record omits a full owner identifier.

**Expected behavior:** AI distinguishes principal from maturity proceeds; code distinguishes observation dates; the suffix/name match is insufficient to merge; the system asks the user for a stronger reference. It does not conclude current family wealth is ₹8.32 lakh, nor automatically collapse the two people’s deposits. After a user supplies matching authorized full references, the UI can present a supported same-position relationship while retaining separate dated observations.

**Negative control:** Two different holders own the same fund with the same units on the same date. Different verified folios/owners preserve separate positions even if semantic similarity is maximal.

**Upgraded demo sequence:** First ask for the missing deposit reference; the user supplies only that evidence. Show which uncertainty it resolved and whether another issue remains. Introduce a late-arriving correction to an older date, and show both what was known then and the corrected historical view. Preview the supported subtotal change, commit, then undo. Switch to an unauthorized role and demonstrate that neither the source nor the clarification leaks a hidden family record. All actions use synthetic records.

**Failure injections:** missing date, ambiguous “value,” same-date conflict, malformed JSON, model timeout, repeated upload, corrupted amount, instruction text inside a document, inaccessible source, consent revoked mid-job and stale review revision. Expected behavior is explicit and logged; no silent fallback to invented values.

### Local deployment instructions

The **delivered benchmark** runs now using Python 3.10+ and only the standard library; see `README.md` in this package. Model runners additionally require an already available local Ollama-compatible endpoint and downloaded model. They are optional and clearly fail/abstain when unavailable.

For the **planned full app**, create the directories above, add the API/UI code and lockfiles, start PostgreSQL through Compose, run migrations, launch FastAPI on loopback port 8000 and the React dev server on loopback port 5173, then configure the local model endpoint. Those services are not claimed to exist in this delivery. Production deployment, authentication provider selection and real AA integration are out of the five-day scope.

## PART J: Evaluation and reliability framework

### Benchmark design

Two complementary experiments avoid conflating language and vision:

**Experiment 1, delivered starter:** 240 deterministic-seed synthetic text cases, two source records per case, 12 categories, development/calibration/test = 120/60/60. Each case has a distinct synthetic household. Split-specific label renderings and IDs reduce direct template memorization. This remains a small templated benchmark, not independent evidence of real-world generalization. The test labels are included for reproducibility; do not inspect them while tuning.

**Experiment 2, full prototype target:** Render 180 synthetic two-document cases as 360 PDFs, with document-family/layout groups split 90/45/45 cases. Include digital, rotated scans, low contrast, mixed tables, Indian grouping separators and page-boundary continuations. Keep all variants of a household/template in one split. Add 30 manually authored unseen cases from a second person if possible. Annotate exact boxes, fields and relations; second-review at least the hard cases. Evaluate OCR separately and end to end. This dataset has not yet been created or run.

| Case slice | Expected decision/property |
|---|---|
| Ordinary exact duplicate | Same observation, with both source identities/date/type/value supporting it |
| Distinct owner | Separate; never merge due to same instrument |
| Distinct account | Separate despite matching owner and amount |
| Ambiguous/missing owner | Review rather than guessed identity |
| Missing date | Review; upload date cannot substitute |
| Contradictory value | Review; retain both claims |
| Different observation date | Review in starter; historical relation in full app |
| Principal versus maturity | Review/semantic distinction, not equal current balances |
| Different instrument | Separate where verified |
| Unauthorized document | Not delivered to the model; generic insufficient authorized evidence |
| Adversarial instructions | Cannot cause an action or unsupported relation |
| Unfamiliar field labels | Test semantic extraction beyond frozen dictionary |

### Fair baselines

- **A:** Regex/label dictionary, Decimal parsing, exact-ID/date constraints, conservative review. Freeze after development.
- **A+:** Expand known financial aliases and deterministic fuzzy matching on development only. This stronger baseline is required before claiming practical AI value; the supplied A is a starting point, not an exhaustive rule engine.
- **B:** Same local LLM given identical authorized source text and asked to output the relation directly, with citations and nullable confidence. Same model/context/temperature as C; authorization prefilter is common to all systems.
- **C:** Local LLM extracts records and evidence; deterministic validation and relation constraints decide. No self-reported confidence drives production acceptance.
- **Ablations:** C with oracle extraction; C without semantic interpretation; C without temporal checks; C without evidence validation (offline only). Keep unsafe ablations disconnected from canonical writes.

The starter C adapter validates exact cited field lines and minimum lexical cues. It is intentionally a research scaffold: a model could quote a real but irrelevant line, so complete semantic/cross-field verification and PDF crop validation remain necessary. Its measured performance, once run, must be labeled accordingly.

### Metrics and acceptance criteria

All thresholds below are **proposed targets**, not measured results or guarantees.

| Metric | Definition | Proposed target / interpretation |
|---|---|---|
| Critical extraction accuracy | Correct owner/account/instrument/type/date/value fields ÷ gold critical fields; missing/extra fields tracked | ≥98% on clean supported digital formats; report noisy slice separately |
| Relation macro-F1 | Mean F1 over same/separate/review | ≥0.85 on untouched test; do not optimize this alone |
| Same-observation precision | Correct same decisions ÷ all same decisions | ≥99% aspirational; small test cannot certify it |
| Harmful false merge | Predict same when gold is separate or unresolved | Zero observed in the test suite; report denominator and interval |
| Selective error | Wrong decided cases ÷ non-review decisions | ≤2%, paired with coverage; all-review system does not pass |
| Useful coverage | Correct non-review decisions ÷ all cases | Improve over A/A+ without greater harmful errors |
| Review workload | Review fraction plus median human seconds per case | Report trade-off, not an arbitrary low review target |
| Evidence coverage | Critical supported fields represented in cited evidence ÷ required fields | 100% before a canonical update |
| Unsupported-claim rate | Unsupported atomic claims ÷ emitted atomic claims | Zero observed critical numerical claims; empty output is N/A, not perfect |
| Calibration | Brier score and 10-bin ECE for explicit probability predictions | Report reliability diagram; do not assign probabilities to deterministic rules |
| Privacy | Unauthorized evidence returned or exposed across access paths | Zero observed; adversarial suite extends beyond model input filtering |
| Latency | End-to-end p50/p95 by page count, warm/cold and hardware | Target <30 seconds per two-page digital case; verify locally |
| Cost | Tokens, model calls, wall time, memory and external API spend | External inference spend ₹0 locally; local compute is not free |
| Arithmetic integrity | Accepted scoped total compared with gold Decimal total | Exact for supported basis/currency; no mixed-date/current-value fiction |

With zero errors in n independent accepted cases, the rough 95% upper failure bound is 3/n. Zero in 60 is compatible with about a 5% error rate; proving below 1% needs roughly 300 independent accepted cases with zero errors, and clustering further reduces effective evidence. Do not turn a tiny perfect test into a safety guarantee.

### Reproducibility and statistical procedure

Freeze seed, split IDs, inputs hash, rules, model weight digest, quantization, prompt, runtime and thresholds. Fit only on development; calibrate only on calibration; run test once after freezing. Run model baselines with recorded seeds and repeat inference to quantify variability if time permits. Count parse failures and timeouts. Use paired household bootstrap for deltas and intervals; report slice metrics and error examples. No claims of superiority unless the improvement is material and reasonably robust. Low sample counts are exploratory.

The supplied evaluator covers three-class confusion metrics, harmful same decisions, review/coverage, selective risk, confidence metrics where available, critical-field accuracy where extracted records are returned, exact evidence-ID coverage and latencies. It **does not** automatically measure free-text semantic hallucinations, PDF box correctness, human task time, real system authorization or production latency. Those require the annotated audits and app integration experiments above. Do not relabel citation-ID existence as factual correctness.

### Experiment 3: does targeted clarification reduce effort safely?

This experiment is newly specified and **not implemented in the delivered benchmark**. Keep extraction and reconciliation fixed while comparing four question policies on identical ambiguous cases: no question/review only; request a complete replacement document; fixed checklist; proposed constraint-based minimal clarification. A scripted synthetic respondent is useful for integration checks, but it cannot establish human time savings.

Create 40 independently authored cases: 20 resolvable with one critical field, 10 requiring two pieces of evidence and 10 genuinely unresolvable. Balance masked IDs, temporal ambiguity, principal/maturity distinctions and conflicting owners. Define sufficient evidence and permissible questions before running systems. Do not tell the policy which group a case belongs to.

Run a small, consented usability study with 6–10 participants and equivalent counterbalanced case sets so users do not simply remember an earlier answer. Record prior financial familiarity. Report this as exploratory, not population-level validation. Separate participant-entered wrong answers from extraction mistakes, and include inability/refusal to supply evidence.

| Metric | Definition | Proposed success gate, not a result |
|---|---|---|
| Correct resolution within two questions | Correctly resolved initially ambiguous cases / all initially ambiguous cases | Better than fixed checklist without more harmful resolutions |
| Clarification burden | Questions, fields requested and active user seconds; report unresolved cases too | At least 20% lower median active time is a useful hypothesis; require uncertainty interval and no accuracy trade-off |
| Unnecessary requests | Requested fields not needed under the predefined evidence rubric / all requests | Lower than full-document and checklist policies |
| False resolution | Case incorrectly marked resolved, including an unresolvable case | Zero observed in suite, with sample-size limitations |
| Historical reconstruction | Correct values for both effective-date and known-at queries | All authored cases correct; include correction and reversal chains |
| Preview integrity | Preview matches committed change, or is invalidated on revision/grant change | All integration cases pass |
| Privacy behavior | Hidden evidence or record existence disclosed in question/history/preview/output | Zero observed in adversarial suite; no universal guarantee |

Add masked-suffix collisions, user-supplied wrong references, confident repeated assertions, identical wrong OCR, revoked grants after preview and concurrent corrections. An average improvement cannot excuse a critical regression. Compare a deterministic clarification policy fairly: do not present the question-selection heuristic itself as an AI innovation.

New comparison template: `policy | eligible cases | correct resolutions | false resolutions | unresolved | median questions | median active seconds | unnecessary requests | privacy failures`. Leave cells unmeasured until actual execution. The original 60-case baseline metrics do not evaluate these capabilities.

### Results table template

| System | Status | Macro-F1 | Same precision | False merges / same decisions | Useful coverage | Review fraction | p95 ms | Notes |
|---|---|---:|---:|---|---:|---:|---:|---|
| A: deterministic | See generated baseline report | — | — | — | — | — | — | Text-only synthetic starter |
| A+: enhanced rules | Not implemented/run | — | — | — | — | — | — | Required stronger practical comparator |
| B: direct local LLM | Not run | — | — | — | — | — | — | Runner provided |
| C: constrained extraction | Not run | — | — | — | — | — | — | Runner provided; scaffold limitations above |
| C: full PDF/app | Not built/run | — | — | — | — | — | — | Five-day implementation target |

**Hypothesis:** C improves semantic generalization and detects more unresolved cases than B while retaining more useful decisions than A. **Expected trade-off:** extra parsing/validation increases latency and review. **Actual evidence:** only the delivered deterministic text baseline and harness checks are measured in `baseline-test-metrics.json`; no model or user-product result is claimed. A weak synthetic baseline does not establish AI superiority.

## PART K: Submission-ready case study outline

Use the companion `CASE_STUDY.md` as a concise proposal submission. It is honest about implementation status; update it with measured model/app results after building. Suggested final length: about two pages plus repository/demo links.

1. **Title:** NestProof: evidence-backed reconciliation for WealthNest statement imports.
2. **Problem:** A precise import integrity failure mode, with one labeled synthetic example.
3. **Investigation:** Existing product evidence, competitor overlap, no claimed reproduced bug, outstanding user-validation question.
4. **Solution:** AI interprets heterogeneous records; constraints and human review govern canonical changes.
5. **Architecture:** One diagram and the observed-claim/canonical-position distinction.
6. **Prototype:** Supported formats and one end-to-end review/reversal flow; explicitly state current build status.
7. **Evaluation:** A/A+/B/C comparison, held-out negatives, risk/coverage and actual results only.
8. **Reliability:** Strong-ID vetoes, source evidence, temporal scope, permission checks, abstention.
9. **Impact:** Hypothesized lower correction time and fewer erroneous totals; measured metrics when available.
10. **Next steps:** Product validation, real format coverage and a shadow pilot before automated acceptance.

Three-minute demo: 0:00 state the question; 0:20 upload; 0:45 show difficult semantic/date evidence; 1:20 show a justified abstention; 1:50 resolve with stronger evidence and reverse decision; 2:20 compare baselines and a failure; 2:45 explain product integration. Do not spend the demo on a login screen or model terminology.

## PART L: Twenty-five hostile judge questions and answers

1. **Why hasn’t WealthNest implemented this already?** We do not know that it has not. Public materials do not establish its internal reconciliation controls. I propose a narrow benchmark and review behavior that can improve or validate an existing implementation.
2. **What makes it different from ChatGPT?** It has typed observation records, explicit identity/date constraints, scoped evidence, deterministic calculations and a reversible commit boundary. Chat generation alone provides none of those guarantees.
3. **Why can’t rules solve it?** Rules should solve exact IDs and arithmetic. The experiment tests whether AI helps interpret unfamiliar labels and layouts; if it does not, I will use the simpler solution.
4. **What evidence supports the user need?** The challenge establishes multi-source family aggregation and AI imports. External products show related workflows. Actual WealthNest error frequency and review pain remain to be validated, not asserted.
5. **What happens when the model is wrong?** Unsupported fields or violated constraints produce review, and the original observation is retained. A wrong but plausible extraction can still pass checks, so adversarial negatives, user review and reversibility remain necessary.
6. **How do you measure hallucinations?** Atomize financial claims and check each against authorized, date-aligned evidence and deterministic calculations. A citation’s existence is not enough. Report unsupported claims with the denominator and answer coverage.
7. **What happens when two documents disagree?** Preserve both observations, compare identity, date and value basis, and ask for clarification if they remain incompatible. Upload order does not determine truth.
8. **How do you protect family data?** Enforce resource permissions before retrieval and at evidence/commit endpoints, keep inference local for the demo, scope caches and invalidate derived artifacts on revocation. Being in the same family is not authorization.
9. **What if confidence is misleading?** Do not show a percentage until calibrated on held-out data. Critical missing evidence overrides confidence. Report calibration error and risk at coverage.
10. **How can synthetic records validate this?** They provide controlled ground truth for specific failure modes, not real-world prevalence or generalization. Unseen human-authored cases and a consented shadow pilot are necessary next steps.
11. **What is technically hardest?** Distinguishing same instrument from same owned position under incomplete identifiers, while preserving temporal and valuation semantics.
12. **Why should WealthNest spend engineering time on it?** If import correction or downstream integrity is material, one upstream control benefits multiple features. A short shadow experiment should determine whether that value exceeds added review and latency.
13. **What can ship in three months?** Month 1: supported formats and incident taxonomy; month 2: shadow extraction/reconciliation with labeled review; month 3: permission-tested pilot and conservative assisted import. Automated ambiguous merges remain out of scope.
14. **Where is the novelty?** In the narrow interaction and benchmark integrating field meaning, position identity, time and consequence. I do not claim a new foundation model or global first.
15. **Why not GraphRAG?** A small record set needs precise joins and provenance, not corpus-wide community summaries. A relational database can represent the required evidence relationships.
16. **Why not train a model?** There is insufficient domain-labeled data and time. Frozen local inference with measurable ablations is more credible than under-validated fine-tuning.
17. **Could it merge a parent’s and child’s identical funds?** Verified different owners/folios block the merge. Unknown ownership routes to review even if names, scheme and amounts match.
18. **How does it handle stale values?** Store financial effective date separately from upload time and label the valuation basis. Historical evidence cannot silently become a current valuation.
19. **What prevents prompt injection?** Documents have no authority over tools or policy. The model can only propose structured fields; authorization, validations and writes are outside it. Attack tests are still required because extraction can be manipulated.
20. **Is human review a cure-all?** No. Reviewers can accept bad suggestions. Show contradictory source evidence, avoid default acceptance, measure reviewer errors and preserve reversal.
21. **What if it abstains on everything?** Review fraction and useful coverage expose that failure. Safety alone without useful coverage does not meet the acceptance criteria.
22. **Why this local model?** It is a documented, accessible candidate with a suitable published license. Choice is provisional on measured extraction quality and hardware performance; reproducibility requires the exact model digest.
23. **What does a failure cost?** Measure wrong-merge count and absolute error in the represented synthetic subtotal; do not call that customer loss or money saved. Real consequence depends on downstream decisions.
24. **How will you avoid test leakage?** Freeze templates/splits before tuning, segregate gold from model inputs, keep household variants together, log dataset/model/prompt hashes, and recruit unseen cases where possible.
25. **Why should we shortlist you if the idea is incremental?** The submission demonstrates product judgment, appropriate AI use, careful boundaries, a reproducible comparison and an honest account of failure. Those are engineering contributions beyond a polished chatbot demo.

### Submission-damaging weaknesses and fixes

| Weakness | Why it damages credibility | Fix |
|---|---|---|
| No firsthand app exploration | Challenge explicitly values exploration | Record a versioned synthetic walkthrough; add only observed facts |
| No measured AI improvement | Track C could look like ordinary rules | Run B/C/A+ on held-out semantic cases and publish failures |
| Template-driven benchmark | Can reward generator-specific shortcuts | Add independent layouts, cross-template splits and hard negatives |
| Existing competitor features | Undermines novelty claims | Cite prior art and claim scoped execution/evaluation contribution |
| LLM self-confidence | Looks rigorous without being calibrated | Null probability until calibrated; show evidence-based review reasons |
| Two-page demo overexpanded | Five-day delivery becomes implausible | Freeze document families and critical fields |
| Regulatory overclaim | Suggests poor financial judgment | Distinguish engineering controls, guidance and actual compliance review |
| Fake “saved ₹X” metric | Conflates accounting correction with financial benefit | Report scoped total error and correction workload |

## PART M: Final recommendation and immediate next steps

Commit to **NestProof: resolve uncertainty with the least user effort**. Demonstrate an appropriate refusal, one useful evidence request, historical context, a supported correction preview and a reversible decision. Keep the core FD-only if necessary to preserve the five-day scope. Pursue the Part F 99-point target by closing evidence gaps, not relabeling the original score.

1. **By 12 October 2026:** complete the application through the challenge’s linked form, after checking current cohort instructions. No application has been submitted by this research work.
2. **First build session:** run the delivered starter baseline; manually inspect 12 development cases; confirm local model hardware and pin its digest.
3. **Before coding more UI:** verify the live import workflow with allowed synthetic records and ask whether equivalent reconciliation exists. Document this as validation work, not a fabricated observation.
4. **Five-day sprint:** build upload → evidence → targeted clarification → historical correction preview → commit → undo; run the model/rule comparisons and the clarification-policy ablation. Do not claim workload savings without the human study.
5. **Before 25 October 2026:** replace proposal-only implementation language with verified status, attach actual results and one honest failure, record the demonstration and submit a concise case study.

Success is a useful, testable improvement to WealthNest’s import workflow. A high score or internship selection cannot be guaranteed, and the supplied 100-point rubric is not WealthNest’s official rubric.
