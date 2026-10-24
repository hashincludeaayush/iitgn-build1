# Brief A analysis plan and Hypo A result

**Status:** Working draft authored 2026-10-24. Hypotheses retain their original prediction labels and authored dates. The user later selected the IITGN Build 1 cleaning rule for the current Brief A calculations; the dated addendum at the end records the redefinition and measured values. Earlier Brief A candidate sections remain historical and are not the current primary values. The IITGN-aligned measure is still not owner-confirmed as the official KPI.

## Current result

Hypo A currently shows **455,383** validated booking test lines in H1 2026 versus **433,611** in H1 2025, a **5.02% increase**. The increase combines **3.77% more people**, **0.97% fewer visits per person**, and **2.20% more test lines per visit**. These are descriptive results, not causal proof. The saved CSV files in `data/hypo_A/` are the evidence used for this summary.

## Scope, decisions, and governance

The selected work is Brief A only. Brief B and Brief E are outside the current scope. This plan records the question, the checks, the prediction and the evidence used for the H1 test-volume comparison.

The decisions are: (A) how to allocate test-volume resources against the city plan; (B) whether to change targets or staffing in the affected cities; and (E) whether to increase the offer budget. The analysis should first verify each metric and baseline, locate any change, test the customer journey and documented operational changes, then choose a primary metric, a few diagnostics and guardrails, the simplest distinguishing method, and an action. No action recommendation is made here.

**Assistant-use disclosure:** The handbook says assistants must not generate analysis, notebooks, write-ups, or scripts. The team has reported a later instructor clarification permitting AI assistance for multi-brief work, but the clarification date and exact scope are not recorded in the project files. This draft was created with assistant help at the user's direction and will be recorded in ai-log.md. Confirm and document whether the instructor's permission covers analysis planning, analysis, code, slides, and write-ups. The handbook restriction has not been silently edited or removed.

## Data status and prerequisites

- The approved clean outputs cover bookings, collections, patients, invoices, gateway payments, settlements, results, campaign master and tags, and the city, clinic, and test references.
- **Brief A plan-table profile/cleaning step completed 2026-10-24:** the documented wide CSV contains six city/metric source rows and six 2026 monthly columns. All six source rows were retained and expanded to 36 unique city/metric/month rows; all source cells were populated, all targets parsed as nonnegative integers, there were no duplicate keys, and the source matched its manifest. Exact source labels and raw target strings remain available in `data/clean/plan_2026_H1_source_rows.csv` and `data/clean/plan_2026_H1_clean.csv`. At that table-cleaning step, no booking join, city alias, target aggregation, or actual-versus-plan comparison was made. A later candidate baseline comparison is recorded in the dated section below; `Bangalore` remains unmapped.
- The source README documents that the new booking system was used in Chennai and Jaipur from April 2026; four cities continued using the old system. Use this as documented system-change context, not evidence that the migration caused a booking change.
- Existing cleaning profiles found exact city-label differences between booking and reference/clinic labels: legacy booking rows labelled Bangalore remain distinct from Bengaluru. Do not silently map them in city or plan comparisons; obtain a dated crosswalk or retain an unresolved category.
- Campaign tags are not an assignment log: a tag does not by itself prove offer exposure, eligibility, redemption, or non-exposure for untagged patients. Existing exact-ID exceptions must remain visible.

## Brief A metric/baseline check — candidate counts only (2026-10-24)

This is the single approved metric/baseline step after profiling the H1 plan. It does not freeze an official KPI definition or alter the dated predictions above. The pack README calls the targets “test-volume” targets but does not say whether test volume means booked test lines, collected samples, result runs, or another unit. No written owner rule for the reported 5% or +18% was found in the supplied project files.

**Provisional candidate unit:** one booking source-test row with a nonblank `test_code`; count rows by the local calendar month in `slot_at`. This preserves source-line grain and does not assume that `n_tests`, a collection row, or a result run is the official KPI. The same source-line rule using `created_at` is shown only as a date-anchor sensitivity. `booking_id` and `system` remain strings; city labels are exact source text. No status or reschedule filter, row-level join, ID normalization, or city alias is applied.

| Candidate comparison | H1 2025 denominator | H1 2026 numerator | Difference | Rate and status |
|---|---:|---:|---:|---|
| Nonblank booking `test_code` lines by `slot_at` month | 435,880 | 461,080 | +25,200 | +5.7814%; candidate only, not an official KPI reproduction |
| Same source-line rule by `created_at` month | 436,094 | 454,873 | +18,779 | +4.3062%; diagnostic alternative date anchor |

The slot-date candidate rounds to 5.8% (6% to a whole percent), so it does not exactly reproduce a stated 5% claim. The created-date candidate is 4.3%. Without Marketing/COO's source definition and dashboard bridge, the 5% cannot be confirmed or reconciled. The candidates are not evidence that demand or performance grew by either rate.

The H1 slot windows contain 897,846 source rows: 896,960 have a nonblank `test_code`; 886 blank-code/zero-test placeholder rows remain outside this candidate count. The booking file-reconciliation table contains all 36 monthly city files in each H1 window, with zero source-row or expanded-test-row reconciliation failures. The created-date windows contain 891,840 source rows: 890,967 nonblank-code rows and 873 blank-code/placeholder rows. Source counts reconcile exactly to `n_tests - n_blank_test_code_rows` in the canonical booking output across 148 city/system/month/date-anchor groups. All booking source timestamps in the provenance table carry `+05:30`; dates are counted on that local calendar without changing IDs or timestamp values.

All H1 2025 booking lines are legacy. In H1 2026, 398,769 candidate lines are legacy and 62,311 are Nova; the pack README says Nova began in Chennai and Jaipur in April 2026. All status values were retained: 398,769 legacy lines have no `status_at_export`, 58,770 Nova lines are labelled `booked`, and 3,541 are labelled `rescheduled`. These labels are not an approved eligibility rule. In H1 2026, 751 candidate lines also belong to booking records where `slot_at` precedes `created_at`; they remain counted pending a source explanation. The booking-level `ready_for_test_volume_analysis` flag is not used to remove entire bookings: doing so would exclude 814 nonblank coded lines from 463 flagged booking groups.

**Plan comparison remains incomplete on exact city labels.** The plan totals 515,740 targets. Its six exact city/month keys do not align completely with booking slot-city keys: 30/36 city-month pairs match; six plan rows are `Bangalore` with no exact H1 2026 slot-city match, while six actual rows are `Bengaluru` with no exact plan label. No alias/crosswalk was applied.

| Exact-label matched city subset only | H1 2026 candidate lines | H1 2026 target | Difference | Actual vs target |
|---|---:|---:|---:|---:|
| Ahmedabad | 84,986 | 90,773 | -5,787 | -6.4% |
| Chennai | 83,049 | 93,912 | -10,863 | -11.6% |
| Hyderabad | 78,575 | 86,421 | -7,846 | -9.1% |
| Jaipur | 41,424 | 52,372 | -10,948 | -20.9% |
| Pune | 65,503 | 72,177 | -6,674 | -9.2% |
| **Five-city partial subtotal** | **353,537** | **395,655** | **-42,118** | **-10.6451%** |

