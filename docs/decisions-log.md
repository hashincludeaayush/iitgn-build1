# Decisions log · cleaning and reconciliation · Brief <LETTER> · Group <N>

Every act of cleaning is a decision with a reason and an effect. Input equals clean plus rejected, every time. The headline number is recomputed after every decision so the bridge from raw to final is visible.

## Reconciliation

| Step | Table | Rows in | Rows kept | Rows rejected | In = kept + rejected? | Headline number after this step | Owner | Date |
|---|---|---|---|---|---|---|---|---|
| 0 | raw as received | | | | | | | |
| 1 | | | | | | | | |
| 2 | booking validation | 25,069 | 24,993 | 76 | yes | 24,993 valid bookings; 58,362 booking-test rows were grouped into 25,069 booking records | Group 6 | 2026-10-23 |

## Decisions

| # | Table | What we found | Decision (drop / default / keep and flag / map / split) | Reason | Rows affected | Effect on the headline | Reversible? | Owner |
|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | |
| 2 | bookings | 76 records failed model, booking-id or test-code validation. | drop from valid analysis; keep in rejects_bookings.csv | They do not satisfy the agreed data contract and cannot be safely repaired without source-system evidence. | 76 bookings | Valid booking headline is 25,069 -> 24,993; rejected records are excluded from valid counts. | yes, by reviewing the rejects and source contract | Group 6 (2026-10-23) |
| 3 | bookings | Nova contains 500 records marked as reschedules. | keep until the visit identity rule is applied in notebook 03 | Loading and validation must be separated from the later business decision about superseded visits. | 500 bookings | No change yet; notebook 03 will decide the comparable visit count. | yes | Group 6 (2026-10-23) |

## Joins

| # | Left table (rows) | Right table (rows) | Key | Type | Rows after | Keys matched more than once | Explanation of the change in count | Owner |
|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | |

## Cold runs

| Date | Who ran it | Fresh Codespace? | Runtime | Headline number | Same as last run? | If not, why |
|---|---|---|---|---|---|---|
| | | | | | | |
