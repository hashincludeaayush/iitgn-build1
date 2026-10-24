# Brief A: IITGN-aligned recalculation

**Updated:** 2026-10-24  
**Status:** Working descriptive result selected by the team for Brief A. This is not an owner-confirmed official KPI.

## Takeaway

H1 2026 has **455,383** validated booking test lines versus **433,611** in H1 2025, so the increase is **5.02%**. The tree says this came from more people and more test lines per visit, partly offset by slightly fewer visits per person. This is a descriptive result, not a causal or clinical conclusion.

## Selected measure

Use the existing IITGN Build 1 `bookings_clean.csv.gz` table. Count `n_tests` for each retained booking record and assign the record to the H1 containing its source-local `slot_at` date. Use the half-open periods `[2025-01-01, 2025-07-01)` and `[2026-01-01, 2026-07-01)`, including all of June 30.

IITGN notebook 03 validates booking IDs and test lines, rejects invalid booking records, and removes records whose `status_at_export` equals `rescheduled` as superseded originals. `n_tests` is the number of validated nested test lines on a booking. The final denominator does not filter on the collection `status`; booked and missing-collection records remain. Notebook 06 describes the unit as bookings “collected or no-show,” but its code applies no such filter. This analysis follows the implemented cleaning path and labels the result **validated booking test lines after IITGN validation and superseded-record removal**. It does not call them attended, collected, or performed tests.

The IITGN pre-outcome prediction in `docs/project-statement.md`, dated 2026-10-23, says the change will combine patient volume, visit frequency, and tests per visit rather than come from one driver. This remains a prediction tested below.

## Revised H1 values and driver identity

| Measure | H1 2025 | H1 2026 | Change | Percent change |
|---|---:|---:|---:|---:|
| Validated booking test lines, `sum(n_tests)` | 433,611 | 455,383 | +21,772 | +5.0211% |
| Distinct `person_id` values | 94,275 | 97,827 | +3,552 | +3.7677% |
| Distinct `booking_id` values, visit proxy | 188,803 | 194,020 | +5,217 | +2.7632% |
| Visits per person, bookings / `person_id` | 2.0027 | 1.9833 | -0.0194 | -0.9680% |
| Test lines per visit, `sum(n_tests)` / bookings | 2.2966 | 2.3471 | +0.0505 | +2.1972% |

The product identity reconciles in each half-year:

`distinct person_id × visits per person × test lines per visit = test lines`

The exact product is 433,611 in H1 2025 and 455,383 in H1 2026, with zero difference from `sum(n_tests)`. The IITGN notebook's log decomposition also reconciles: person growth contributes +3.6985 log-percent, visits per person -0.9727, and tests per visit +2.1734, summing to total log growth of +4.8991. Log growth is not the simple percent growth, which is +5.0211%.

`person_id` comes from the IITGN patient map, which groups normalized phone, normalized name, and date of birth. It is an analytical person proxy, not a verified clinical identity; placeholder DOBs limit certainty. Visits use distinct, unchanged `booking_id` values after the superseded-record rule. The booking table has one row per ID. A booking remains a visit proxy because the exports do not prove attendance.

## Source-to-IITGN reconciliation

| Period | Nonblank raw test-code lines | Validation-rejected test lines | Superseded test lines removed | Retained test lines |
|---|---:|---:|---:|---:|
| H1 2025 | 435,880 | 2,269 | 0 | 433,611 |
| H1 2026 | 461,080 | 2,156 | 3,541 | 455,383 |

The source-line counts reproduce the stored 05a checkpoint exactly. H1 2026 removes 1,499 superseded booking records carrying 3,541 test lines. The raw-to-clean reduction is a definition and validation effect; it is not evidence that tests or patients disappeared in the business.

The Kalpa source-row table has 21 more H1 2026 rows/booking keys than the IITGN flattened input (461,544 vs 461,523). All 21 are blank-code-only; both inputs contain exactly 461,080 nonblank test-code lines. The difference does not affect the selected line count or retained IITGN bookings. Keep it disclosed as a source-copy completeness difference.

For the `Bangalore` → `Bengaluru` lineage check, exact `system + booking_id` matches connect 557,994 of 563,380 IITGN clean bookings to the Kalpa source rows; 5,386 do not match exactly. IITGN's `Booking` model applies `str_strip_whitespace=True`. Applying that documented rule only to the audit join matches all 563,380, with zero normalized ID collisions. The helper did not rewrite IDs in either source. It found 12,559 source rows and 5,409 distinct source IDs with outer whitespace. Of the retained rows, 83,921 booking records (192,317 test lines) have source city `Bangalore` and IITGN city `Bengaluru`; this is the explicit city rule in IITGN `models.py` and it matches the Kalpa clinic/city-reference evidence. In H1 2025 it changes 43,483 booking records / 99,438 test lines. H1 2026 source labels already say `Bengaluru`.

## City contribution to year-over-year growth