The separate `Bangalore` plan subtotal is 120,085; the H1 2026 source has no exact slot-city label `Bangalore`. The separate `Bengaluru` actual subtotal is 107,543 and has no exact plan row. Summing all six observed actual labels gives 461,080 against the six plan labels' 515,740, a raw aggregate ratio of -10.5984%; this is explicitly **unreconciled, not a validated overall plan variance** until city coverage is confirmed with an approved effective-dated crosswalk. The plan sum is 18.3216% above the H1 2025 slot-date candidate, a diagnostic relationship only; it is not proof that the documented +18% plan was defined on this denominator.

Outputs and reproduction are in `notebooks/05a_brief_a_metric_baseline.ipynb`, `src/kalpa/brief_a_baseline.py`, and the three `data/clean/brief_a_metric_baseline_*.csv` files. Existing `05_methods.ipynb` and `06_answer_cold_run.ipynb` were not run. In particular, the latter's “collected or no-show” eligibility wording remains unverified and was not used. No driver decomposition, collection/result comparison, final claim, or slide was produced.

## Provisional metric contracts

These contracts are candidates for stakeholder confirmation, not final KPI definitions.

| Brief | Decision metric | Numerator / denominator and period | Diagnostics | Guardrails |
|---|---|---|---|---|
| A | Actual 2026 H1 test volume versus the sum of the city-month plan; report the absolute test gap and percent of plan. The 5% year-over-year figure is a separate reproduction check. | Plan variance = (eligible actual tests in 2026-01-01 through 2026-06-30 minus planned tests for those city-months) / planned tests for those city-months. Reproduction check = (eligible tests in 2026 H1 minus eligible tests in 2025 H1) / eligible tests in 2025 H1. Confirm the date anchor and eligible-test rule with the KPI owner before counting. | Patient count; visits per patient; tests per visit; monthly and city/channel components; booked versus collected/result-backed test counts. | Comparable source coverage, unresolved city labels, ID/reschedule sensitivity, patient-map sensitivity, and no conversion of missing collection/result links into automatic cancellations. |
| B | Comparable booking count by city after validating what one visit means in legacy and nova. | Raw change per city = Q2 2026 booking count minus Q1 2026 booking count; relative change = that difference / Q1 2026 booking count. Windows are provisionally 2026-04-01 through 2026-06-30 versus 2026-01-01 through 2026-03-31; confirm this is the count behind the COO's statement. Report raw and harmonized counts separately. | Recording component versus residual change; distinct patient/visit counts; collections/results corroboration; monthly trends by system, city, channel, and source. | File coverage, system-migration timing, unmatched keys, city labels, reschedule rules, and unequal calendar-day counts. Do not infer a confirmed/tentative rule from status names. |
| E | Causal effect on booking incidence among a defined eligible population, if a credible assignment/control design exists. If not, causal effect stays unresolved; the 9% report is only a descriptive reproduction. | Descriptive candidate = (eligible bookings in the campaign quarter minus eligible bookings in the immediately prior quarter) / eligible bookings in the prior quarter. Exact campaign period, booking definition, city scope, and denominator must first be obtained from Marketing. Preferred causal estimand, if randomized assignment exists: eligible assigned patients with at least one qualifying booking in the fixed follow-up window / all eligible assigned patients in each arm; compare offer versus holdout (intention-to-treat risk difference). | Prior booking frequency, new versus returning patients, city, channel, home-collection usage, exact campaign-tag linkage, and segment-level descriptive rates. | No inferred control group, incomplete tags, concurrent campaigns, selection into offer use, campaign costs, home-collection capacity, and contribution margin. |

### Metric-definition gates

1. For A, confirm whether test volume means booked test lines, collected samples, result runs, or another reported measure. The handbook describes a test as needing a booking, collection, and result, but the supplied collection source is visit-level and does not identify each test. A booking test line and a result row are not interchangeable without a reconciliation rule. Keep the 5% year-over-year rate separate from actual-versus-plan variance against 18%; do not subtract unlike denominators.
2. For A, use city-month plan rows only after the plan table is profiled. Reconcile city totals to the all-city total. The plan's city labels must match actual city labels exactly or use an approved, effective-dated crosswalk.
3. For B, first trace representative real-world visits across old/new booking rows, collections, and results. Define comparable booking/visit identity from evidence. Keep source IDs as strings; retain unknown mappings and unmatched rows. The candidate quarterly windows above are provisional and may not match the COO's undocumented dashboard rule.
4. For E, obtain the written Marketing definition behind 9%: exact dates, booking grain, numerator, denominator, city/channel scope, eligibility, and comparison. Recompute that descriptive metric before profiling treatment selection. A pre/post change or matched comparison alone is not a causal estimate.

## Brief A - Growth

**Decision:** Identify the branch and city/channel that explain the test-volume plan gap, so the COO can decide where to direct staff, reagents, and capacity. No branch is presumed responsible.

**Primary / diagnostics / guardrails:** Primary is actual eligible 2026 H1 test count versus the profiled city-month plan. Diagnostics are same-half year-over-year growth, the patient x visits-per-patient x tests-per-visit identity, and city/channel contribution. Guardrails are source coverage, data-definition sensitivity, city mapping, and identity/reschedule sensitivity. The branch identity is usable only if all factors reconcile exactly to the selected test count under one visit rule.

### A-H1 - The reported year-over-year rate is reproducible

- **Prediction, not finding; authored:** 2026-10-24. The 5% claim will be reproducible to the stated rounding once the official test unit, event date, population, and source table are applied consistently to both first-half periods.
- **Evidence fingerprint if true:** Monthly source counts reconcile to eligible H1 totals under one documented definition; the same rule applied to 2025 and 2026 yields approximately the reported 5%, and changing the plan denominator does not change this YoY rate.
- **Evidence that weakens or contradicts it:** No documented definition yields the claim; source coverage differs by month/system; or the result depends materially on counting booking test lines versus result rows or on unresolved city mapping.
- **Required tables / fields / keys:** Booking test source rows (system, booking_id, test_code, created_at/slot_at raw and parsed, city, channel, source_file, source record/order); collections (booking_id, status, collected_at); results (booking_id, test_code, result_ts, source file/row); and the KPI definition. Preserve source row provenance. Candidate exact visit key is system + booking_id pending validation; link result rows to bookings by exact booking_id and test_code where supported. Collection links are booking-level, not test-level.
- **Metric numerator / denominator / period:** Numerator = T_2026H1 - T_2025H1; denominator = T_2025H1; rate = numerator / denominator. Periods are 2026-01-01 through 2026-06-30 and 2025-01-01 through 2025-06-30. T is undefined until the KPI owner confirms the eligible test rule and date anchor.
- **Alternatives / confounders:** Booking-created versus slot date versus result date; migration from legacy to nova in two cities in April; test-array expansion; blank tests; repeat result runs; reschedules; missing collections/results; late/out-of-window exports; and city label mismatch.
- **Decision affected:** Whether the board's 5% starting point is a sound baseline for resource allocation and plan variance.
- **What would change the team's mind:** A written KPI definition and a reproducible row-level bridge showing the dashboard count, source coverage, and both half-year totals. A material discrepancy under that rule changes the prediction to a definition/coverage reconciliation problem.

