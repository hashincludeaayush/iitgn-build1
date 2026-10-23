# Decisions log · cleaning and reconciliation · Brief <LETTER> · Group <N>

Every act of cleaning is a decision with a reason and an effect. Input equals clean plus rejected, every time. The headline number is recomputed after every decision so the bridge from raw to final is visible.

## Reconciliation

| Step | Table | Rows in | Rows kept | Rows rejected | In = kept + rejected? | Headline number after this step | Owner | Date |
|---|---|---|---|---|---|---|---|---|
| 0 | raw as received | | | | | | | |
| 1 | | | | | | | | |
| 2 | booking validation | 567,986 | 564,879 | 3,107 | yes | 564,879 valid bookings from the current full-data run | Group 6 | 2026-10-23 |
| 3 | superseded booking removal | 564,879 | 563,380 | 1,499 | yes | 563,380 comparable bookings; 1,303,719 tests after removing superseded Nova originals | Group 6 | 2026-10-24 |
| 4 | collection deduplication | 552,492 | 549,598 | 2,894 | yes | 549,598 unique collection events retained | Group 6 | 2026-10-24 |
| 5 | patient deduplication | 309,217 | 303,153 | 6,064 | yes | 303,153 analytical people retained; every booking patient ID mapped | Group 6 | 2026-10-24 |

## Decisions

| # | Table | What we found | Decision (drop / default / keep and flag / map / split) | Reason | Rows affected | Effect on the headline | Reversible? | Owner |
|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | |
| 2 | bookings | 3,107 records failed model, booking-id or test-code validation. | drop from valid analysis; keep in rejects_bookings.csv | They do not satisfy the agreed data contract and cannot be safely repaired without source-system evidence. | 3,107 bookings | Valid booking headline is 567,986 -> 564,879; rejected records are excluded from valid counts. | yes, by reviewing the rejects and source contract | Group 6 (2026-10-23) |
| 3 | profiling | The current pack's representative files show different grains: bookings and results have multiple rows per booking, while invoices, payment IDs and patient IDs are unique in the profiled files. | keep raw files unchanged; use the profiled grain to choose later counts and joins | A row count is meaningful only at the correct grain. Notebook 02 and notebook 03 will validate the full pack before analysis. | representative files | No headline change; prevents later overcounting and incorrect join assumptions. | yes | Group 6 (2026-10-23) |
| 4 | bookings | Nova marks the original booking as rescheduled and creates a replacement booking. | drop superseded originals; keep the replacement | One rescheduled visit must count once so Legacy and Nova are comparable. | 1,499 bookings | 564,879 -> 563,380 bookings; tests 1,307,260 -> 1,303,719. | yes | Group 6 (2026-10-24) |
| 5 | collections | Exact repeated collection rows existed for the same booking, status and timestamp. | remove exact duplicates and require one collection row per booking | Prevents collection joins from multiplying booking rows. | 2,894 rows | 552,492 -> 549,598 collection rows. | yes | Group 6 (2026-10-24) |
| 6 | bookings + collections | 18,269 bookings were `left_only` after the left join; 545,111 matched and no right-only collection rows existed. | keep the bookings and label missing status `cancelled_or_missing`; flag for interpretation | `left_only` does not prove cancellation; it can also indicate a future booking, missing event or ID issue. | 18,269 bookings | Booking row count remains 563,380; no join fan-out. | yes | Group 6 (2026-10-24) |
| 7 | bookings + collections | No collection timestamp was more than one day before its booking slot. | keep timestamps; retain a clock-skew flag with zero positives | No timing anomaly met the defined threshold. | 0 rows | No headline change. | yes | Group 6 (2026-10-24) |
| 8 | patients | 309,217 rows mapped to 303,153 people using normalized phone, name and DOB; 1,492 rows used placeholder DOB `1900-01-01`. | deduplicate for aggregate analysis; disclose placeholder-DOB limitation | The rule supports person-level counting but is not definitive identity verification for clinical communication. | 6,064 duplicate rows | 309,217 -> 303,153 analytical people; all booking patient IDs mapped. | yes | Group 6 (2026-10-24) |
| 9 | invoices + payments | 470,776 invoices totalled Rs 737,020,069; payments included 455,469 captured and 18,038 failed rows. | normalize amounts and reconcile captured payments by normalized invoice reference | Invoice amounts were text and payment amounts were paise; units and references must be normalized before reconciliation. | 473,507 payment rows | 450,881 invoice/payment matches; 21,820 invoice-only and 4,588 payment-only rows. | yes | Group 6 (2026-10-24) |
| 10 | captured payments | 1,925 invoices had more than one captured payment. | aggregate or investigate at invoice level; do not count payment rows as invoices | Multiple captures may be retries, partial payments or duplicate events. | 1,925 invoices | Preserves completed finance data-quality groundwork, although invoice/payment reconciliation is no longer a selected headline objective. | yes | Group 6 (2026-10-24) |

## Joins

| # | Left table (rows) | Right table (rows) | Key | Type | Rows after | Keys matched more than once | Explanation of the change in count | Owner |
|---|---|---|---|---|---|---|---|---|
| 1 | bookings (563,380) | collections (549,598) | booking_id | left, one-to-one validated | 563,380 | 0 | 545,111 matched; 18,269 left_only; no fan-out and no right_only rows | Group 6 (2026-10-24) |
| 2 | invoices (470,776) | captured payments | invoice_id | outer, one-to-many validated | 477,289 relationship rows | 1,925 invoice IDs have multiple captured payments | 450,881 both; 21,820 invoice-only; 4,588 payment-only | Group 6 (2026-10-24) |

## Cold runs

| Date | Who ran it | Fresh Codespace? | Runtime | Headline number | Same as last run? | If not, why |
|---|---|---|---|---|---|---|
| | | | | | | |
