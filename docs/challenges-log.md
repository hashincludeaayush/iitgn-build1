# Challenges log · Brief <LETTER> · Group <N>

What broke or surprised us, what we tried, what we changed and why. Entries are dated and written as they happen. A log written on the last evening answers no interview question, and the commit history shows which kind this is.

| # | Phase | What broke or surprised us | What we tried first | What we changed, and why | What we would do differently next time | Who | Date |
|---|---|---|---|---|---|---|---|
| 0 | *Profile and clean* | *Our first join of invoices to payments returned almost no matches.* | *Printed ten ids from each file side by side.* | *Wrote a mapping rule from invoice id to payment reference; kept unmappable rows in a separate list.* | *Profile id formats before writing any join.* | *example* | *example* |
| 1 | | | | | | | |
| 2 | Profile | The manifest hash check failed for `README.md`, and 29 Bengaluru legacy booking-test rows had seven-digit booking-id suffixes although the current validation pattern expects six. | Recomputed the sampled SHA-256 values and inspected the invalid booking IDs after stripping whitespace. | Confirmed that the sampled data files matched their manifest hashes, treated the README mismatch as a documentation-pack issue, and carried the booking-ID anomaly forward without silently repairing or deleting it. | Confirm the source-system ID contract and regenerate the manifest whenever the raw pack is published. | Group 6 | 2026-10-23 |
| 3 | Load and validate | Notebook 2 loaded 58,362 booking-test rows into 25,069 booking records, and 76 records failed validation. The process pool was slower than sequential loading on the small sample. | Compared sequential and process-pool loading, inspected the schema differences, grouped rows by booking ID, and reviewed the rejection reasons. | Kept the process-pool loader for the larger pack because it returned the same rows and targets CPU-heavy parsing; excluded all 76 rejected records from valid analysis and preserved them in `rejects_bookings.csv`. | Benchmark on the full pack before optimizing worker count, and confirm source-system formats before changing validation rules. | 25,069 = 24,993 accepted + 76 rejected; final booking-grain uniqueness and minimum-test checks passed. | Group 6 | 2026-10-23 |

## The entry we are proudest of

<One paragraph on the problem that taught the group the most. This is the story each of you tells in the viva.>