### A-H2 - Patient volume is the largest short branch

- **Prediction, not finding; authored:** 2026-10-24. One candidate explanation is that the number of distinct patients with an eligible visit/test grew less than planned and contributes more to the shortfall than visit frequency or tests per visit.
- **Evidence fingerprint if true:** Under a consistent visit/test definition, distinct patients are the branch with the largest adverse change; visits per patient and tests per visit are stable or contribute less, and P x (V/P) x (T/V) reconciles to T in each half.
- **Evidence that weakens or contradicts it:** Patient counts are stable or rise, while visits per patient or tests per visit account for the larger change; the ranking changes when patient_id is used instead of the reversible person_id proxy.
- **Required tables / fields / keys:** Canonical bookings (system, booking_id, patient_id, created_at, slot_at, city, channel, reschedule fields); patient ID map (patient_id, person_id, identity_rule); booking test rows, collections, and results under the chosen eligibility rule. Join the patient map by unchanged patient_id; retain an account-ID sensitivity measure because person_id is an analytic proxy.
- **Metric numerator / denominator / period:** P_t = distinct eligible person_id with at least one eligible visit/test in half-year t; patient growth = (P_2026H1 - P_2025H1) / P_2025H1. Visit frequency = eligible distinct visits / P_t. Periods are the same H1 windows as A-H1. These component ratios must multiply back to the corresponding total under the chosen grain.
- **Alternatives / confounders:** Patient-account merges, incomplete person identity, new versus returning patient definitions, city/system migration, unlinked booking rows, and test eligibility.
- **Decision affected:** Acquisition/retention effort versus operations or capacity investment.
- **What would change the team's mind:** A validated identity crosswalk or sensitivity analysis that moves the largest contribution to a different branch; evidence that a new-patient/returning-patient definition changes the decision.

### A-H3 - Visit frequency or tests per visit is the largest short branch

- **Prediction, not finding; authored:** 2026-10-24. A competing explanation is that patients are making fewer eligible visits, ordering fewer tests per visit, or both; the separate middle and final branches will show which, if any, is short.
- **Evidence fingerprint if true:** Visits per patient (V/P) and/or tests per visit (T/V) declines relative to the corresponding baseline/plan contribution; all components multiply to T and the pattern remains when booked, collected, and result-backed definitions are compared.
- **Evidence that weakens or contradicts it:** Both ratios are stable or higher and the patient count or measurement rules explain the gap; the component identity fails to reconcile because the chosen visit/test grain is invalid.
- **Required tables / fields / keys:** Booking test rows (system, booking_id, test_code, source_test_order, date fields); canonical booking rows (patient_id, rescheduled_from, status_at_export, city, channel); collections (booking_id, status, collected_at); results (booking_id, test_code, result_ts). Candidate visit key system + booking_id; validate reschedule chains before deduplicating. Preserve repeated result rows unless a documented event key supports classification.
- **Metric numerator / denominator / period:** V/P = distinct eligible visits / distinct eligible patients; T/V = eligible tests / distinct eligible visits; periods are 2025 H1 and 2026 H1, with growth/plan contribution computed from each period's component. Numerators and denominators use the same city/system inclusion rule.
- **Alternatives / confounders:** Reschedule recording, split test arrays, repeat lab runs, changes in channel/city mix, migration timing, and tests whose visit has no collection/result export.
- **Decision affected:** Scheduling, service mix, clinic capacity, and channel investment.
- **What would change the team's mind:** A row-level visit trace or authoritative reschedule/test-run rule showing the apparent component change is a recording artifact, or a sensitivity check that reverses which branch contributes most.

### A-H4 - Part of the apparent gap is a definition or coverage change

- **Prediction, not finding; authored:** 2026-10-24. A competing explanation is that the reported YoY number or plan gap changes materially when both halves are put on the same source coverage and test eligibility rules, particularly around the booking-system migration.
- **Evidence fingerprint if true:** Monthly/system source coverage or eligible test counts shift at migration; alternative reasonable source definitions produce materially different growth, while a common rule narrows or changes the apparent plan gap.
- **Evidence that weakens or contradicts it:** Complete and comparable monthly coverage, consistent source-to-result/collection reconciliation, and a stable headline across documented definitions.
- **Required tables / fields / keys:** Booking per-file reconciliation/provenance and test rows; collections and results with booking_id, test_code, status/timestamps, file/row lineage; migration dates and dashboard definition; plan city/month rows after their separate cleaning step. Use exact source identifiers and do not infer status mappings.
- **Metric numerator / denominator / period:** Difference in YoY rate across candidate documented definitions, each using (T_2026H1 - T_2025H1) / T_2025H1. Report record coverage as matched eligible rows / candidate source rows separately, by month and system; no denominator is silently removed. Periods are the two H1 windows.
- **Alternatives / confounders:** Real demand change may coexist with migration; quarter seasonality, delayed result timestamps, file gaps, and unmatched IDs can mimic coverage changes.
- **Decision affected:** Whether to act on the headline now or first correct KPI instrumentation and restate the baseline.
- **What would change the team's mind:** A source-owner definition and complete period-level coverage reconciliation that makes all reasonable definitions converge; or a clear definition change that accounts for the gap.

## Brief B - Two Cities

**Decision:** Whether to reduce targets or headcount in the two cities named by the COO. The raw pack documentation says Chennai and Jaipur moved to nova from April 2026; treat these as migration context, not proof of cause. Confirm the COO's affected-city labels and comparison window.

**Primary / diagnostics / guardrails:** Primary is the per-city change in comparable bookings under an evidenced visit rule, with raw counts and harmonized counts shown separately. Diagnostics are system-specific monthly counts, hand-reconstructed visit examples, distinct patients, and collection/result corroboration. Guardrails are source coverage, unmatched keys, raw city labels, reschedules, and asymmetric export behavior.

### B-H1 - Recording differences explain most of the apparent fall

