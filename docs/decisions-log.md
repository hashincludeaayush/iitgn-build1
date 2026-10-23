# Decisions log · cleaning and reconciliation · Brief <LETTER> · Group <N>

Every act of cleaning is a decision with a reason and an effect. Input equals clean plus rejected, every time. The headline number is recomputed after every decision so the bridge from raw to final is visible.

## Reconciliation

| Step | Table | Rows in | Rows kept | Rows rejected | In = kept + rejected? | Headline number after this step | Owner | Date |
|---|---|---|---|---|---|---|---|---|
| 0 | raw as received | | | | | | | |
| 1 | | | | | | | | |
| 2 | booking validation | 567,986 | 564,879 | 3,107 | yes | 564,879 valid bookings from the current full-data run | Group 6 | 2026-10-23 |

## Decisions

| # | Table | What we found | Decision (drop / default / keep and flag / map / split) | Reason | Rows affected | Effect on the headline | Reversible? | Owner |
|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | |
| 2 | bookings | 3,107 records failed model, booking-id or test-code validation. | drop from valid analysis; keep in rejects_bookings.csv | They do not satisfy the agreed data contract and cannot be safely repaired without source-system evidence. | 3,107 bookings | Valid booking headline is 567,986 -> 564,879; rejected records are excluded from valid counts. | yes, by reviewing the rejects and source contract | Group 6 (2026-10-23) |
| 3 | profiling | The current pack's representative files show different grains: bookings and results have multiple rows per booking, while invoices, payment IDs and patient IDs are unique in the profiled files. | keep raw files unchanged; use the profiled grain to choose later counts and joins | A row count is meaningful only at the correct grain. Notebook 02 and notebook 03 will validate the full pack before analysis. | representative files | No headline change; prevents later overcounting and incorrect join assumptions. | yes | Group 6 (2026-10-23) |

## Joins

| # | Left table (rows) | Right table (rows) | Key | Type | Rows after | Keys matched more than once | Explanation of the change in count | Owner |
|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | |

## Cold runs

| Date | Who ran it | Fresh Codespace? | Runtime | Headline number | Same as last run? | If not, why |
|---|---|---|---|---|---|---|
| | | | | | | |
