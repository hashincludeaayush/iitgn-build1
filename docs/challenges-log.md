# Challenges log · Brief <LETTER> · Group <N>

What broke or surprised us, what we tried, what we changed and why. Entries are dated and written as they happen. A log written on the last evening answers no interview question, and the commit history shows which kind this is.

| # | Phase | What broke or surprised us | What we tried first | What we changed, and why | What we would do differently next time | Who | Date |
|---|---|---|---|---|---|---|---|
| 0 | *Profile and clean* | *Our first join of invoices to payments returned almost no matches.* | *Printed ten ids from each file side by side.* | *Wrote a mapping rule from invoice id to payment reference; kept unmappable rows in a separate list.* | *Profile id formats before writing any join.* | *example* | *example* |
| 1 | | | | | | | |
| 2 | Profile | Notebook 01 profiled the current full data pack through its largest representative file per source family. The structural grains differ: bookings and results have multiple rows per booking, collections are near one row per booking, and invoices, payment IDs and patient IDs are unique in the profiled files. | Compared rows per key and distinct-key counts across bookings, collections, results, invoices, payments and patients. | Recorded the results as representative structural evidence and used notebook 02 for full booking ingestion and validation rather than treating notebook-01 counts as full-pack totals. | Profile every file if any family shows inconsistent schemas, date ranges or ID rules. | Representative counts: legacy bookings 19,602 rows/8,344 bookings; Nova 13,966/5,903; collections 8,161/8,120; results 16,310/7,084; invoices 83,630; payments 28,758; patients 309,217. | Group 6 | 2026-10-23 |
| 3 | Load and validate | Notebook 02 validated 567,986 booking records and rejected 3,107 under the current model, booking-ID and test-code contract. | Grouped booking-test rows by booking ID, applied the Pydantic validation boundary, and reviewed the reconciliation output. | Excluded all 3,107 rejected bookings from valid analysis and preserved them with reasons in `rejects_bookings.csv`; retained the accepted output for notebook 03. | Review the rejection categories against source-system documentation before changing any validation rule. | Passed reconciliation: 567,986 = 564,879 accepted + 3,107 rejected. | Group 6 | 2026-10-23 |

## The entry we are proudest of

<One paragraph on the problem that taught the group the most. This is the story each of you tells in the viva.>