- **Prediction, not finding; authored:** 2026-10-24. A candidate explanation is that old/new system row shapes or status/reschedule behavior create a substantial part of the reported Q2 booking decline.
- **Evidence fingerprint if true:** Hand-traced visits show that one business event is represented differently across systems; the raw-to-comparable count bridge removes much of the decline after a documented mapping, with rejected/unmatched records accounted for.
- **Evidence that weakens or contradicts it:** Representative visits have equivalent one-visit counts in both systems, IDs and statuses reconcile under source documentation, and the comparable Q2 decline remains close to the raw decline.
- **Required tables / fields / keys:** Raw/canonical booking source rows (system, booking_id, patient_id, created_at_raw, slot_at_raw, city/path, clinic_id, status_at_export, rescheduled_from, source_issue, test arrays/source_test_order, source_file and row); collections and results keyed by unchanged booking_id and, for results, test_code; invoice booking_id only as an independent visit check if valid. Use system + booking_id for within-system identity and an evidenced cross-system visit map for cross-system identity. Keep unmatched/ambiguous IDs.
- **Metric numerator / denominator / period:** For each confirmed affected city, raw bookings Q2 minus Q1 and relative change = (N_Q2 - N_Q1) / N_Q1; candidate windows are 2026-04-01 to 2026-06-30 and 2026-01-01 to 2026-03-31, subject to stakeholder confirmation. Recording component = raw Q2-minus-Q1 change minus harmonized Q2-minus-Q1 change, in counts; report this separately from the harmonized residual. Denominator for each relative change is that city's Q1 count. Also show monthly counts and per-calendar-day rates as a sensitivity because the quarters have different day counts.
- **Alternatives / confounders:** Real demand change, seasonality, competitor centres/prices, channel mix, export coverage, legacy slot overwrite, nova reschedule records, status semantics, city label differences, and cancellations absent from collection records.
- **Decision affected:** Whether to protect targets/headcount pending measurement repair or accept a real decline.
- **What would change the team's mind:** Vendor documentation plus multiple source-row traces with stable mapped visit identity; if the mapping is ambiguous or unmapped share can change the decision, do not claim a recording share.

### B-H2 - A real demand decline remains after comparable counting

- **Prediction, not finding; authored:** 2026-10-24. A competing explanation is that comparable eligible visits/patients decline in the affected cities even after the system recording difference is removed.
- **Evidence fingerprint if true:** The residual Q2 change remains negative under defensible old/new rules and is corroborated by one or more independent journey signals (patient visits, collections, results) with coverage stable enough to interpret; the decline is not solely a test-array or status-count change.
- **Evidence that weakens or contradicts it:** Harmonized booking counts recover to baseline, the residual is within expected count noise, or collection/result sources have timing/coverage gaps that prevent corroboration.
- **Required tables / fields / keys:** Same booking event map as B-H1; patient map by exact patient_id; collections by booking_id/status/collected_at; results by booking_id/test_code/result_ts; city and clinic references. Keep booking, collection, and result measures separate; do not require a result to call an appointment a booking.
- **Metric numerator / denominator / period:** Harmonized eligible Q2 booking count minus harmonized eligible Q1 count; relative change divides by harmonized Q1 count, per city. Diagnostics: distinct patients in the same windows and collection/result-linked events / eligible booking rows. Compare monthly and same-quarter 2025 trends if file coverage permits; the primary requested comparison remains the stakeholder-confirmed window.
- **Alternatives / confounders:** Migration, competitor entry, price changes, calendar/holiday mix, channel mix, patient identity mapping, and incomplete or delayed collections/results.
- **Decision affected:** City targets and staffing, with a cost of cutting a healthy city.
- **What would change the team's mind:** A validated cross-system event mapping that eliminates the residual, or interviews/operational records showing cancellations, capacity, or external causes not represented in these exports.

### B-H3 - External competition or pricing explains a residual city decline

- **Prediction, not finding; authored:** 2026-10-24. The competitor story in the brief is a plausible alternative to migration, but the supplied operational data alone cannot establish it.
- **Evidence fingerprint if true:** Independently dated competitor-centre openings/prices and city-head evidence align with the onset and affected geography, and the comparable residual is larger in exposed segments than in plausible unaffected comparisons. This would be supportive, not causal proof by itself.
- **Evidence that weakens or contradicts it:** No verified opening/price dates, the residual predates competitor entry, or the same decline appears in unexposed channels/cities.
- **Required tables / fields / keys:** Comparable bookings/patients/collections/results as in B-H2; additional verified competitor opening dates, locations, prices, and city-head interviews. Those external competitor data are not in the current pack.
- **Metric numerator / denominator / period:** Comparable city booking change as in B-H2, with any exposed/unexposed segment rate defined by a verified exposure rule; numerator = change in eligible bookings, denominator = baseline eligible bookings, period = confirmed pre/post competitor dates. Without exposure data, this comparison is not estimable.
- **Alternatives / confounders:** System migration, seasonality, pricing by Kalpa, city/channel composition, capacity, and concurrent local campaigns.
- **Decision affected:** Whether to respond with staffing/targets, pricing, channel investment, or further market research.
- **What would change the team's mind:** Verified exposure/timing evidence and a comparison that addresses migration and seasonality; otherwise keep this explanation unresolved and ask the city heads.

## Brief E - The Offer

**Decision:** Whether to increase the free-home-collection budget. The handbook says the offer cost includes a phlebotomist visit per booking, but the current data profiles do not provide a verified incremental cost, eligible-population denominator, or randomized holdout. No budget recommendation is made here.

**Primary / diagnostics / guardrails:** Primary should be incremental booking incidence among eligible assigned patients versus a contemporaneous holdout. It is not identified by a before/after count or a campaign-tagged cohort alone. Diagnostics are exact campaign-link coverage, previous booking behavior, city/channel/patient segments, and home-collection usage. Guardrails are incremental delivery cost, contribution margin, capacity, cancellations/no-shows, and missing exposure/assignment records.

### E-H1 - Marketing's descriptive 9% can be reproduced

- **Prediction, not finding; authored:** 2026-10-24. The reported 9% may be reproducible as a descriptive quarter-over-quarter booking-count change once Marketing supplies its exact definition; matching the arithmetic would not establish causality.
- **Evidence fingerprint if true:** The documented offer dates, city/channel scope, booking grain, numerator, and prior-quarter denominator reproduce the 9% within stated rounding from traceable booking rows.
- **Evidence that weakens or contradicts it:** The 9% cannot be reproduced under Marketing's stated rule, the time windows or city scope differ, or exact campaign links/booking eligibility are incomplete.
- **Required tables / fields / keys:** Marketing's original calculation and definition; campaign master (campaign_id, starts, ends); campaign tags (booking_id, campaign_id, waiver_rs, link status); canonical bookings (booking_id, system, created_at/slot_at, patient_id, city, channel, home_fee); exact unchanged booking_id links and person map. Campaign tags alone do not establish complete exposure.
- **Metric numerator / denominator / period:** Candidate descriptive relative change = (N_offer-quarter - N_immediately-prior-quarter) / N_immediately-prior-quarter. N is the distinct eligible booking count under Marketing's definition. The numerator, denominator, quarter dates, city scope, and channel scope remain unconfirmed. Use the exact dates supplied by Marketing, not a guessed quarter.
- **Alternatives / confounders:** Calendar seasonality, city/channel/system mix, booking definition, unlinked tags, other concurrent campaigns, and changes in export coverage.
- **Decision affected:** Whether the headline claim is sufficiently defined to use in a budget meeting.
- **What would change the team's mind:** Marketing's row-level calculation, written denominator/window/scope, and a reconciliation to the bookings table. A reproduced 9% changes only descriptive confidence, not the causal verdict.

### E-H2 - Campaign-tagged patients were already more likely to book

