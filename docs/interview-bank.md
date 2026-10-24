# Interview bank: the questions this project earns you the right to answer

Each question is tied to the place in the kit where you did the thing. Answer in under a minute, at level three (the number or the mechanism, what moved it, how sure you are). Tags are this programme's own calibration for 0 to 3 year Indian-market roles: [S] staple asked everywhere, [F] frequent in GCC and product screens, [SV] service-major screen opener, [D] differentiator.

## pandas

| Tag | Question | Where you did it | What a good answer covers |
|---|---|---|---|
| [S] | What does `merge(how='left', validate='one_to_one', indicator=True)` do, and why would you set all three? | 03 | LEFT keeps every left row; validate raises on a cardinality violation instead of fanning out silently; indicator shows which side each row came from, which is the anti-join check. |
| [S] | Your join grew the row count. What happened and how do you find out? | 03, checks.join_did_not_fan_out | The right key repeats. Group the right side by key and count; separate retries, true duplicates and a wrong key. |
| [F] | When is `category` the right dtype, and when is it the wrong one? | 01, loaders.LEGACY_DTYPES | Low-cardinality columns: memory and groupby speed. Wrong for ids, and a trap on concat with different category sets. |
| [F] | `groupby().apply()` was slow. What did you do instead? | 02, records_from_rows | Sort once, find group boundaries with `np.unique(return_index=True)`, slice; or use named aggregations and vectorised string ops. Measure before and after. |
| [F] | How do you read a CSV too large for memory? | loaders.iter_chunks | `chunksize`, aggregate per chunk, or filter columns with `usecols` and declare dtypes; or load into the database and query. |
| [D] | Explain `observed=True` in a groupby on categoricals. | 05 | Without it pandas emits every category combination, including empty ones, which pads results and slows the aggregation. |
| [S] | Mean or median for order value, and why? | Week 1 | A single bulk order drags the mean; the median describes the typical visit. Report both when they disagree, and say why. |
| [D] | What is the difference between `NaN`, `None`, `pd.NA` and `NaT`, and when did it bite you? | 02, 03 | Float NaN, Python None, the nullable-dtype missing marker, and the datetime missing marker; equality tests fail on all of them, so use `isna()`. |

## NumPy

| Tag | Question | Where you did it | What a good answer covers |
|---|---|---|---|
| [F] | What is broadcasting, with an example from your work? | 05 | Arithmetic between arrays of compatible shapes without copying: `tests_per_visit = tests / visits` across a column, or subtracting the network rate from a vector of clinic rates. |
| [F] | How did you run thousands of shuffles without a Python loop? | 05, shuffle_reference | Recognised the statistic as a count of a binary outcome in one group, so the shuffled distribution is hypergeometric; one vectorised draw. Kept the loop version to show they agree. |
| [D] | Why is the log decomposition of growth exact when the percentage one is not? | 05, tree | log(a·b·c) = log a + log b + log c, so growth in a product is the sum of log growths; percentages only add approximately for small changes. |
| [S] | What does setting a seed buy you, and what does it not? | every notebook, CONFIG | Reproducible random draws for the same code and library version; it does not make the analysis correct, and a different NumPy version can change the stream. |

## Pydantic and Python

| Tag | Question | Where you did it | What a good answer covers |
|---|---|---|---|
| [F] | What does a pydantic model give you that a DataFrame check does not? | models.Booking | One named contract per record, reused by the loader, the tests and the database; per-field reasons on rejection; normalisation that is explicit. Cost: per-record Python time, so run it once at the boundary. |
| [F] | `field_validator` against `model_validator`: when each? | models.Booking | Field: one value in isolation (an id shape, a case fold). Model: a rule across fields (slot not before creation). |
| [S] | Why a process pool rather than threads for parsing files? | loaders.read_many | CPU-bound work under the interpreter lock runs one thread at a time; processes have their own interpreter. Threads for I/O waits. |
| [F] | What is a generator and where did you use one? | records_from_rows, iter_chunks | A function that yields items lazily, so a million records are never all in memory at once. |
| [D] | What does `with pd.read_csv(..., chunksize=...) as reader` do that a plain call does not? | loaders.iter_chunks | The context manager closes the file handle when the loop ends or raises. |
| [D] | How did you make a notebook idempotent? | 03, 06 | Reads only from raw and clean, writes clean with overwrite, no in-place mutation of inputs, no state carried between runs; the cold run proves it. |

## SQL

