# Project statement · Brief A · Group 6

Written in Scope, before the data is opened. Updated when the data proves a line wrong, with the old line struck through rather than deleted, so the panel can see what you learned.

## 1. Dr Menon's words

> Working sponsor question, inferred from Brief A: What is driving the change in Kalpa Health's test volume between H1 2025 and H1 2026: more people, more visits per person, or more tests per visit?

## 2. The question in our words

The sponsor needs one evidence-based explanation of test-volume growth. We will decompose the change into people, visits per person and tests per visit using the cleaned, comparable booking data. The answer will show whether growth came primarily from acquiring more people, increasing visit frequency, or changing the number of tests per visit.

## 3. The question she did not ask

What operational or commercial factors explain the observed change after the data has been made comparable? This matters because the available exports can describe the pattern and quantify the reconciliation, but may not establish why patients or clinics behaved differently.

## 4. Translation into the method

| Her words | The Week 1 or 2 method it maps to | Where the vocabulary changes |
|---|---|---|
| Test volume changed | The tree: people × visits per person × tests per visit | “Growth” must be separated into its measurable drivers. |
| Test volume changed | The tree | The total must be separated into people, visits per person and tests per visit. |

## 5. What does not transfer from Retail

| In Retail | In a diagnostics business | What changes for our analysis |
|---|---|---|
| A missed sale costs one order. | A missed visit may affect several tests and downstream lab capacity. | Count visits and tests separately. |
| The shopper chooses the basket. | A patient, clinic, channel and test package jointly shape the visit. | Preserve booking, patient and test grains. |
| | One visit can appear differently across booking, collection, invoice and payment systems. | Define identities and reconcile systems before comparing totals. |

## 6. Our prediction, before the data

Before profiling, dated 2026-10-23: we expected the apparent change in test volume to be a combination of patient volume, visit frequency and tests per visit rather than one single driver. We also expected some legacy-versus-Nova difference to be measurement-related because the source systems have different grains. The Brief-A result now supports the first two points as descriptive findings; the source-system and booking-line limitations remain caveats, not causal explanations.

## 6a. What the Hypo A files show now

The saved Hypo A results support the prediction as a description of the data: validated booking test lines rose from **433,611** in H1 2025 to **455,383** in H1 2026 (**+5.02%**). People rose **3.77%**, visits per person fell **0.97%**, and test lines per visit rose **2.20%**. This describes the pattern; it does not prove why the pattern happened. The measure counts validated booking test lines, not confirmed attended or performed tests.

## 6b. Team ownership

| Member | Brief-A responsibility | Main evidence |
|---|---|---|
| Aayush | Own the integrated Brief-A answer and keep the final project package consistent | Notebook 05 methods, Notebook 06 cold run, charter, statement, logs, diagrams, write-ups and board artifact |
| Harsh | Own the Hypo-A recalculation and the evidence for the selected drivers | IITGN-aligned metric summary, component changes, city contributions, identity checks and reconciliation |
| Riya | Own loading, validation, cleaning checks and reproducibility | Profiling, accepted/rejected reconciliation, SQL reproduction, join checks and cold-run validation |

All three members review the metric definition, reproduce the headline numbers and can explain the limitations. A booking test line is the selected descriptive measure for this submission; it is not presented as an attended, collected or performed test.

## 7. Requirements

### Functional: what the analysis must do

| # | Requirement | How we will show it is met |
|---|---|---|
| F1 | Explain H1 2025 versus H1 2026 test-volume change. | Tree decomposition with counts, rates, periods and denominators. |
| F2 | Validate the decomposition. | The factors multiply back to the observed test totals and the log-growth branches reconcile. |
| F3 | Preserve reproducibility and auditability. | Cold run, validation checks, rejected-record file and decision logs. |

### Non-functional: how well it must do it

| # | Requirement | How we will show it is met |
|---|---|---|
| N1 | Re-runs from a fresh Codespace in under ten minutes with no manual edits. | A teammate's cold run, logged in decisions-log.md. |
| N2 | An analyst can audit every number back to rows. | Clean tables, SQL grain comments and exception lists. |
| N3 | Every cleaning decision is written down with its reason and effect. | decisions-log.md and challenges-log.md. |
| N4 | No raw record is silently repaired or discarded. | Accepted/rejected reconciliation and explicit anomaly handling. |

### Constraints: what we cannot change

| # | Constraint |
|---|---|
| C1 | Use the repository's Python, Pandas and SQL workflow with the released raw data. |
| C2 | Do not make causal or clinical claims unsupported by the exports. |
| C3 | Preserve raw files; cleaning must be reproducible and logged. |
| C4 | Work within the available January 2025 to June 2026 data period. |

## 8. Scope

| In | Out, and why |
|---|---|
| H1 2025 versus H1 2026 test-volume decomposition | Causal explanations that require data not present in the pack |
| Booking and patient cleaning used to support the growth measure | Booking-system comparison, campaign-effectiveness claims and clinical interpretation |
| Reproducible clean tables, SQL and audit logs | Unverified repair of ambiguous IDs and periods outside the released data |

## 9. Done looks like

Done means a fresh run produces clean, reconciled tables and one defensible finding explaining H1 2025 versus H1 2026 test-volume change through people, visits per person and tests per visit. Each factor carries its denominator, period, caveat and action.

## 10. Who signs off

| Reader | What they will check | What would make them reject it |
|---|---|---|
| Dr Menon | The growth finding and its action | A number without a comparison, denominator or period |
| The data reviewer | Every factor traces to rows and its definition is clear | A tree that does not reconcile to total test growth |
| Operations leaders | The people, visit-frequency and test-mix interpretation is fair | Treating raw source-system row counts as the driver without checking grain |