- **Prediction, not finding; authored:** 2026-10-24. A candidate explanation is selection: patients tagged under the offer may have booked more often before it began than the eligible population generally.
- **Evidence fingerprint if true:** Among patients with a complete pre-period, exact-linked tagged patients have higher prior booking frequency or repeat-booking share than an independently defined eligible comparison population; the pattern persists by city/channel and after separating new from returning patients.
- **Evidence that weakens or contradicts it:** Pre-offer booking histories are comparable under a verified eligibility/exposure denominator, or a randomized holdout shows the post-offer difference despite balanced pre-period behavior.
- **Required tables / fields / keys:** Campaign tags (booking_id, campaign_id), campaign dates, canonical bookings (booking_id, patient_id, created_at, city, channel, home_fee), patient map (patient_id, person_id). Exact booking_id links only; 1,998 prior tag-to-booking exact-link exceptions remain unresolved. An eligible non-tagged population and exposure/assignment log are required for a valid comparison; absence of a tag is not proof of non-exposure.
- **Metric numerator / denominator / period:** Diagnostic = total eligible bookings per patient during the fixed pre-campaign window (numerator = pre-window bookings, denominator = patients with a complete observable pre-window); also report share with at least one prior booking (numerator = patients with prior booking, denominator = observable tagged patients). Compare offer-tagged to a separately validated eligible population; use the 90 days before campaign start only if Marketing confirms that lookback.
- **Alternatives / confounders:** Targeting rules, city/channel differences, patient tenure, prior campaign exposure, missing booking links, incomplete observation windows, and unobserved offer awareness.
- **Decision affected:** Whether the 9% descriptive increase is likely incremental enough to justify doubling the budget.
- **What would change the team's mind:** A documented eligible population and exposure assignment, balanced pre-trends, or a randomized holdout showing a positive effect independent of prior booking behavior.

### E-H3 - The offer caused an incremental increase in bookings

- **Prediction, not finding; authored:** 2026-10-24. A causal increase is possible but will remain unresolved with the current tag and before/after data unless a credible treatment/control design can be established.
- **Evidence fingerprint if true:** In a pre-registered randomized holdout (or a defensible natural experiment with explicit assumptions), offer-assigned eligible patients have higher booking incidence in a fixed follow-up window than control-assigned patients; baseline behavior and segment mix are balanced, treatment assignment is logged, and the effect is not explained by concurrent changes.
- **Evidence that weakens or contradicts it:** No assignment/holdout exists; exposure is defined only by post-booking tags; comparison groups differ at baseline; the effect disappears after accounting for pre-period booking behavior or migration/seasonality; or uncertainty includes no meaningful effect.
- **Required tables / fields / keys:** Current campaign and tag tables, bookings and patient map; additionally required for retrospective causal analysis: eligible-patient roster, treatment assignment and timestamp, offer exposure/delivery, holdout/control assignment, redemption, fixed outcome window, concurrent campaign flags, incremental home-visit cost, and contribution margin. These assignment/eligibility/cost fields are not established in the current cleaned outputs.
- **Metric numerator / denominator / period:** Preferred intention-to-treat outcome = eligible assigned patients with at least one qualifying booking during a pre-specified follow-up window / all eligible assigned patients in each randomized arm; effect = offer-arm incidence minus holdout-arm incidence. Unit = eligible patient; period = fixed follow-up from assignment. If the decision is about booking count per patient instead, pre-specify that as a separate outcome and keep the denominator as all eligible assigned patients. Current observational tables do not supply the required assignment denominator.
- **Alternatives / confounders:** Self-selection, prior booking frequency, seasonality, channel/city mix, migration, offer awareness without redemption, concurrent marketing, and changes in staff capacity.
- **Decision affected:** Increase, maintain, or stop the offer budget and set a future experiment.
- **What would change the team's mind:** A properly logged randomized holdout with enough follow-up and a pre-agreed minimum worthwhile effect/cost threshold. Without it, report causal effect as unresolved and recommend a next-quarter test rather than inventing a control group.

## Shared dependency map and provisional ownership

| Shared dependency | Brief A | Brief B | Brief E |
|---|---|---|---|
| Canonical bookings, exact IDs, dates, source provenance | Test-line count and period anchor | Old/new event mapping and city-quarter counts | Booking outcomes and exposure-link checks |
| Patient ID map and person proxy | Patient branch and new/returning split | Patient/visit corroboration | Prior booking behavior and patient-level denominator |
| Collections and results | Candidate completed-test validation | Independent journey corroboration | Home-collection and booking diagnostics |
| City/clinic references | City/channel plan reconciliation | Fair city comparisons and migration contexts | City segmentation |
| Campaign master/tags | Not primary | Concurrent campaign alternative | Offer dates, tags, eligibility and causal design |
| City plan | Profile/cleaning is complete; first candidate baseline comparison is recorded, with city crosswalk/KPI rule unresolved | Not primary | Not primary |
| Missing owner/external inputs | KPI definition and plan meaning | Vendor rules, city-head context, competitor dates/prices | Marketing metric definition, assignment/holdout, incremental cost |

After dependencies are accepted, possible ownership for three members is: Member 1 leads Brief A and the city-plan profile; Member 2 leads Brief B's old/new visit traces; Member 3 leads Brief E's campaign-definition and causal-design assessment. All three review shared metric contracts, reproduce all headline numbers, and can explain rejected alternatives. Names and ownership are not assigned here.

## Open questions and next actions

1. Confirm whether the team is formally answering A, B, and E or must select one brief; clarify the six-slide limit.
2. Record the date and exact scope of the instructor's AI-use clarification; do not alter the handbook/project-statement wording silently.
3. Confirm the KPI owner and exact definition of test volume, its event date, and the source behind the reported 5% and 18%.
4. **Completed:** profile and clean plan/plan_2026_H1.csv; then, after separate approval, run the candidate Brief A metric/baseline check in `notebooks/05a_brief_a_metric_baseline.ipynb`. The candidate outputs and exact-label partial plan reconciliation are saved under `data/clean/`. Obtain the official KPI definition and an effective-dated `Bangalore`/`Bengaluru` crosswalk before treating any plan percentage as the full-city result.
5. Confirm the affected cities/windows behind Brief B and request vendor definitions or a migration crosswalk and representative visit traces.
6. Request Marketing's 9% calculation, exposure/eligibility definition, assignment/holdout records, and actual incremental home-collection cost.
7. **Next A step, not started:** if separately approved, test the patient × visits-per-patient × tests-per-visit identity and related components using the provisional source-line candidate, clearly preserving unresolved KPI and city-label limitations. Keep each brief's analysis in its own dated section and update hypotheses only through dated revisions.

## Stop gate

The original dated hypotheses remain predictions. A single approved Brief A candidate metric/baseline step has been calculated and documented; it is not an official KPI reproduction or a validated full-city plan result. No driver decomposition, Brief B/E outcome analysis, causal claim, final recommendation, chart, or slide has been produced. Pause here for the next step approval.

## Brief A driver decomposition — dated measurement addendum (2026-10-24)

