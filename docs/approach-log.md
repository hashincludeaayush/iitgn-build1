# Approach log · Brief <LETTER> · Group <N>

One row per part of the work. At least two approaches in every row. Written when the choice is made, not afterwards; the commit timestamp is the proof. An approach you tried for twenty minutes and abandoned is the best kind of row. Keep the dead notebook cell and link to it.

The panel reads this file before it reads your notebooks. A panellist will cover the "chosen" column and ask you to choose again, aloud.

| # | Part of the work | Approaches considered (two at least) | Chosen | Why this, and not the others | What would have changed the choice | What happened when we tried it | Owner | Date |
|---|---|---|---|---|---|---|---|---|
| 0 | *Example: matching invoice ids to payment references* | *(a) Strip the prefix and match on digits. (b) Match on amount and date within two days. (c) Both, and keep the rows where they disagree.* | *(c)* | *(a) alone matched 91 percent and silently paired two invoices with one payment. (b) alone could not separate same-day same-amount visits. Together they flag what each misses.* | *A shared id in both feeds would have made (a) enough.* | *96 percent matched. The 4 percent became finance's list.* | *example* | *example* |
| 1 | Which table to count tests from | | | | | | | |
| 2 | How to define the period (first half, both years) | | | | | | | |
| 3 | Profiling: what to check in each table | | | | | | | |
| 4 | Duplicates: the identity rule | | | | | | | |
| 5 | Missing values: drop, default, or keep and flag | | | | | | | |
| 6 | Each join: type, key, validation | | | | | | | |
| 7 | The method (tree / ladder / bridge / shuffle / comparison) | | | | | | | |
| 8 | The segmentation (city, channel, type) | | | | | | | |
| 9 | The chart that carries the claim | | | | | | | |
| 10 | The one sentence | | | | | | | |
| 11 | Handling profiling anomalies before cleaning | (a) Change validation rules immediately so every check passes. (b) Delete or repair rows that do not match the expected pattern. (c) Measure and preserve anomalies, verify whether data files match the manifest, then decide the rule from the source-system contract. | (c) | Immediate rule changes or repairs could hide a real source-system issue and make the analysis irreproducible. The profile showed that the data files sampled matched the manifest while the README did not, and that the 29 Bengaluru rows differed only in suffix length; both findings need to remain auditable. | A confirmed vendor specification allowing seven-digit Bengaluru IDs would justify updating the validation pattern; an official regenerated manifest would resolve the README mismatch. | The profiling notebook wrote both profiling CSVs, found 4 of 6 checks passed, and preserved the two issues for validation and cleaning rather than silently changing the raw data. | Group 6 | 2026-10-23 |
| 12 | Loading booking files | (a) Load sequentially. (b) Use a process pool. | (b) for the full pack, while measuring both | CSV/JSON parsing and gzip decompression are CPU-heavy; processes can run independently. The small sample was slower in parallel because worker startup dominated, but both methods returned the same rows. | A much smaller file pack or predominantly I/O-bound work would favor sequential loading or threads. | Sequential 0.3s versus process pool 1.7s for the 12-file comparison; same rows: True. | Group 6 | 2026-10-23 |
| 13 | Choosing the booking grain | (a) Count raw booking-test rows. (b) Count unique booking IDs for visits and retain booking-test rows for test-level work. | (b) | A booking can contain multiple tests, so raw rows overcount visits. The combined data had 58,362 booking-test rows but 25,069 distinct bookings. | If every source guaranteed one row per booking, row count would be sufficient; it does not here. | Created booking-test `bookings_all` and booking-level `bookings` outputs. | Group 6 | 2026-10-23 |
| 14 | Validating booking records | (a) Use field-by-field vectorized checks only. (b) Validate each grouped booking with the Pydantic contract, then use DataFrames afterward. | (b) | The model validates fields and cross-field rules together and preserves rejection reasons. It costs Python-level runtime, so it is used once at the boundary. | A performance-critical repeat validation after the boundary would favor vectorized checks. | 25,069 input bookings reconciled to 24,993 accepted and 76 rejected. | Group 6 | 2026-10-23 |
| 15 | Handling rejected bookings | (a) Repair or include records to maximize counts. (b) Exclude all 76 from valid analysis and preserve them with reasons. | (b) | The records do not satisfy the current contract, and repairing IDs or test codes would require guessing. Keeping the rejects preserves auditability and prevents invalid records from affecting objectives A, B or C. | Source-system documentation proving a rejected format is valid would justify a later contract change and re-run. | `rejects_bookings.csv` contains the rejected records; valid booking output contains 24,993 unique bookings. | Group 6 | 2026-10-23 |
| 16 | Reproducible validation | (a) Accept whatever count appears in one run. (b) Sort inputs, use fixed validation rules and reconcile input with accepted plus rejected. | (b) | A fresh teammate should get the same result from the same raw files and code. Deterministic ordering and reconciliation make changes visible. | Changed raw files, package versions or validation rules would require a documented re-run. | Final checks passed: unique booking IDs and at least one test per accepted booking. | Group 6 | 2026-10-23 |

## Parts we never had to choose about

<List any part where only one approach was possible, and say why. The panel will ask whether that was true.>