| Tag | Question | Where you did it | What a good answer covers |
|---|---|---|---|
| [S] | Logical order of a SELECT with GROUP BY and HAVING, and why an alias cannot be used in WHERE. | 04 | FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY; WHERE runs before the alias exists. |
| [S] | INNER against LEFT against FULL OUTER: what does each drop or keep? | sql/04 bridge, anti-join | Matches only; all of the left plus matches; both sides' orphans. The anti-join is LEFT with a NULL test on the right. |
| [S] | RANK, DENSE_RANK, ROW_NUMBER on a tie. | sql/04 monthly rollup | Gap after the tie; no gap; arbitrary break. The business tells you which. |
| [F] | When does a window function beat GROUP BY? | sql/04 | When every row must stay and the value is computed over neighbours: LAG, running totals, rank within partition. |
| [F] | What is a CTE for, and when does it hurt? | sql/04 | Named steps a reader can follow top to bottom; in some engines a CTE is materialised, so a huge one can cost memory. |
| [F] | A query over a million rows is slow. First three things you look at. | sql/05 | EXPLAIN ANALYZE; whether a scan, a sort or a join dominates; whether an index on the filter or group columns exists and is used. |
| [D] | Why no foreign key from payments to invoices in your schema? | sql/01 | Orphan payments must load so they can be listed; a foreign key would reject them at load and hide the problem. |
| [D] | How would you make the bridge query something finance runs every week? | sql/04, appendix stretch | Parameterise the period, add the index the filter needs, assert the two sides reconcile in the query itself, schedule it. |

## Data and statistics

| Tag | Question | Where you did it | What a good answer covers |
|---|---|---|---|
| [S] | The dashboard and Finance disagree by Rs 20 lakh. What do you do first? | 03, 05 bridge | Profile both, agree the period and the definition, reconcile input = matched + unmatched, then classify the gap into timing, unmatched and amount. |
| [S] | What does p = 0.03 mean, and not mean? | 05 shuffle | Three percent of chance-only worlds are at least this extreme. It says nothing about the probability that the clinic is fine, and nothing about the size of the effect. |
| [S] | Revenue rose after the discount. Three reasons that is not proof. | 05 fair comparison | Season, selection, mix. |
| [F] | 42 percent on 12 bookings against 31 percent on 400. Which do you trust? | 05 | The second; the first is noise with a headline. Say the sample size beside every rate. |
| [F] | Two systems export the same entity with different id formats. How do you reconcile them? | 02, 03 | Trace one entity through both by hand, write the mapping rule, apply it, check the count before and after, list what did not map. |
| [D] | Your bridge balances. Name one way it could balance and still be wrong. | 05 bridge | Two errors cancelling: a mis-keyed payment counted on the wrong invoice and that invoice's own payment missing. |
| [D] | Why can every segment fall while the total rises? | 05 fair comparison | Mix: the total is a weighted average and the weights moved toward the segment with the higher level. |

## The project itself

| Tag | Question | Where |
|---|---|---|
| [S] | Walk me through the analysis you did on unfamiliar data and one decision you would defend. | approach-log |
| [S] | You have joined a healthcare company; how would you apply what you did in retail to our data? | project-statement, section 5 |
| [F] | What changes when the cost of an error is a missed diagnosis rather than a missed sale? | project-statement, section 5 |
| [F] | What broke, and what did you do? | challenges-log |
| [D] | State your finding in one sentence a COO can carry into a board meeting. | slide 3 |
| [D] | What would make you wrong? | slide 5 |

## Notebook-wise simplified answers

These answers are written as short viva responses. Start with the first sentence, then add the second sentence if the interviewer asks for more detail.

### Notebook 01 · Profiling

#### 1. Why did the first CSV read fail, and why should encoding not be guessed?

The legacy file was not UTF-8; it used Latin-1, and its dates were day-first. Trying random encodings until the file opens is unsafe because the file may open while accented characters are silently changed. The correct approach is to confirm the source-system encoding and write it explicitly in the loader.

#### 2. What does `category` do, and when is it a bad choice?

`category` stores each repeated value once and stores a small code in each row, so low-cardinality columns such as city use less memory and can group faster. It is a poor choice for high-cardinality fields such as booking IDs, because almost every value is different and the category table gives little benefit. It also needs care when combining tables with different category lists.

#### 3. What does the profile reveal that `head()` does not?

The profile shows the table's grain, duplicate level, missing-value rate, date range, data type and ID-format quality. For example, more than one row per booking ID means the table is at booking-test grain, not booking grain. It also reveals that invoice amounts are text, payment timestamps are Unix seconds, and even a small missing rate can represent many affected tests.