This addendum records the focused next step. It does not rewrite the original dated predictions, convert them into findings, or change the provisional KPI definition. Hypothesis statuses below describe evidence against those predictions; the city/channel concentration check is exploratory because no separate pre-outcome city/channel hypothesis card was present in the register before this run.

This dated update supersedes the earlier “Next A step, not started” and stop-gate status above; those statements document the prior checkpoint and are retained as history.

### Source and identity rules

- The 05a notebook, helper, all three baseline outputs, canonical booking table, booking source rows, patient-ID map, H1 plan, city/clinic references, and existing Brief A predictions/logs were inspected. The slot-date checkpoint is reproduced exactly: 435,880 in H1 2025 and 461,080 in H1 2026 (+25,200; +5.7814%). The created-date sensitivity also matches: 436,094 and 454,873 (+18,779; +4.3062%). All 148 stored source-to-canonical groups reconcile.
- Source rows represent expanded booking/test entries, not proof of completed tests. The candidate is a source row with nonblank `test_code` by local `slot_at` month, with all statuses and reschedule references retained. Input accounting is 436,302 = 435,880 kept + 422 blank-code rows classified for H1 2025, and 461,544 = 461,080 + 464 for H1 2026; no rows were rejected or removed.
- Primary patient measure: distinct unchanged `patient_id` values, labelled patient accounts represented in eligible booking-source lines—not patients proven served. Sensitivity: distinct `person_id` values from the reversible patient map. Both count 94,566 in H1 2025 and 98,125 in H1 2026. There are no missing IDs or map-unmatched eligible lines in either period; this particular sensitivity does not change the counts.
- Booking record identity: exact composite `system + booking_id`, unique in the canonical table and linked to all 896,960 eligible H1 source lines without fan-out. The data-pack README describes one booking as one patient visit, but the helper labels these as booking records/visit proxies because status and reschedule fields do not establish whether records refer to distinct attended visits. No reschedule deduplication was applied.
- The row-level identity uses `T = P × (B/P) × (T/B)`, where `T` is qualifying source test lines, `P` is distinct patient account IDs (or the person-proxy sensitivity), and `B` is distinct booking records. The identity reconciles in both periods with zero missing-ID lines and zero booking-to-patient conflicts. The order-independent Shapley bridge averages each factor's marginal contribution over all six change orders; it is an accounting attribution, not a causal estimate.

### Driver results and hypotheses

| Hypothesis / check | Result and status | Evidence against or alternative | Confidence and what would change the view |
|---|---|---|---|
| A-H1: the reported 5% year-over-year rate is reproducible | **Weakened; official KPI unresolved.** The unchanged slot-date candidate is +5.7814% (rounds to 6% at whole-percent precision); the created-date sensitivity is +4.3062%. | Excluding 3,541 H1 2026 lines with `status_at_export = rescheduled` gives 4.9690%; excluding 3,435 lines with nonblank `rescheduled_from` gives 4.9933%. These are unapproved and mutually different filters, not evidence that either is the KPI rule. In H1 2026 the two flags have zero overlapping lines; 3,541 status lines are on 1,499 booking records and 3,435 reference lines are on 1,456 other booking records. | High confidence in arithmetic; low confidence in KPI interpretation. A dated KPI-owner definition and dashboard-to-row bridge, including status/reschedule eligibility, could confirm or replace the candidate. |
| A-H2: patient volume is a material driver | **Supported descriptively as a positive contributor; not evidence of a patient shortfall versus plan.** Patient-account count rises 3,559 (+3.7635%). The Shapley attribution is +16,564 lines, 65.73% of the net +25,200. | `patient_id` is an account key, not a verified person identity. The person-proxy sensitivity happens to give the same period counts; this does not validate clinical identity. There is no patient-count plan denominator. | Moderate confidence in the account-count description; no causal conclusion. A verified identity crosswalk and patient-level plan/eligibility definition could change it. |
| A-H3: booking frequency or test lines per booking explain the change | **Weakened as an adverse short branch.** Booking records rise 6,652 (+3.5043%); booking records per patient fall slightly from 2.0073 to 2.0023 (-0.2498%), a Shapley contribution of -1,121 lines (-4.45% of net change). Test lines per booking rise from 2.2963 to 2.3468 (+2.2000%), contributing +9,757 lines (+38.72%). | Booking records are only visit proxies; reschedule/superseded-record semantics are unresolved. The test-line-per-record increase is not proof of increased performed tests. | Moderate confidence in the descriptive bridge, lower confidence in its real-world visit interpretation. A vendor reschedule contract or traceable attended-visit rule could change the result. |
| A-H4: metric/coverage or recording differences materially affect the headline | **Supported as a material unresolved measurement risk.** The date anchor changes the candidate growth rate, and the two incompatible reschedule indicators can make a separate sensitivity round to 5%. The source-to-canonical join itself has 0 unmatched candidate lines and 0 field mismatches. | Collections/results were not joined, so booked test lines have not been validated as performed tests. The primary candidate retains all status/reschedule rows. System coverage also changes: H1 2025 is legacy; H1 2026 contains 398,769 legacy and 62,311 Nova lines. The pack README documents Nova in Chennai and Jaipur beginning April 2026; this is context, not a cause. | High confidence that these definitions differ; official test volume remains unresolved. A documented dashboard rule and row-level booking/collection/result bridge would change the conclusion. |

### City and channel contribution checks

Exact source city-label changes reconcile arithmetically to +25,200 but are not all paired: `Bangalore` has 99,991 H1 2025 lines and no H1 2026 exact-label lines; `Bengaluru` has no H1 2025 exact-label lines and 107,543 in H1 2026. The other exact-label changes are Ahmedabad +8,133, Chennai +2,854, Hyderabad +5,413, Jaipur -3,671, and Pune +4,919.

The alias sensitivity is supported by the reference chain: all 31 clinic city labels match the city reference, all 568,007 canonical bookings match a clinic by exact `clinic_id`, and 84,402 booking records labelled `Bangalore` link to clinic/city-reference label `Bengaluru` (`BLR`). In H1 2025, the `Bangalore` label contributes 99,991 candidate lines; in H1 2026, `Bengaluru` contributes 107,543. With the explicit `Bangalore` → `Bengaluru` comparison mapping, the city changes are Ahmedabad +8,133, Bengaluru +7,552, Chennai +2,854, Hyderabad +5,413, Jaipur -3,671, and Pune +4,919. They sum to +25,200. This mapping is used only in sensitivity outputs; no source field was changed. The mapping is file-supported but not a formally approved effective-dated crosswalk.

On exact labels, only 30/36 2026 city/month keys match: 353,537 actual candidate lines versus 395,655 targets (-42,118; -10.6451%) for the five-city matched subset. Six `Bangalore` plan keys and six `Bengaluru` actual keys remain unmatched. Under the explicit alias sensitivity, all 36 keys match: 461,080 candidate lines versus 515,740 targets, a candidate gap of -54,660 (-10.5984% of target). The largest city shortfalls in that sensitivity are Bengaluru (-12,542), Jaipur (-10,948), and Chennai (-10,863), together 34,353 or 62.9% of the candidate gap. This is still not an official KPI plan variance until the metric and alias are approved.

