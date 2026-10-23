# Project charter · Objectives A, B and E · Group 6

The charter is the one page a sponsor signs before work starts. It says what will be delivered, by whom, by when, with what, and what counts as done. Fill it in Scope and commit it before the first notebook. Change it later only by adding a dated line under "Changes", never by silent edit.

| | |
|---|---|
| Project | Build 1 · Data to Insight in Kalpa Health · Objectives A, B and E |
| Sponsor | Dr Priya Menon, COO, Kalpa Health |
| Reviewers | The finance controller (auditability); <the stakeholder your brief touches> |
| Group | 6 |
| Repository | <public URL> |
| Working days | Three to four, ending with the presentation |
| Charter committed on | 2026-10-23 |

## 1. The question, in the sponsor's words

> Working sponsor question, inferred from Objectives A, B and E: What is happening to Kalpa Health's test volume, how much of the apparent change is real rather than a booking-system measurement effect, and did the campaign increase bookings beyond seasonality and patient mix?

## 2. The question, in ours

The sponsor needs one evidence-based view of growth, booking measurement and campaign performance. We will decompose test-volume change into people, visits per person and tests per visit; compare legacy and Nova using a common booking definition and like-for-like periods; and compare campaign versus non-campaign bookings while accounting for seasonality, patient mix and segment differences. The answer determines whether the next action belongs primarily with operations, data governance during migration, or marketing experimentation.

## 3. The deliverables

| # | Deliverable | Form | Acceptance test |
|---|---|---|---|
| D1 | The claims | Three concise findings covering growth, booking comparability and campaign effectiveness, each with a number, denominator and period | Dr Menon can repeat the findings without a follow-up question about the base or timeframe |
| D2 | The evidence | Notebooks 01 to 06 running cold; SQL queries finance can re-run | A teammate's fresh-Codespace run produces the same clean-table counts and headline outputs |
| D3 | The audit trail | approach, decisions, challenges logs | Every number traces to rows; every rule has a reason and an effect |
| D4 | The action | A prioritized recommendation for operations, data quality and collections | States what to do, what it costs, and what being wrong costs |
| D5 | The write-ups and the video | docs/writeups.md, video link in README | The team's reasoning and limitations are documented |

## 4. Targets

| Target | Measure | Owner |
|---|---|---|
| T1 Explain growth | Decompose test volume into people, visits per person and tests per visit | |
| T2 Compare systems fairly | Report like-for-like legacy versus Nova booking measures and caveats | |
| T3 Evaluate campaign effect | Compare offer and non-offer bookings by period and segment, and separate lift from mix or seasonality | |
| T4 Auditable | Decisions log reconciles at every step | |
| T5 Reproducible | Cold run under ten minutes | |
| T6 Defended | Any member, any number, alone | |

## 5. Scope

| In | Out |
|---|---|
| H1 2025 versus H1 2026 test-volume decomposition; comparable booking measures across legacy and Nova; campaign/offer comparison; data-quality exceptions; reproducible evidence and recommendations. | Causal claims not supported by the exports; patient-level clinical conclusions; changing raw records to force a match; analysis outside the available period and source systems. |

## 6. Roles and parts

| Member | Part owned | Notebooks | Also responsible for |
|---|---|---|---|
| | | | |

## 7. Risks, and what we do about them

| Risk | Likelihood | Impact | What we do |
|---|---|---|---|
| The two booking systems count differently and we compare them anyway | | | Trace one visit through both before any count |
| A join doubles the headline silently | | | Row-count check on every join; `validate=` on every merge |
| We discover the claim on the last day | | | Claim stated by the middle of Analyse; the rest tests it |
| One member holds all the understanding | | | Rotate roles daily; every member runs the cold run once |
| | | | |

## 8. Assumptions we are making

| Assumption | What would prove it wrong | Where it appears if it does |
|---|---|---|
| The pack covers the whole first half of both years | A gap in the monthly counts | Findings and caveat |
| Booking-test rows can be rolled up to a comparable booking definition | Duplicate or missing booking identities that cannot be reconciled | System-comparison caveat |
| Captured payment references can be normalized without guessing | Unmatched or ambiguous invoice references remain after normalization | Collections exception list |

## 9. Decision rights

| Decision | Who makes it | By when |
|---|---|---|
| The identity rule for a booking | Group 6, documented in the decisions log | Before notebook 03 |
| The headline claims | Group 6 after peer review | Before notebook 05 is frozen |
| Freeze | Group 6 | The evening before the presentation |

## 10. Changes

| Date | What changed | Why | Who |
|---|---|---|---|
| 2026-10-24 | Changed the selected objectives from A, B and C to A, B and E. | The project now focuses on test-volume growth, fair Legacy/Nova comparison and campaign/offer effectiveness; invoice/payment work remains documented data-quality groundwork rather than a headline objective. | Group 6 |