#### 4. Is ID normalisation a parsing step or a cleaning decision?

It is a cleaning decision because we are asserting that two text forms identify the same record. Trimming a trailing space is a low-risk, reversible rule and should be logged with its row count. A transposed digit is different: repairing it would be guessing, so it should remain unmatched and appear in an exception list.

#### 5. Which table should be used to count tests?

Use the booking-test data for test counts, because each row represents a test inside a booking. Use `n_tests.sum()` after rolling up to booking grain. Do not use the number of bookings as the test count, and do not use `len()` as the booking count when a booking can contain multiple test rows.

### Notebook 02 · Loading and validation

#### 1. Why use a process pool instead of a thread pool?

Reading compressed files and parsing CSV or JSON uses CPU as well as disk. Python threads compete for the interpreter, while separate processes can use separate interpreters. Threads are better when the work mostly waits for I/O, such as network requests, or when moving large data between workers would make processes expensive.

#### 2. What is a booking in this project?

A booking is one patient visit, represented by one booking ID after the test rows have been grouped together. Multiple test rows can belong to that one visit. A Nova reschedule creates a replacement record, but whether the old record counts separately is a later identity decision; for comparable visits, the superseded original is not counted twice.

#### 3. Why validate with Pydantic instead of only using Pandas string checks?

Pydantic gives one named contract for a complete booking. It checks field formats and rules involving several fields, and it records a reason when a booking is rejected. It is slower than vectorised Pandas checks, so we use it once at the input boundary and use DataFrames for later analysis.

#### 4. How many bookings were rejected, and could some have been real visits?

The full run had `567,986` input booking records, with `564,879` accepted and `3,107` rejected. Some rejected rows may represent real visits, but they do not satisfy the current data contract and cannot be safely repaired without source-system evidence. They are preserved in `rejects_bookings.csv`, not silently deleted.

#### 5. Would a fresh rerun produce the same rejection count?

It should, because the input files, validation rules, sorting and reconciliation are deterministic. A different count would require an explained change such as new raw files, a changed model, a different package version or a changed source-data rule. The check `567,986 = 564,879 + 3,107` makes the result auditable.

### Notebook 03 · Cleaning and reconciliation

#### 1. What is `pd.NA`, and why is `fillna(False)` important?

`pd.NA` is Pandas' missing-value marker for nullable columns. Comparing a missing status with `"rescheduled"` produces an unknown value, and negating it with `~` still produces an unknown value. In a filter, those rows can disappear, so the notebook uses `fillna(False)` to say that a missing reschedule status is not marked as rescheduled.

#### 2. How do you make two systems comparable when they store the same event differently?

Trace one real event through both systems, describe how each system records it, define one common business event, and map both systems to that definition. Then compare the counts only after applying the rule. The trap is comparing raw rows and mistaking a storage difference for a business difference.

#### 3. Why were superseded Nova bookings removed?

Nova creates a new booking when a visit is rescheduled and marks the old one as rescheduled. Legacy changes the existing booking instead. Keeping both Nova records would count one visit twice, so `1,499` superseded originals were removed. The comparable population became `563,380` bookings and `1,303,719` tests.

#### 4. What do `left`, `validate='one_to_one'` and `indicator=True` mean?

The left join keeps every booking, even when no collection row matches. `validate='one_to_one'` checks the expected key relationship and raises if the data breaks it. `indicator=True` adds `both`, `left_only` and `right_only`, making unmatched records visible instead of hiding them.

#### 5. What does `left_only` mean here?

It means a booking has no matching collection record. It does not prove cancellation: the booking may be in the future, may have had no sample, may be missing an export event, or may have an ID mismatch. There were `18,269` such bookings, so the notebook keeps them and labels the status cautiously as `cancelled_or_missing`.

#### 6. Why is patient deduplication a business decision?

Merging two patient rows says that they are the same human, so it changes the number of people and the visits-per-person calculation. We used normalised phone, name and date of birth, producing `303,153` people from `309,217` rows. The `1,492` placeholder-DOB rows are a limitation: this rule is suitable for aggregate growth analysis, not definitive identity proof for clinical communication.

#### 7. What does it mean when a join grows?

A growing join usually means the right-hand key appears more than once, so one left row is being copied. Possible causes include repeated scans, multiple payment attempts, genuine multiple charges, or a wrong join key. Check duplicate counts by key, filter to the correct status, and validate the intended one-to-many or one-to-one relationship before accepting the join.

