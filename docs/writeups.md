# Individual write-ups · Brief A · Group 6

## Group summary

Dr Priya Menon asked why Kalpa Health's test volume changed between H1 2025
and H1 2026. We answered this with a growth tree rather than treating the
change in the total as an explanation. The tree separates validated booking
test lines into people, visits per person and test lines per visit.

The current result is that validated booking test lines increased from
433,611 to 455,383, or **+5.02%**. People increased 3.77%, visits per person
fell 0.97%, and test lines per visit increased 2.20%. The result is
descriptive, not causal. It depends on the documented identity rules,
complete H1 coverage and the definition of a booking test line. The action is
to confirm the KPI definition with the owner before using the number for
operational targets, then monitor the three growth factors separately.

---

## Aayush

**1. In your own words, what was Dr Menon asking for, and what did she actually need?**

She was asking what drove the change in test volume: more people, more visits
per person, or more tests per visit. She did not need a complicated model or a
list of every data-quality issue. She needed one number with a clear
comparison, a denominator, a period and an explanation that could be repeated
in a board meeting. We therefore treated the decomposition as the main answer
and kept the other work as evidence supporting it.

**2. Which part of the work was yours, and what did you produce that the group now depends on?**

I coordinated the final Brief-A version of the project. I connected the
notebook outputs, Hypo A files, project statement, charter, logs, interview
bank, diagrams and presentation artifacts. I also made sure the old headline
was not mixed with the revised Hypo A result. The group now depends on the
single current definition: 433,611 validated booking test lines in H1 2025
and 455,383 in H1 2026.

**3. Which approaches did you consider for your part, which did you choose, and why not the others?**

We considered using only the original notebooks, using only the teammate's
Hypo A work, or combining both and recording which result was current. We
chose the third option. The Hypo A work fixed the half-year boundary and made
the measure explicit, while the original notebooks preserved the full
profiling and cleaning trail. Replacing the earlier work completely would
have hidden how the number changed. Keeping both without labeling them would
have created two competing headlines.

**4. Which number do you trust most, what is its denominator, and what would make you stop trusting it?**

I trust the current +5.02% growth rate most because its numerator is 455,383
retained booking test lines in H1 2026 and its denominator is 433,611 retained
booking test lines in H1 2025. Both use the same half-open local-date windows
and the same cleaning rule. I would stop trusting it as the business KPI if
the owner supplied a different definition, such as collected or performed
tests, or if a row-level bridge showed that the booking table did not cover
the full periods.

**5. What broke, what did you try, and what did you change? Point at the challenges-log entry.**

The biggest issue was that the first result and the Hypo A result were
different. We traced the difference to the date endpoint and the chosen
measure instead of silently replacing one number. The challenges log records
that the complete calendar half-year includes June 30 after midnight. We
changed the project documents and board artifact to use the Hypo A result and
kept the earlier result as historical evidence.

**6. What do you understand about a diagnostics business now that you did not before?**

A diagnostics visit can create several test lines, and those lines can appear
differently in booking, collection and result systems. A booking row is not
automatically a completed test. That means the grain and identity rule matter
before any growth percentage is calculated. I also understand that a patient
count is not just a distinct ID count when accounts can be duplicated or
contact details can be incomplete.

**7. Where did the team work well, where did it not, and what would you change for Build 2?**

The team worked well when we challenged the first plausible number and
recorded the reason for changing it. The Hypo A work gave us stronger
reconciliation and city evidence. We did not work well when parallel logs and
notebook outputs temporarily created duplicate sources of truth. For Build 2,
I would assign owners in the charter at the start, use one canonical log per
topic, and add a headline-version check before presentation work begins.

**8. Which idea from Weeks 1 and 2 do you understand better after using it on this data, and what was fuzzy before?**

I understand the difference between a metric and a business explanation much
better. Before this project, I might have treated a 5% increase as the
finding. The growth tree showed that a total can rise even when one factor
falls. I also understand that reproducibility is not just rerunning code; it
means preserving the date rule, grain, denominator, exceptions and decision
history.