The IITGN city normalization is applied for this table; all city totals reconcile to the overall H1 totals.

| City | H1 2025 lines | H1 2026 lines | Change | Change % | Share of net change |
|---|---:|---:|---:|---:|---:|
| Ahmedabad | 76,480 | 84,523 | +8,043 | +10.52% | 36.94% |
| Bengaluru | 99,438 | 106,973 | +7,535 | +7.58% | 34.61% |
| Hyderabad | 72,828 | 78,131 | +5,303 | +7.28% | 24.36% |
| Pune | 60,225 | 65,141 | +4,916 | +8.16% | 22.58% |
| Chennai | 79,762 | 80,502 | +740 | +0.93% | 3.40% |
| Jaipur | 44,878 | 40,113 | -4,765 | -10.62% | -21.89% |
| **Total** | **433,611** | **455,383** | **+21,772** | **+5.02%** | **100.00%** |

The three largest positive city changes (Ahmedabad, Bengaluru, Hyderabad) sum to +20,881 lines, 95.91% of the net increase. Jaipur offsets some of that growth. This describes where the net change appears; it does not identify a cause.

## Plan comparison, kept separate from year-over-year growth

The six-city 2026 plan totals 515,740. Against the H1 2025 IITGN-aligned actual of 433,611, that plan implies +18.9407% growth. The actual +5.0211% growth is 13.9196 percentage points below that implied rate. This calculation treats the plan total as comparable and is still a diagnostic, not proof of the official “18%” baseline.

For actual-versus-plan, H1 2026 actual is 455,383 against 515,740 target: **-60,357 lines, -11.7030% of target, 88.2970% attainment**. These figures use the explicit IITGN city normalization to map the plan's `Bangalore` label to `Bengaluru`.

Without the alias, only 30/36 city-month keys match. Those five exact-label cities have 348,410 actual lines against 395,655 targets, a partial gap of -47,245 (-11.9410%). Six `Bengaluru` actual keys (106,973 lines) and six `Bangalore` plan keys (120,085 target lines) remain unmatched. With the declared IITGN mapping, all 36 keys match. Formal approval of the city crosswalk and plan measure is still needed before treating this as an official plan variance.

The largest mapped plan shortfalls are Chennai (-13,410), Bengaluru (-13,112), and Jaipur (-12,259). Together these are -38,781, 64.25% of the total target gap.

## Channel and hypothesis result

Channel categories reconcile only when shown with system. Legacy clinic lines change by -68,951, legacy home by +31,953, Nova clinic contributes 35,212 in H1 2026, and Nova home contributes 23,558. Nova has no H1 2025 comparison. The change in system mix prevents a channel-only causal interpretation.

**Prediction tested:** test-volume change will combine patient volume, visit frequency, and tests per visit rather than come from one driver.  
**Status:** supported descriptively. The factors change by +3.7677%, -0.9680%, and +2.1972%, respectively, and their product/log identity reconciles to the total. This supports the stated decomposition pattern, not a causal explanation. The prediction did not define a threshold for “material.”

**Evidence that limits the interpretation:** the patient identity is constructed, booking IDs are visit proxies, and test lines are not verified as performed tests. The migration mix, rejection rules, reschedule handling, result/collection coverage, or a different KPI definition could change the business interpretation. An owner-confirmed dashboard definition and a row-level bridge could change the selected measure.

## Date-boundary and other cautions

The existing IITGN notebooks use `.between("YYYY-01-01", "YYYY-06-30")` on timestamps. That includes June 30 only at midnight. It returns 431,261 / 452,933 test lines and +5.0253%. The corrected full-calendar counts above include 2,350 H1 2025 and 2,450 H1 2026 test lines scheduled on June 30 after midnight. Both rates round to 5.0% at one decimal, but the corrected half-open periods are the selected method.

The computed result is a reproduction of the IITGN cleaning rule, not confirmation of the official 5% KPI. The status wording in notebook 06 is unsupported by its code. The `18%` plan statement also remains unverified against an owner-specified denominator. No descriptive decomposition here establishes why growth occurred or what action would cause an improvement.

## Reproduction

Run notebook `notebooks/05d_brief_a_iitgn_alignment.ipynb` from a fresh kernel after the existing clean tables and plan output are present. It calls `src/kalpa/brief_a_iitgn_alignment.py`, which reads the IITGN intermediate/clean booking tables, the Kalpa source-row table for source city lineage, the stored 05a baseline, and the cleaned plan. The bounded helper completed in about 29 seconds in this environment. It did not run the full cleaning pipeline, notebook kernel execution, test suite, or full Codespace cold run. No raw source files were modified.

Aggregate outputs are `data/clean/brief_a_iitgn_*.csv`. Earlier 05a–05c files and the earlier slide/workbook package remain preserved as historical outputs; they use the prior nonblank booking-source test-code-line definition and must not be cited as the current IITGN-aligned result.
