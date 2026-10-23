# Project statement · Objectives A, B and E · Group 6

Written in Scope, before the data is opened. Updated when the data proves a line wrong, with the old line struck through rather than deleted, so the panel can see what you learned.

## 1. Dr Menon's words

> Working sponsor question, inferred from the selected objectives: What is happening to Kalpa Health's test volume, how much of the apparent change is real rather than a booking-system measurement effect, and did the campaign increase bookings beyond seasonality and patient mix?

## 2. The question in our words

The sponsor needs one evidence-based view of growth, booking measurement and campaign performance. We will decompose test-volume change into people, visits per person and tests per visit; compare legacy and Nova using a common booking definition and like-for-like periods; and compare campaign versus non-campaign bookings while accounting for seasonality, patient mix and segment differences. The answer determines whether the next action belongs primarily with operations, data governance during migration, or marketing experimentation.

## 3. The question she did not ask

What operational or commercial factors explain the observed change after the data has been made comparable? This matters because the available exports can describe the pattern and quantify the reconciliation, but may not establish why patients or clinics behaved differently.

## 4. Translation into the method

| Her words | The Week 1 or 2 method it maps to | Where the vocabulary changes |
|---|---|---|
| Test volume changed | The tree: people × visits per person × tests per visit | “Growth” must be separated into its measurable drivers. |
| Legacy and Nova totals differ | The ladder and fair comparison | Raw rows are not comparable when the systems use different grains and reschedule rules. |
| Campaign bookings differ from ordinary bookings | The fair comparison and segment grid | The apparent lift must be separated from seasonality, selection and mix shift. |

## 5. What does not transfer from Retail

| In Retail | In a diagnostics business | What changes for our analysis |
|---|---|---|
| A missed sale costs one order. | A missed visit may affect several tests and downstream lab capacity. | Count visits and tests separately. |
| The shopper chooses the basket. | A patient, clinic, channel and test package jointly shape the visit. | Preserve booking, patient and test grains. |
| | One visit can appear differently across booking, collection, invoice and payment systems. | Define identities and reconcile systems before comparing totals. |

## 6. Our prediction, before the data

Before profiling, dated 2026-10-23: we expect the apparent change in test volume to be a combination of patient volume, visit frequency and tests per visit rather than one single driver. We also expect some legacy-versus-Nova difference to be measurement-related because the source systems have different grains, and we expect the invoiced-to-collected gap to include timing and unmatched-reference items.

## 7. Requirements

### Functional: what the analysis must do

| # | Requirement | How we will show it is met |
|---|---|---|
| F1 | Explain H1 2025 versus H1 2026 test-volume change. | Tree decomposition with counts, rates, periods and denominators. |
| F2 | Compare legacy and Nova fairly. | Booking-level and test-level measures after common normalization, with reschedules addressed. |
| F3 | Evaluate campaign/offer effectiveness. | Compare offer and non-offer bookings by period and segment, with selection and seasonality caveats. |
| F4 | Preserve reproducibility and auditability. | Cold run, validation checks, rejected-record file and decision logs. |

### Non-functional: how well it must do it

| # | Requirement | How we will show it is met |
|---|---|---|
| N1 | Re-runs from a fresh Codespace in under ten minutes with no manual edits. | A teammate's cold run, logged in decisions-log.md. |
| N2 | A finance analyst can audit every number back to rows. | Clean tables, SQL grain comments and exception lists. |
| N3 | Every cleaning decision is written down with its reason and effect. | decisions-log.md and challenges-log.md. |
| N4 | No raw record is silently repaired or discarded. | Accepted/rejected reconciliation and explicit anomaly handling. |

### Constraints: what we cannot change

| # | Constraint |
|---|---|
| C1 | Use the repository's Python, Pandas and SQL workflow with the released raw data. |
| C2 | Do not make causal or clinical claims unsupported by the exports. |
| C3 | Preserve raw files; cleaning must be reproducible and logged. |
| C4 | Work within the available January 2025 to June 2026 data period. |

## 8. Scope

| In | Out, and why |
|---|---|
| H1 2025 versus H1 2026 test-volume decomposition | Causal explanations that require data not present in the pack |
| Legacy/Nova booking comparability and data-quality reconciliation | Clinical interpretation of patient results |
| Campaign/offer comparison and actionable experiment recommendations | Unverified repair of ambiguous IDs |
| Reproducible clean tables, SQL and audit logs | Periods outside the released data |

## 9. Done looks like

Done means a fresh run produces clean, reconciled tables and three defensible findings: what drove test-volume change, what part of the booking-system difference is measurement, and whether the campaign produced evidence of lift beyond seasonality and mix. Each finding carries its denominator, period, caveat and action.

## 10. Who signs off

| Reader | What they will check | What would make them reject it |
|---|---|---|
| Dr Menon | Three concise findings and the action each supports | A number without a comparison, denominator or period |
| The finance controller | Every invoice/payment number traces to rows | A bridge with unexplained unmatched or duplicate items |
| City and clinic leaders | Booking and test comparisons are fair across systems | Treating source-system row counts as business performance |