**9. Which viva question would you least like to be asked, and what is your answer to it?**

I would least like to be asked whether +5.02% proves that patients performed
5.02% more tests. The answer is no. It is a descriptive increase in validated
booking test lines. It is supported by the current data definition, but it
does not prove attendance, collection, performance or causation. A KPI owner
would need to confirm the event definition and provide a bridge to performed
tests.

**10. If you had two more days, what would you do first, and why that?**

I would first obtain the official KPI definition and build a row-level bridge
from booking test lines to collections and results. That would tell us whether
the board number measures booked demand, collected samples or completed lab
work. I would then rerun the same tree under the approved definition and
compare the result with the current descriptive measure.

---

## Harsh

**1. In your own words, what was Dr Menon asking for, and what did she actually need?**

Dr Menon wanted to know what was behind the change in test volume between the
first halves of the two years. The useful answer was not simply “volume went
up.” It needed to identify the contribution of people, visit frequency and
tests per visit, while making clear what the data could and could not prove.

**2. Which part of the work was yours, and what did you produce that the group now depends on?**

My main contribution was the Hypo A recalculation and its supporting evidence.
I worked with the IITGN-aligned booking table and produced the metric summary,
component changes, city contributions, reconciliation and identity checks.
The work established the current values: 433,611 test lines in H1 2025 and
455,383 in H1 2026. It also showed that the increase was spread across most
cities, while Jaipur declined.

**3. Which approaches did you consider for your part, which did you choose, and why not the others?**

For the metric, we considered counting raw nonblank test-code rows, copying
the earlier notebook's timestamp boundary, or using the validated booking
table and complete local calendar half-years. We chose the third approach for
the current descriptive result because it applies the documented cleaning
rule, includes all of June 30 and keeps the numerator and denominator
comparable. The other counts remain useful sensitivities, but they do not
replace the selected result.

**4. Which number do you trust most, what is its denominator, and what would make you stop trusting it?**

I trust the retained-line comparison: 455,383 divided by 433,611 minus one,
which gives +5.0211%. The denominator is the H1 2025 retained booking test-line
count. I would stop treating it as the official KPI if the owner says that
test volume means collected samples, results, attended visits or another
event. I would also revisit it if the source-copy reconciliation or city
crosswalk changed the eligible rows.

**5. What broke, what did you try, and what did you change? Point at the challenges-log entry.**

The main challenge was the difference between the source-line candidate and
the IITGN-aligned result. We compared the source counts, validation
exclusions, superseded lines and the date endpoint. We found that 3,541 H1
2026 lines were removed with superseded records and that the complete
half-year added June 30 lines. We recorded both the arithmetic and the
limitations instead of presenting the revised number as if nothing had
changed.

**6. What do you understand about a diagnostics business now that you did not before?**

I learned that the same patient journey is distributed across several
operational systems. A booking may contain multiple test lines, and a
reschedule may create a new record. Collections and results answer different
questions from bookings. Therefore, a growth analysis needs explicit event
and identity rules before it can be interpreted by operations.

**7. Where did the team work well, where did it not, and what would you change for Build 2?**

We worked well when we reconciled the result at several levels: total
product, log growth, city totals and source rows. We were slower when the
original and teammate logs developed separately. For Build 2, I would create
the Hypo A evidence folder and metric contract at the beginning, then require
every notebook and slide to read the same summary file.

**8. Which idea from Weeks 1 and 2 do you understand better after using it on this data, and what was fuzzy before?**

I understand sensitivity analysis more clearly. A sensitivity is not another
answer chosen because it looks better; it is a controlled alternative that
shows how a definition affects the result. The date-anchor and
reschedule-rule comparisons helped us explain uncertainty without hiding it.

**9. Which viva question would you least like to be asked, and what is your answer to it?**

I would least like to be asked whether the city contributions prove that
Ahmedabad or Bengaluru caused the growth. They do not. Ahmedabad contributed
8,043 lines and Bengaluru 7,535 under the selected city view, but those are
descriptive contributions. They do not separate demand, system migration,
capacity, mix or recording effects.

