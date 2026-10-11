# Independent evaluation and participant study pack

**Status: tooling prepared; no external assessor or participant results collected.** This pack cannot raise an accuracy or impact claim by itself. Use only fictional synthetic records for the initial study. Keep raw materials and participant records local, outside tracked files.

## Document evaluation protocol

1. Choose an assessor who did not implement or tune NestProof. Record their role using an alias; do not imply independence merely because this runner exists.
2. Freeze the code before the assessor creates or reveals final cases:
   ```sh
   mkdir -p .runtime/validation
   python -m evaluation.external freeze --out .runtime/validation/build-freeze.json
   ```
3. Ask the assessor to create 30–50 document pairs with varied wording/layouts. This is an exploratory sample, not safety certification. Include same deposit, different identity, earlier/later date, principal conflict, maturity conflict, missing identity, missing principal, unsupported currency, scans/unreadable content and contradictory fields. Avoid copying the developer's fixture generator for every layout.
4. Independently label each pair before running the system. Have a second person resolve ambiguous gold labels where possible. Include `facts` annotations for both documents. Use null when a field cannot be established; omit only fields deliberately not evaluated. Mark unreadable/unsupported files `unsupported`; reviewable missing evidence is `review`, not a successful extraction.
5. Save the manifest and source files together in `.runtime/validation/assessor/`. Example schema: `validation/manifest.example.json`. Replace the nonexistent example filenames with the assessor's actual files. Do not change labels to match model output.
6. Run:
   ```sh
   python -m evaluation.external run --manifest .runtime/validation/assessor/manifest.json --freeze .runtime/validation/build-freeze.json --out .runtime/validation/report-01.json
   ```
7. Publish aggregate metrics with denominators, failure IDs/types and methodology after reviewing for privacy. The report avoids source text and amounts, but still contains case IDs, authorship metadata and content hashes; review those before sharing.
8. Any engine or frontend change invalidates the freeze. Retain the first results, create a new freeze and use a separate untouched set for a final evaluation. Rerunning inspected cases is regression testing.

The runner compares exact, calibrated fuzzy and ML under the same domain rules. It reports relation correctness, false same decisions, accepted-same precision, review/blocked counts, parser failures and annotated field accuracy. Failures remain in the denominator. It refuses overwrite of result files and checks code plus key parser/model package versions. A fingerprint is not tamper-proof registration or evidence of assessor independence.

## Gold label guide

- `same`: same identity/date/principal; no known contradictory maturity details.
- `separate`: complete critical fields and a different holder, institution or deposit reference.
- `historical` / `update`: same identity, earlier / later effective statement date.
- `conflict`: same identity/date but principal or known maturity details disagree.
- `review`: missing critical evidence prevents a supported decision.
- `blocked`: incompatible values within a source, inconsistent maturity/principal, or quarantined instruction-like text under the documented prototype policy.
- `unsupported`: file cannot be parsed, including scans without text. This label must reflect expected parser refusal, not hide ordinary extraction errors.

Do not infer principal from maturity proceeds. Use ISO dates, canonical reference spelling and INR amounts as decimal strings for facts. Include difficult cases that may break the policy; record disagreements in a separate adjudication note instead of forcing gold to agree with implementation.

## Participant study

Recruit 5–8 consenting adults for an exploratory usability study. Use aliases P01–P08, fictional records and no real account information. Do not recruit under pressure or collect unnecessary identity details. Participation can stop at any time; agree locally when session notes will be deleted. Do not record audio/video without separate consent.

Give each participant a practice task that is excluded from results. Then use two equivalent but different task sets A/B with four cases each: new asset, duplicate with a missing reference, same-date conflicting amount and genuinely unresolved evidence. Supply an authoritative fictional reference sheet for any question that can be answered. Have an assessor define correct outcomes before sessions.

Counterbalance: P01/P03/P05/P07 use manual A then NestProof B; P02/P04/P06/P08 use NestProof A then manual B. Give both conditions the same source information, calculator availability and acceptance policy. Avoid repeating the identical case in both conditions. Explain that rejecting or leaving a case unresolved can be correct.

**Participant instructions:** “Review these fictional documents and decide how the ledger should change. You may add a deposit, link evidence, select an observation after checking the source, or leave it unresolved. Explain what evidence you used. We are testing the workflow, not your financial expertise.”

**Manual condition:** use a blank worksheet listing initial holdings, source facts, proposed action and final principal. **NestProof condition:** use an isolated fresh synthetic database per session and the same task data. Do not silently help one condition more than the other. Record facilitator help.

Measure elapsed task time, final correctness, wrong acceptance, unresolved outcome, clarification count and help. Time incorrect and abandoned attempts too. Set an equal disclosed time cap (for example six minutes per task) before starting. Record timeouts; do not silently drop them or count them as correct. Review correctness against the prewritten answer key, preferably by someone other than the facilitator.

Use `session-record.example.json` as a blank per-participant record. Keep completed files in `.runtime/validation/study/`. Replace null only with observed values; never fill missing results using an agent simulation.

## Reporting template

- Dates, participant count, recruitment and consent procedure; number of completed/abandoned tasks.
- Frozen build identifier; task allocation and counterbalancing; synthetic dataset authorship.
- Correct decisions / all assigned tasks for each condition; wrong accepted decisions and unresolved cases separately.
- Per-participant paired time differences, with incorrect attempts and timeout policy explicitly handled. Report raw anonymized rows and medians; avoid a universal percentage claim from 5–8 people.
- Facilitator interventions, learning effects and task equivalence limitations.
- What failed, what was changed, and which findings were retested on new material.
- Do not combine simulation question counts with human observations or call convenience participants representative customers.

## Next integration evidence

With permission, observe WealthNest's actual import review or ask its team to assess this boundary. Record what exists already, where uncertainty appears, and whether this proposal removes work. A reply or interview is not endorsement; quote only with permission. No product-fit validation is claimed until it happens.