The city-concentration check is **exploratory, not pre-registered**. A small group accounts for most of the net city-level increase under the alias sensitivity: the three largest positive contributions (Ahmedabad, Bengaluru, Hyderabad) sum to 21,098, or 83.7% of the net +25,200; Jaipur offsets growth by 3,671. This is descriptive and does not identify causes.

Channel values were kept as exact raw categories with system. In legacy, `clinic` changes from 286,905 to 217,656 (-69,249; -24.14%) and `home` from 148,975 to 181,113 (+32,138; +21.57%). Nova contributes 37,334 raw `CLINIC` and 24,977 `HOME` lines in H1 2026, with no H1 2025 Nova comparator. Channel groups reconcile to the overall totals, but system migration and label case differences prevent a clean channel-only interpretation; no casefold mapping was applied.

### Reproducibility, decisions, and remaining gates

The additive step is in `notebooks/05b_brief_a_driver_decomposition.ipynb` and `src/kalpa/brief_a_drivers.py`; aggregate outputs and join/identity checks are listed in `data/clean/README.md`, including the exact-label and alias-sensitivity city-plan contribution tables. The helper ran in about one minute and checked checkpoint totals, period row accounting, identity products, city/channel totals, plan-key coverage, source/canonical consistency, and zero join fan-out. The notebook JSON and code cells were parsed, but the notebook itself, full cleaning notebooks, test suite, and full-project cold run were not run. No collections/results join, cause analysis, final slide claim, or slide was produced. Raw source files and 05a artifacts remain unchanged.

The current next gates are to obtain (1) the written test-volume/dashboard definition and status/reschedule rule, (2) formal confirmation of the `Bangalore`/`Bengaluru` crosswalk for plan reporting, and (3) if “performed tests” is required, an owner-approved booking-to-collection/result rule. Preserve the current predictions and this dated measured addendum separately; do not turn the descriptive bridge into a causal statement.

## Brief A result and collection link validation — dated addendum (2026-10-24)

This validation continues from the 05b driver decomposition and uses only the approved cleaned booking, result, and collection outputs. The preceding statement that no collections/results join had been made was accurate at the 05b checkpoint; this addendum records the subsequent bounded validation. It does not change the 05a/05b candidate definition or convert the candidate into an official or completed-test KPI.

### Rules and reconciliation

- Keep the primary candidate unchanged: nonblank booking-source `test_code` rows by local `slot_at` month, all status/reschedule records retained. The source table row unit is still a booking/test entry.
- For result corroboration, use exact unchanged `booking_id + test_code`. The canonical `booking_id` is unique across system namespaces, so a system field is not available/needed on the result table for this exact link. Group result rows by the same key for a coverage check, retain the underlying rows and their counts, and do not deduplicate result runs. There are no repeated matchable nonblank result keys; nine extra rows across the full result data occur outside the nonblank-key join. The full cleaned result table contains 1,078,420 rows, including 3,211 with blank/whitespace `test_code`; none were removed.
- Result event timestamps are not used to choose the half-year: the source timestamp has no documented timezone. Each linked result is assigned only to its booking's `slot_at` cohort for this diagnostic. This is not a count of result runs occurring within H1.
- For collections, join exact `booking_id` after checking the cleaned table is unique on that key. Keep the source status as text and group candidate lines by their booking-level status; a collection row does not identify an individual test. No exact collection record is classified as unmatched, not as cancelled or not performed.
- The grouped LEFT joins record both sides' unmatched key counts. Result and collection records outside an H1 candidate cohort remain in their full cleaned source tables; their presence outside a cohort is not treated as a failed event or deleted row.

| H1 period | Candidate source rows | Candidate lines | Blank-code rows classified | Exact result-linked candidate lines | No exact result link | Result-link coverage | Candidate bookings with exact collection record | Candidate lines on raw `collected` status bookings | Candidate lines on raw `no_show` status bookings | Candidate lines with no collection record |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2025 | 436,302 | 435,880 | 422 | 351,176 | 84,704 | 80.5671% | 182,386 / 189,822 | 357,668 (82.0565%) | 61,139 (14.0266%) | 17,073 (3.9169%) |
| 2026 | 461,544 | 461,080 | 464 | 371,623 | 89,457 | 80.5984% | 187,581 / 196,474 | 378,360 (82.0595%) | 61,663 (13.3736%) | 21,057 (4.5669%) |

Source accounting is 436,302 = 435,880 candidate + 422 blank-code classified + 0 rejected in H1 2025, and 461,544 = 461,080 + 464 + 0 in H1 2026. Candidate lines reconcile to exact result-linked plus no-exact-link lines in both periods. Candidate booking records reconcile to exact collection-linked plus unmatched records; candidate lines also reconcile when weighted by each booking's collection record. The collection table is at booking/visit grain: the `collected` and `no_show` percentages above describe lines on booking records carrying those exact source labels, not test-level collection outcomes.

The exact result-linked candidate subset grows by 20,447 (+5.8224%) between these slot-date cohorts, compared with +5.7814% for the full provisional booking-line candidate. Aggregate coverage changes by only +0.0312 percentage points, but this hides system variation: H1 2026 legacy lines have 81.1753% exact result-link coverage and Nova lines have 76.9062%, while H1 2025 is all legacy at 80.5671%.

In the two mixed-system cities, exact result-link coverage is 81.0851% on legacy and 76.7681% on Nova in Chennai (Nova lower by 4.3170 percentage points); in Jaipur it is 82.1299% on legacy and 77.1786% on Nova (Nova lower by 4.9514 points). The 2026 system/city groups reconcile to the period total and retain exact source city labels. This system-linked difference strengthens the recording/coverage alternative even though aggregate coverage looks stable. It does not establish a system cause: cohorts may differ in booking composition, timing, or export behavior. Roughly 19.4% of candidate lines in each H1 period have no exact result link. Missing links do not establish that a test was not performed. The 1,349 (2025) and 1,457 (2026) result rows on candidate booking IDs whose code does not match an H1 candidate code remain outside exact test-line linkage.

### Interpretation and updated hypothesis status

- **A-H1 remains weakened as a reproduction of the reported 5%; official KPI unresolved.** The exact-result-linked subset is directionally consistent with the provisional candidate but is incomplete and uses booking-slot cohorting, not result-event dates. No dashboard rule or KPI-owner bridge was found.
- **A-H4 remains supported as a material measurement risk, with one alternative weakened.** Result-link coverage is nearly unchanged across the two H1 cohorts, which weakens differential link coverage as an explanation for the growth rate. The incomplete result linkage, booking-level collection grain, timestamp timezone gap, status/reschedule sensitivity, and unresolved official metric continue to limit interpretation.
- These are descriptive linkage checks. They do not establish causes, completed tests, or an official actual-versus-plan variance. The city alias and plan rules remain unapproved as recorded above.

### Reproduction and remaining gate