#### 8. Which cleaning rule changed the booking headline most, and what would finance challenge?

Removing superseded Nova records changed the booking headline by `1,499` visits. Finance would challenge the invoice/payment matching first because references need normalisation, units differ, unmatched records remain, and one invoice can have multiple captured payments. Those finance outputs are supporting groundwork for Brief A, not the selected headline.

### Notebook 04 · SQL transformations

#### 1. What is the logical order of a grouped SQL query?

Conceptually, SQL processes `FROM` and joins first, then `WHERE`, `GROUP BY`, `HAVING`, `SELECT`, `ORDER BY` and `LIMIT`. A `SELECT` alias cannot normally be used in `WHERE` because `WHERE` is evaluated before the alias is created. `HAVING` comes after grouping, so it can filter an aggregate such as a count.

#### 2. When is a window function better than `GROUP BY`?

Use a window function when every original row must remain while you calculate a value using related rows. Examples are the previous month's value, a running total, or a rank within a city. The partition says which rows belong together, and the order says how the calculation proceeds; a tie-breaker is needed for deterministic results.

#### 3. How would you investigate a slow query over 1.3 million rows?

Start with `EXPLAIN ANALYZE`. Check whether the cost is a full scan, sort, join or aggregation, and whether the estimated row count is far from the actual count. An index on fields commonly used for filtering, such as city and date, may help, but indexes use storage and slow writes, so add only indexes that support repeated queries.

#### 4. Which Pandas number should SQL reproduce for Brief A?

SQL should reproduce the H1 2025 and H1 2026 booking, people and test totals, then calculate the same three factors: people, visits per person and tests per visit. The result should agree with Pandas: `431,261` versus `452,933` tests and `+5.03%` growth. If it differs, check the date boundaries, grain, rejected rows and person identity mapping before changing either result.

#### 5. Why are raw rejected or unmatched records not hidden by database constraints?

An audit dataset should load exceptions so they can be reported. A strict foreign key could reject an unmatched payment or malformed reference at load time and make the problem disappear from the analysis. Preserve the exception, flag it, and decide how it affects the headline.

### Notebook 05 · Methods and Brief A

#### 1. What is the Brief-A tree?

The tree says:

```text
tests = people × visits per person × tests per visit
```

It separates total test growth into three understandable drivers. People means distinct `person_id` values, visits means booking-grain rows, and tests per visit means total tests divided by visits.

#### 2. What did the tree show?

H1 2025 had `431,261` tests, `93,926` people and `187,771` bookings. H1 2026 had `452,933` tests, `97,501` people and `193,005` bookings. Tests grew `5.03%`; people grew `3.81%`; visits per person fell `0.98%`; and tests per visit grew `2.18%`.

#### 3. Why use log growth?

The factors multiply, and the logarithm turns multiplication into addition. Therefore the log growth of people plus the log growth of visits per person plus the log growth of tests per visit equals the log growth of tests exactly. Ordinary percentage changes only add approximately, so the log check is a reliable reconciliation.

#### 4. What would you check before presenting the tree?

Check that the two periods use the same date boundaries and the same booking definition. Check that people are counted with `person_id.nunique()` rather than raw patient IDs, and check that rejected and superseded records are handled consistently. Finally, confirm that the three branches multiply back to the total.

#### 5. What is the Brief-A limitation?

The conclusion depends on the person identity rule, the completeness of the H1 data and the stability of the booking definition. Placeholder DOBs can affect person deduplication, so the result is a defensible aggregate explanation, not proof of an individual-level causal story.

### Notebook 06 · Answer and cold run

#### 1. What is the final board number?

The board number is `+5.0%`, rounded from the exact `+5.03%`. It compares `452,933` tests in H1 2026 with `431,261` tests in H1 2025. The denominator is the H1 2025 test total, and the unit is tests on cleaned booking records.

#### 2. What makes the final claim defensible?

It has a percentage, numerator, denominator, period and explanation of the drivers. It also states the main caveat: the result depends on the documented identity rule and complete period coverage. A number without those details would be difficult to audit or interpret.

#### 3. What does the cold run prove?

It shows that the answer can be regenerated from the clean files without relying on hidden notebook state. The final run passed the finite-number check and the written-claim check, and produced `slides/board_number.xlsx`.

#### 4. What would make the claim wrong or require revision?

The claim would need revision if the H1 files were incomplete, the booking or patient identity rules changed, rejected records were later proven valid, or the clean outputs were generated from different source data. The claim should then be recalculated and the change recorded rather than silently overwriting the old result.