**10. If you had two more days, what would you do first, and why that?**

I would obtain an owner-approved KPI and a dated city crosswalk. The KPI
would resolve whether the measure is a booking line, collection or result.
The crosswalk would make the plan comparison more defensible. After that, I
would rerun the city and driver tables and check whether the operational
recommendation changes.

---

## Riya

**1. In your own words, what was Dr Menon asking for, and what did she actually need?**

She wanted an explanation of year-over-year test-volume growth that a
non-technical leader could use. The answer needed to be fair to the source
systems and clear about what one visit, one person and one test line meant.
That made data preparation and validation part of the answer, not background
work that could be skipped.

**2. Which part of the work was yours, and what did you produce that the group now depends on?**

My contribution focused on the notebook workflow, loading and validation
logic, SQL reproduction and checks around the clean tables. I helped make the
grain visible: source rows can contain several tests, while the growth tree
needs booking records and analytical people. The group depends on the
accepted/rejected reconciliation, clean-table structure, join checks and
repeatable notebook flow.

**3. Which approaches did you consider for your part, which did you choose, and why not the others?**

For validation, we considered checking individual fields only in Pandas,
validating complete booking objects at the boundary, and repairing records
that failed. We chose boundary validation with rejected records preserved,
because it gives a clear contract without guessing repairs. For joins, we
considered silently normalising IDs and joining unmatched rows, but kept exact
matches primary and reported trim-only candidates separately.

**4. Which number do you trust most, what is its denominator, and what would make you stop trusting it?**

I trust the reconciliation that 567,986 input booking records equal 564,879
accepted plus 3,107 rejected records. It is not the headline, but it proves
that the loading step did not silently lose rows. For the final growth result,
the denominator is 433,611 H1 2025 retained booking test lines. I would stop
trusting the result if the reconciliation failed, a join multiplied rows, or
the two periods used different grains.

**5. What broke, what did you try, and what did you change? Point at the challenges-log entry.**

The first full validation approach used a Python loop and was too slow. We
moved suitable checks to vectorised table operations and kept the boundary
validation and rejection reasons visible. We also found that collection
duplicates and unmatched joins could change downstream counts. We removed
only exact duplicate collection payloads, validated the expected join shape
and kept `left_only` bookings instead of calling them cancellations.

**6. What do you understand about a diagnostics business now that you did not before?**

I understand that data grain is closely connected to patient care and
capacity planning. Counting rows can overstate visits or tests, and treating
a missing collection as a cancellation can misstate operations. A reliable
analysis must preserve exceptions because those exceptions may represent
future bookings, missing exports or real process problems.

**7. Where did the team work well, where did it not, and what would you change for Build 2?**

We worked well when one person's output was checked against another person's
table and when decisions were written down with counts. We did not work well
when separate notebooks and logs used different terminology for the same
measure. In Build 2, I would add a shared data dictionary and a small
automated test that checks the headline numerator, denominator and period
before any presentation file is generated.

**8. Which idea from Weeks 1 and 2 do you understand better after using it on this data, and what was fuzzy before?**

I understand reproducibility as an end-to-end property. It includes file
location, encoding, date boundaries, validation rules, join cardinality,
rejected rows and output names. Previously, I thought matching the code was
enough. Here, two correct-looking runs could still disagree if one includes
June 30 differently or uses a different identity rule.

**9. Which viva question would you least like to be asked, and what is your answer to it?**

I would least like to be asked why a left-only collection join was not treated
as cancellation. The answer is that a missing collection can mean a future
booking, a missing export, an ID mismatch or no sample. Without a trusted
cancellation field, the safe choice is to keep the booking and flag it.

**10. If you had two more days, what would you do first, and why that?**

I would run a fresh end-to-end cold run, including the SQL reproduction, and
compare every checkpoint with the Hypo A CSV outputs. Then I would add tests
for the current headline and for the product identity. This would give the
team stronger evidence that the presentation result can be reproduced by a
new teammate rather than only by the person who built each notebook.