The additive validation is implemented in `notebooks/05c_brief_a_analysis_validation.ipynb` and `src/kalpa/brief_a_validation.py`. It reads only approved files in `data/clean/`, writes new `brief_a_validation_*.csv` aggregates, preserves all result rows, exports no patient-level identifiers/result values, and completed in about 38 seconds on this machine. The helper was run directly; the notebook itself, full cleaning pipeline, test suite, and full-project cold run were not run. Raw inputs and the 05a/05b artifacts remain unchanged.

The remaining Brief A gate is stakeholder confirmation of the official test-volume unit, event date, status/reschedule rule, and a row-level dashboard bridge. The data owner should also explain the lower exact result-link coverage on Nova rows in Chennai/Jaipur, while keeping system selection and recording effects as alternatives. If “performed tests” is required, the owner must define how incomplete booking/result links and booking-level collections should be handled. Do not create slide claims until those definitions are available and accepted.


## Brief A evidence package and closeout status (2026-10-24)

The six-slide Brief A package and companion evidence workbook were prepared from the already approved cleaned outputs and the measured addenda above. The slide claim is intentionally limited to the provisional booking-source line candidate; the workbook preserves period denominators, the driver product, the city-plan sensitivity and source filenames. No Brief B or E outcome work is included.

### Reproduction and validation

- The bounded helper sequence (`run_brief_a_metric_baseline`, `run_brief_a_driver_decomposition`, `run_brief_a_analysis_validation`) ran against cleaned inputs in 144.0 seconds and reproduced the stored candidate totals of 435,880 and 461,080, the +25,200 change, zero join fan-out, zero missing-identity lines, and the 36-key alias comparison sensitivity. The sequence invokes the baseline helper and re-emits its aggregate CSVs with the same verified values; the baseline notebook and helper were not edited.
- The 05b driver helper and 05c validation helper report approximately 66.7 seconds and 48.9 seconds respectively, including input reads and output writes. This runtime is from the current environment, not a fresh Codespace.
- The project test suite was run after aligning model tests with the documented preserve-source-values contract: 10 tests passed. The first test run had two stale expectations that assumed normalization/eligibility rules not implemented or supported by the project contract; those expectations were replaced with preservation-focused checks.
- `nbconvert --execute` did not finish in the attempted notebook run and was interrupted before producing an executed notebook. The equivalent bounded Python helper chain completed successfully. The full raw-to-clean Codespace cold run was not performed.

### Reporting boundary and remaining sign-off

The candidate growth rate is +5.7814% by local `slot_at` month, while the created-date sensitivity is +4.3062%. The H1 plan total of 515,740 is 18.32% above the H1 2025 candidate total, but the supplied 18% plan claim's official denominator is unverified. The exact-label comparison has 30/36 matched city/month keys; the evidence-supported but not formally approved `Bangalore` → `Bengaluru` comparison sensitivity has 36/36 and a gap of -54,660 (-10.5984% of target). These are candidate comparisons, not approved official KPI/plan variances.

The result-linked coverage is 351,176/435,880 (80.5671%) for H1 2025 and 371,623/461,080 (80.5984%) for H1 2026. This is an exact-link diagnostic; missing result links do not establish that a test was not performed. Collections are booking-level and are not treated as test-level evidence. The slide action is a measurement/sign-off gate, not a causal explanation or reallocation recommendation.

Before official reporting or resource changes, obtain: (1) the KPI owner's written test-volume unit, event date, denominator, and status/reschedule rule plus a dashboard-to-row bridge; (2) Finance/city-reference owner's approval of an effective-dated `Bangalore`/`Bengaluru` crosswalk for plan reporting; and (3) if the decision requires performed tests, an owner-approved outcome bridge with result/collection timestamp and missing-link rules. Record the instructor's clarification date and exact scope for AI assistance (code, analysis, slides, write-ups); the team reports permission, but the project statement and AI-log boilerplate still contain restrictive wording.

The final review artifacts are the six-page `slides/Brief_A_Growth_6slides.pdf`, its editable six-slide `slides/Brief_A_Growth_6slides.pptx`, and the four-tab workbook `outputs/brief-a-growth-final-2026-10-24/Brief_A_Evidence.xlsx`. PDF page count, PPTX package integrity, six-slide/one-chart structure, workbook readability, formulas, summary counts, and corrected exact-label key status were checked. The workbook contains Summary, Drivers, City plan, and Linkage tabs. These deliverables package descriptive evidence; they do not resolve the sign-off gates above. The earlier workbook export in `outputs/brief-a-growth-closeout-2026-10-24/` is superseded by the final path just named.

## Brief A selected IITGN-aligned recalculation — dated addendum (2026-10-24)

At the user's direction, the current Brief A calculation now follows the implementation in `iitgn-build1`: count `n_tests` in the existing validated `bookings_clean.csv.gz` after `status_at_export = rescheduled` originals are removed. Assign rows by source-local `slot_at` date, using full H1 periods `[Jan 1, Jul 1)`. This redefinition supersedes the prior 05a source-line candidate as the current comparison base; prior outputs remain preserved as historical sensitivity.

The recalculated totals are 433,611 for H1 2025 and 455,383 for H1 2026, a difference of +21,772 (+5.0211%). The IITGN pre-outcome prediction in its project statement expected growth to combine person volume, visits per person, and tests per visit. Its descriptive fingerprint appears: `person_id` +3.7677%, visits/person -0.9680%, tests/visit +2.1972%; their product reproduces test lines in both periods and their log changes sum exactly to total log growth. This supports the prediction as an accounting description, not a causal explanation. `person_id` is a phone/name/DOB proxy and `booking_id` is an unverified attended-visit proxy.

The baseline reconciliation is 435,880 raw nonblank test-code lines less 2,269 validation-rejected lines = 433,611 retained lines in H1 2025; in H1 2026, 461,080 less 2,156 validation-rejected lines and 3,541 lines on 1,499 superseded bookings = 455,383. A 21-row/booking-key difference between the Kalpa source-row copy and IITGN flattened copy consists entirely of blank-code-only keys; nonblank line counts match in both periods.

The clean H1 2026 actual is 455,383 against the 515,740 target, a candidate gap of -60,357 (-11.7030% of target), with the explicit IITGN `Bangalore` → `Bengaluru` comparison mapping. Exact labels match 30/36 city-month keys; the alias comparison matches 36/36. The same target sum implies +18.9407% over the H1 2025 IITGN-aligned actual; actual growth is 13.9196 percentage points below that implied rate. Keep the YoY rate and target variance separate. The city crosswalk and the target's official denominator still need owner confirmation.

Notebook `notebooks/05d_brief_a_iitgn_alignment.ipynb`, helper `src/kalpa/brief_a_iitgn_alignment.py`, and `data/clean/brief_a_iitgn_*.csv` outputs contain the focused calculation and row/join audits. The helper completed in about 29 seconds; the raw-to-clean pipeline, notebook-kernel execution, test suite, and full Codespace cold run were not run. The cold-run notebook's “collected or no-show” label has no corresponding filter in its code, so the selected count is not represented as performed tests. The prior six-slide deck and evidence workbook still show the earlier candidate and are historical until refreshed from this recalculation.
