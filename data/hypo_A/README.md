# data/clean

## Current Brief A basis (2026-10-24)

The current Brief A results use the IITGN Build 1 cleaned-booking rule: sum `n_tests` on validated bookings after removing `status_at_export = rescheduled` originals, grouped by full local `slot_at` H1 dates. H1 2025 is 433,611 lines and H1 2026 is 455,383 (+5.0211%). The definition, hypothesis result, city/plan interpretation, and limits are in `../../docs/brief-a-iitgn-aligned-results.md`.

Run `../../notebooks/05d_brief_a_iitgn_alignment.ipynb` to create the additive `brief_a_iitgn_*.csv` outputs. It uses existing IITGN intermediate/clean tables and the current plan table. It does not rerun cleaning or modify source files. The helper completed in about 29 seconds on this machine.

The older 05a–05c outputs and the earlier slide/workbook package remain available as historical artifacts. They use the nonblank booking-source test-code-line candidate and must not be quoted as the current IITGN-aligned Brief A values. The existing cold-run label “collected or no-show” is not implemented as a filter; the selected count is not a completed-test count. The official KPI definition and formal city-plan crosswalk remain open.

Reproducible notebook outputs. The notebooks resolve the released source pack from the sibling
`kalpa_healt/datapack` folder, or from `KALPA_DATA_ROOT` when set. The starter-kit `data/raw`
sample is not selected implicitly. Booking outputs are written by notebook 02; each later table
is profiled and processed only at its approved step. Regenerate an output by rerunning its source
notebook from a fresh kernel.

## Bookings, completed step

- `bookings_source_rows.csv.gz`: parsed booking/test rows with source file, source record number,
  original timestamp text, and the source values retained.
- `bookings.csv.gz`: one candidate per system and unchanged source booking ID, plus quality flags.
  “Accepted” here means it could be grouped consistently; it does not mean every field is ready
  for every brief's metric.
- `rejects_bookings.csv.gz`: candidates without a usable ID or with conflicting booking-level
  values. This pack produced zero such candidates.
- `bookings_file_reconciliation.csv`: per-file input, classified repeated headers, retained rows,
  and reconciliation checks.
- `bookings_column_profile.csv`, `bookings_category_profile.csv`, and `bookings_id_profile.csv`:
  observed columns, category values, and ID-format diagnostics.
- `bookings_id_trim_collision_profile.csv` and `bookings_id_trim_collisions.csv`: diagnostics for
  whether trimming outer ID whitespace would merge raw IDs. No ID was changed.
- `bookings_integrity_summary.csv`: duplicate-payload, testless-record, and reschedule diagnostics.

## Collections, completed step

- collections_source_rows.csv.gz: all 552,492 parsed gzip-CSV source rows as strings, with source file, source row reference, filename city, and filename month. All 108 UTF-8 files match the supplied manifest; raw collection exports are unchanged.
- collections.csv.gz: 549,598 canonical rows after classifying only exact copies across the six source fields. Original timestamp text is retained in collected_at_raw; collected_at is parsed as local Asia/Kolkata time. IDs and category strings are unchanged.
- collections_classified_duplicates.csv.gz: 2,894 extra exact-payload copies with a pointer to the retained source row. These are classified copies, not proof of double scans.
- collections_file_reconciliation.csv: row accounting for each of the 108 source files, including manifest size/hash checks.
- collections_column_profile.csv, collections_category_profile.csv, and collections_integrity_summary.csv: raw fields and types, category values, timestamp range/completeness, ID-format diagnostics, duplicate counts, and other profile checks. The source has no numeric or currency field; its event timestamps are documented as local time.
- collections_booking_link_profile.csv, collections_booking_link_exceptions.csv.gz, collections_booking_field_differences.csv.gz, and collections_booking_time_flags.csv.gz: exact-key join counts, unmatched rows, unapplied whitespace-match candidates, case differences, and event/slot time diagnostics. No unmatched rows were dropped and no booking data was overwritten.

## Patients, completed step

- `patients_clean.csv.gz`: one row per reversible analytic person proxy, with the selected source patient row, original field values, `person_id`, source-record count, and a flag for DOB exactly `1900-01-01`. Original values are preserved; the DOB flag does not assert that the date is invalid.
- `patients_patient_id_map.csv.gz`: all 309,217 source `patient_id` values mapped to an analytic `person_id` and the rule used. This retains traceability for account rows classified into the same person proxy.
- `patients_identity_review.csv.gz`: IDs and decisions for the 6,064 repeated normalized phone/name/DOB candidate groups; no names, phone values, or DOB values are copied into this review file.
- `patients_reconciliation.csv` and `patients_identity_summary.csv`: row accounting, field/date diagnostics, candidate counts, and the analytical identity-proxy count.
- `patients_column_profile.csv`, `patients_id_profile.csv`, `patients_phone_format_profile.csv`, and `patients_city_profile.csv`: aggregate profiles only; IDs, names, and phone values are not printed in these files.
- `patients_booking_link_profile.csv` and `patients_booking_link_exceptions.csv.gz`: exact-string LEFT join counts and any unmatched booking rows. The join retained all 568,007 bookings; this pack had zero unmatched booking rows. Patient account IDs with no booking remain in the patient master.
- `bookings_clean.csv.gz`: the unchanged booking rows plus `person_id` from the patient-ID crosswalk; no booking rows were filtered.

The person mapping is a reversible analytical proxy, not a clinical identity determination. It maps only two-row candidates with a normalized phone/name/DOB signature, same city and signup date, a valid DOB other than `1900-01-01`, and at most one account ID already used by bookings. The 35 candidate groups containing the sentinel DOB were left separate. Invoices, gateway payments, settlements, lab results, and the campaign master are completed approved steps. The campaign-booking link table remains pending its own approval.


## Invoices, completed step

- `invoices_source_rows.csv.gz`: all 470,776 parsed invoice rows as source text with `source_file` and one-based `source_row_number` provenance.
- `invoices_clean.csv.gz`: all source rows retained with original invoice/date/booking/patient/city/channel/amount values, plus `source_file` and numeric `amount_rs` for downstream SQL. IDs remain strings; no booking or payment join was performed.
- `invoices_file_reconciliation.csv`: row accounting and per-file schema, UTF-8/gzip, filename-period, byte-size, and manifest SHA-256 checks for all seven invoice files.
- `invoices_column_profile.csv`, `invoices_id_profile.csv`, `invoices_category_profile.csv`, and `invoices_integrity_summary.csv`: null/blank/type/date/amount diagnostics, aggregate ID lengths/prefixes, city/channel counts, invoice-ID/exact-payload uniqueness, and invoice-per-booking counts.
- All 470,776 rows reconcile as 470,776 kept + 0 classified + 0 rejected. Invoice IDs are globally unique in this source; no exact payload copies or blank source fields were observed. Amount text has valid grouped formatting with two decimal places and is retained unchanged.
- Four rows dated 2024-12-30/31 are present in `invoices_2024Q4.csv.gz`, earlier than the README's stated Jan 2025 start; they are retained and flagged by filename-period/date profile. One invoice per booking_id was observed inside this source, but the relationship to the bookings table has not been validated.
- Gateway payments were profiled and linked to invoices in an approved step. Settlement exports were processed only in the next separately approved step; no payment cutoff or paid/unpaid conclusion was made.


## Gateway payments, completed step

- `payments_source_rows.csv.gz`: all 473,507 monthly gateway payment-attempt rows as source text, with `source_file`, one-based `source_row_number`, derived UTC/local timestamps, rupees, invoice-reference candidate, and link classification. Settlement export files are not included.
- `payments_clean.csv.gz`: all 473,507 gateway attempts retained in the existing SQL schema order. Original `notes_invoice_ref`, `amount_paise`, `created_at_epoch`, `status`, and `settlement_id` values remain unchanged; numeric `amount_rs`, Asia/Kolkata `created_at`, and a strict-format `invoice_id` candidate are added. Malformed reference shapes have a blank candidate; valid-shaped candidates absent from invoices remain visible as orphans.
- `payments_file_reconciliation.csv`: row accounting, schema, encoding, UTC timestamp ranges, UTC/local month-boundary counts, and manifest size/hash checks for all 20 gateway files. All files match the manifest. The filename month agrees with UTC event month in all rows; 3,173 local timestamps fall into the next calendar month after UTC-to-Asia/Kolkata conversion.
- `payments_column_profile.csv`, `payments_id_profile.csv`, `payments_category_profile.csv`, and `payments_integrity_summary.csv`: source field completeness/types, aggregate ID and reference shapes, status/method counts, amount/time quality, duplicate diagnostics, and source period.
- `payments_invoice_link_profile.csv` and `payments_invoice_link_exceptions.csv.gz`: validated many-to-one LEFT join counts and row-level unmatched attempts. Exact raw reference matches: 329,122; links after strict supported normalization: 468,742; 1,976 formatted candidates lack an invoice row; 2,789 references do not fit the supported formats. All 4,765 unmatched attempts remain in the exception output.
- Attempt grain is preserved: 19,492 matched invoice IDs have two attempts, 141 have three, and 4 have four. 21,820 invoice rows have no supported attempt link under the rule; this is not evidence that they are unpaid, and the 1,976 candidates absent from the invoice export may reflect scope or export gaps.
- Gateway payment files include two Dec 2024 attempts and 1,791 July 2026 attempts beyond the data-pack README's stated Jan 2025–Jun 2026 period; these rows were retained. The subsequent settlement step uses exact settlement IDs only and does not infer paid/unpaid status or apply an export cutoff.


## Settlements, completed step

- `settlements_source_rows.csv.gz`: all 562 quarterly settlement rows as source strings with source file and one-based source row number. No rows were classified or rejected.
- `settlements_clean.csv.gz`: all 562 rows retained with source ID, paise, UTR, epoch, and status fields unchanged, plus derived rupee amount/fees/tax and UTC/Asia-Kolkata timestamps. IDs remain strings.
- `settlements_file_reconciliation.csv`: per-file row accounting, schema, UTF-8/gzip, UTC-quarter/filename agreement, and manifest size/hash checks for all eight files; every file matches.
- `settlements_column_profile.csv`, `settlements_id_profile.csv`, `settlements_category_profile.csv`, and `settlements_integrity_summary.csv`: completeness, observed ID/category shapes, numeric/time parse diagnostics, duplicate checks, ranges, and row accounting.
- The epoch range is 2024-12-31 10:00 UTC through 2026-07-15 10:00 UTC. One settlement row predates the README's Jan 2025 start and 15 follow the Jun 2026 end; all are retained and reported rather than cut off.
- `settlements_payment_link_profile.csv` and `settlements_payment_status_link_profile.csv`: validated exact-string LEFT link from the 455,469 gateway attempts with nonblank settlement IDs to 562 unique settlement rows, with no fan-out. The 18,038 blank gateway settlement IDs are accounted separately; in this export they coincide with gateway rows whose source status is `failed`. This describes the source fields and is not a settlement cutoff or an independent paid/unpaid determination.
- `settlements_payment_link_exceptions.csv.gz`: all 18,038 gateway attempts with blank settlement IDs and any nonblank exact IDs absent from the settlement export (none in this pack), retained with reason. No unmatched attempt or settlement row was dropped.


## Lab results, completed step

- `results_source_rows.csv.gz`: all 1,078,420 result rows from 108 monthly city files, with source file, one-based source row number, source-city folder, and filename month. The source has no dedicated result-run ID; this file/row pair provides lineage. Source fields are retained as text.
- `results_clean.csv.gz`: all result rows retained with unchanged `booking_id`, `test_code`, `result_ts`, `result_value`, and `result_flag`, plus file/row/city/month provenance and a parsed `result_ts_parsed` value. The timestamp format is `YYYY-MM-DD HH:MM:SS`; the source does not specify a timezone, so none was assigned. Result values were not converted or interpreted.
- `results_file_reconciliation.csv`: per-file row accounting, five-column schema, gzip/UTF-8 checks, manifest size/hash, timestamp range, parse failures, and filename-month differences. All 108 source files match the manifest and reconcile with no classified or rejected rows.
- `results_column_profile.csv`, `results_id_profile.csv`, `results_category_profile.csv`, and `results_integrity_summary.csv`: blank/type diagnostics, aggregate booking-ID shape, test-code and result-flag counts, timestamp/value parse diagnostics, duplicate diagnostics, date range, and row reconciliation. The 3,211 blank source-field cells are all blank `test_code` values. There are no exact repeated full-payload rows or repeated nonblank `booking_id`/`test_code` pairs.
- The pack README date range is Jan 2025–Jun 2026; six result timestamps predate it and 1,426 fall after it. 24,002 parsed result calendar months differ from their filename month. These records remain unchanged and are diagnostics only.
- `results_booking_link_profile.csv`: exact-string LEFT join from result rows to unique canonical booking IDs. 1,062,808 of 1,078,420 rows matched; 15,612 result rows for 9,828 distinct booking IDs did not. No result booking IDs were blank. 103,930 canonical booking candidates had no exact result row. No result rows were dropped.
- `results_booking_link_exceptions.csv.gz`: unmatched result rows with booking ID, test code, timestamp, source city, file/row provenance, and reason; result values are deliberately omitted from this exception file.
- `results_booking_city_profile.csv` and `results_booking_city_comparison_profile.csv`: path-city versus matched booking-city diagnostics only. In particular, 156,425 result rows in the `bengaluru` folder link to booking rows labeled `Bangalore`; labels were not normalized and city was not used as a join key.
- One booking can have multiple result rows because the documented result grain is one row per lab test run. No-result booking counts are not proof that a visit did not happen, and result flags/values do not establish clinical meaning or completed-visit status.

## Campaign master, completed step

- `campaigns_source_rows.csv.gz`: all 1 source row from `campaigns/campaigns.csv` as text, with source file and one-based row provenance. The supplied manifest entry matches both byte size and SHA-256.
- `campaigns_clean.csv.gz`: the same row and original five source fields retained, with parsed `starts`/`ends` diagnostics and a numeric `waiver_rs` diagnostic. IDs and labels remain strings; no rows were classified or rejected.
- `campaigns_file_reconciliation.csv`, `campaigns_column_profile.csv`, and `campaigns_integrity_summary.csv`: source schema/encoding, row accounting, manifest validation, blank/whitespace/type/date diagnostics, and campaign-ID/payload duplicate checks.
- The source master has one campaign row. The separate `campaign_bookings.csv.gz` table was not read or joined in this step; no exposure, redemption, booking eligibility, or lift conclusion was calculated.

## Campaign-booking tags, completed step

- `campaign_bookings_source_rows.csv.gz`: all 48,869 rows from `campaigns/campaign_bookings.csv.gz` retained as source strings with file/row provenance. All three source fields are populated; the file matches the supplied manifest size and SHA-256.
- `campaign_bookings_clean.csv.gz`: all source rows retained with unchanged `booking_id`, `campaign_id`, and `waiver_rs`, plus exact-link statuses, campaign-master fields, canonical booking city/system for exact booking matches, and a numeric waiver parse diagnostic. No campaign date or exposure status is present in this source table.
- `campaign_bookings_file_reconciliation.csv`, `campaign_bookings_column_profile.csv`, `campaign_bookings_id_profile.csv`, `campaign_bookings_category_profile.csv`, and `campaign_bookings_integrity_summary.csv`: source schema/encoding, row accounting, manifest checks, blank/type/ID-shape diagnostics, and duplicate-pair checks. The repeated campaign_id is expected foreign-key reuse; no booking_id/campaign_id pair repeats. Observed grain is one row per booking/campaign pair in this export; this is not asserted as a vendor-wide contract.
- `campaign_bookings_booking_link_profile.csv` and `campaign_bookings_campaign_link_profile.csv`: exact-string LEFT joins validated as `many_to_one`. All 48,869 campaign IDs linked to the one-row master and all waiver strings matched. Exact unchanged booking IDs linked for 46,871 of 48,869 rows; all 1,998 unmatched tags remain visible.
- `campaign_bookings_link_exceptions.csv.gz`: the 1,998 exact-unmatched booking tags with reason and a trim-only candidate diagnostic. Each had one candidate when outer whitespace was stripped from both keys: 1,519 unmatched source IDs had whitespace in the campaign-tag file and 479 had whitespace only in the canonical booking ID. There were zero trimmed-key collisions on either side. Candidates were not joined because a source normalization rule is not documented.
- `campaign_bookings_city_link_profile.csv`: matched tags grouped by canonical booking-city label for linkage profiling only. No campaign outcome, offer eligibility, exposure, redemption, or lift was inferred. The 521,136 canonical booking rows without an exact tag in these exports are not proof of no marketing exposure.

## City reference, completed step

- `cities_source_rows.csv` and `cities_clean.csv`: all 6 rows from `reference/cities.csv` retained as text with one-based source-row provenance. `city_code` and `city` are unique, every source field is populated, and no value was normalized.
- `cities_file_reconciliation.csv`, `cities_column_profile.csv`, `cities_id_profile.csv`, `cities_category_profile.csv`, and `cities_integrity_summary.csv`: UTF-8/schema and manifest checks, 6 = 6 + 0 + 0 row accounting, field/ID/region profiles, and duplicate diagnostics. The file matches the manifest size and SHA-256.
- `cities_booking_link_profile.csv` and `cities_booking_label_profile.csv`: exact-string LEFT join of canonical bookings to the unique `city` labels, validated many_to_one. All 568,007 booking rows remain after the join; 483,605 match one of the 6 reference labels and 84,402 do not.
- `cities_booking_link_exceptions.csv.gz`: all 84,402 unmatched booking rows, each labeled `Bangalore` in the legacy source. The reference label is `Bengaluru`, but no alias mapping was applied because the booking table has no city_code and the pack contains no crosswalk. This exact-label mismatch is not a city-performance finding.

## Clinic reference, completed step

- `clinics_source_rows.csv` and `clinics_clean.csv`: all 31 rows from `reference/clinics.csv` retained as source strings with one-based row provenance. `clinic_id` is nonblank and unique; all source fields are populated. Date and numeric-looking fields are diagnostics only; no values were normalized or converted in the clean table.
- `clinics_file_reconciliation.csv`, `clinics_column_profile.csv`, `clinics_id_profile.csv`, `clinics_category_profile.csv`, and `clinics_integrity_summary.csv`: schema/encoding and manifest checks, 31 = 31 + 0 + 0 row accounting, field/type and identifier profiles, observed categories, and duplicate diagnostics. The source file matches the supplied manifest size and SHA-256.
- `clinics_city_link_profile.csv` and `clinics_id_prefix_city_profile.csv`: the exact clinic `city` LEFT join to the approved city reference, plus a diagnostic comparison of clinic-ID prefixes to city codes. All 31 clinic labels match; prefixes happen to equal city codes for all 31 rows, but no prefix mapping is applied.
- `clinics_city_link_exceptions.csv`: clinic rows without an exact city-reference label match; this file is empty for this pack.
- `clinics_booking_link_profile.csv` and `clinics_booking_label_profile.csv`: exact unchanged `clinic_id` LEFT join from canonical bookings to the unique clinic reference, validated as many_to_one. All 568,007 booking rows match one clinic. After exact links, 84,402 legacy rows labeled `Bangalore` differ from the linked clinic's `Bengaluru` label; the comparison does not rewrite either field.
- `clinics_booking_link_exceptions.csv.gz`: booking rows without an exact clinic-ID link. This file is empty for this pack.
- `clinics_booking_city_mismatches.csv.gz`: row-level booking/clinic city-label differences after exact clinic-ID matches. The labels remain unchanged; these differences do not establish a business alias or a city outcome.

## Tests catalogue, completed step

- `tests_catalogue_source_rows.csv` and `tests_catalogue_clean.csv`: all 24 rows from `reference/tests_catalogue.csv` retained as source strings with one-based row provenance. The 24 `test_code` values are nonblank and unique; all fields are populated. Numeric parsing of `list_price_rs` is diagnostic only, and `is_package` remains its source `"0"`/`"1"` string.
- `tests_catalogue_file_reconciliation.csv`, `tests_catalogue_column_profile.csv`, `tests_catalogue_id_profile.csv`, `tests_catalogue_category_profile.csv`, and `tests_catalogue_integrity_summary.csv`: schema/encoding and manifest checks, 24 = 24 + 0 + 0 row accounting, source-field/ID/category profiles, duplicate diagnostics, and code-link totals. The source file matches the supplied manifest size and SHA-256.
- `tests_catalogue_booking_test_link_profile.csv` and `tests_catalogue_booking_test_code_profile.csv`: exact unchanged `test_code` LEFT join from 1,315,204 approved booking test-source rows to the unique catalogue codes, validated many_to_one. 1,313,893 nonblank codes matched; 1,311 rows had blank codes; no nonblank code was absent from the catalogue. All 24 catalogue codes appear in this source.
- `tests_catalogue_booking_test_link_exceptions.csv.gz`: all booking test-source rows with blank or non-catalogue codes, retained with source provenance and reason. In this pack, all 1,311 exceptions are blank-code rows.
- `tests_catalogue_result_link_profile.csv` and `tests_catalogue_result_code_profile.csv`: exact unchanged `test_code` LEFT join from 1,078,420 approved lab result rows, validated many_to_one. 1,075,209 nonblank codes matched; 3,211 rows had blank codes; no nonblank code was absent from the catalogue. All 24 catalogue codes appear in results.
- `tests_catalogue_result_link_exceptions.csv.gz`: all result rows with blank or non-catalogue codes, retained with source provenance and reason. In this pack, all 3,211 exceptions are blank-code rows. Result values were not loaded into or interpreted by this reference step; catalogue prices were not reconciled against booking charges.

## H1 city plan, completed profile/cleaning step

Source: `kalpa_healt/datapack/plan/plan_2026_H1.csv`. The source README describes it as a wide 2026 first-half test-volume target table by city and month. The source contains six city/metric rows and six month columns; all six rows were retained and expanded to 36 city/metric/month rows. All source cells were populated, all target cells parsed as nonnegative integers, both composite keys were unique, and the file size/SHA-256 matched the supplied manifest. Original wide rows and raw target strings are preserved. City and metric text remain unchanged; no city crosswalk or booking join was applied. Targets have not been compared with actuals.

- `plan_2026_H1_source_rows.csv`: all six source rows and original monthly target strings, with source file and row provenance.
- `plan_2026_H1_clean.csv`: long-format city/metric/month targets, preserving raw text and adding a nullable integer parse and parse/key status fields.
- `plan_2026_H1_exceptions.csv`: retained rows with blank/invalid target values or keys and duplicate-key diagnostics; empty for this source.
- `plan_2026_H1_file_reconciliation.csv`: source/long-row counts, file size and SHA-256, and manifest verification.
- `plan_2026_H1_column_profile.csv`, `plan_2026_H1_category_profile.csv`, `plan_2026_H1_key_profile.csv`, and `plan_2026_H1_integrity_summary.csv`: field completeness/types, category counts, observed key uniqueness, parsing, and reconciliation checks.

## Brief A metric/baseline candidate step

Notebook `05a_brief_a_metric_baseline.ipynb` and `src/kalpa/brief_a_baseline.py` read only the approved provenance-bearing booking outputs and the cleaned plan table. The helper counts nonblank `test_code` source rows by exact local `slot_at` and `created_at` months, checks those counts against canonical `n_tests - n_blank_test_code_rows`, and outer-compares grouped plan keys on exact `city + month`. It keeps IDs and labels as strings, retains every booking status and reschedule, and does not alias `Bangalore`/`Bengaluru`.

- `brief_a_metric_baseline_summary.csv`: candidate H1 growth rates, partial exact-label comparison, and clearly marked unreconciled aggregate. None is an official KPI or final claim.
- `brief_a_metric_baseline_monthly.csv`: city/month candidate lines under both date anchors, target, exact-match status, and variance only where slot actual and plan keys match.
- `brief_a_metric_baseline_reconciliation.csv`: source versus canonical nonblank test-line counts by city/system/month for both date anchors. All 148 groups reconcile.

The 2026 plan comparison has 30 exact city/month matches, six plan-only `Bangalore` rows, and six actual-only `Bengaluru` rows. Unmatched rows stay present; no city mapping or full-city plan variance is asserted. No status filter or collection/result join was applied.

## Brief A driver decomposition, completed 2026-10-24

Notebook `05b_brief_a_driver_decomposition.ipynb` and helper `src/kalpa/brief_a_drivers.py` continue from the 05a candidate baseline. The helper reads only the approved outputs in this folder, independently verifies both stored baseline date-anchor totals, and writes new `brief_a_driver_*.csv` files. It does not rerun cleaning, modify raw inputs, or overwrite 05a artifacts. The measured helper runtime was about 59 seconds on this machine; this is not a full-project cold-run result.

The primary unit remains **provisional booking-source test lines**: one nonblank `test_code` source row by the local `slot_at` month. The expanded source-row identity (`source_file`, `source_record_number`, `source_test_order`) has no duplicates in the pack. The source-to-canonical booking link uses exact `system + booking_id`; the pack README describes a booking as one visit by one patient, but the analysis reports booking records as visit proxies because reschedule/supersession identity is not resolved. `patient_id` account counts are primary; `person_id` from the existing analytic map is a sensitivity.

The product identity reconciles on the complete eligible line population for both identities. Driver effects use the average marginal contribution over all six possible factor orders, so the additive bridge reconciles exactly and is descriptive, not causal. Exact raw channel categories and system labels are retained. No channel case normalization or completed-test claim is made.

For city comparisons, source labels remain primary. A separate `Bangalore` → `Bengaluru` sensitivity is supported by exact booking-to-clinic links and the exact clinic-to-city-reference link; the booking-side labels are never rewritten. This is a file-supported comparison sensitivity, not a formally approved effective-dated crosswalk or official KPI decision.

New outputs: `brief_a_driver_checkpoint_verification.csv`, `brief_a_driver_reconciliation.csv`, `brief_a_driver_period_metrics.csv`, `brief_a_driver_component_changes.csv`, `brief_a_driver_shapley_bridge.csv`, `brief_a_driver_city_contributions.csv`, `brief_a_driver_channel_contributions.csv`, `brief_a_driver_status_reschedule_sensitivity.csv`, `brief_a_driver_plan_city_month.csv`, `brief_a_driver_plan_city_contributions.csv`, `brief_a_driver_plan_summary.csv`, `brief_a_driver_city_alias_evidence.csv`, `brief_a_driver_field_consistency.csv`, `brief_a_driver_join_audit.csv`, `brief_a_driver_identity_checks.csv`, and `brief_a_driver_run_metadata.csv`. The status and `rescheduled_from` sensitivities do not alter the primary baseline.

## Brief A result and collection link validation, completed 2026-10-24

Notebook `05c_brief_a_analysis_validation.ipynb` and helper `src/kalpa/brief_a_validation.py` continue from the 05a candidate baseline and 05b driver step. They read only approved cleaned tables in this folder; no cleaning pipeline is rerun and no raw input, 05a baseline artifact, or 05b driver output is overwritten. The candidate remains nonblank booking-source `test_code` rows by local `slot_at` month, with all statuses and reschedule indicators retained.

Result coverage uses exact unchanged `booking_id + test_code` and is only a linkage diagnostic. The canonical booking ID is unique across system namespaces. Result timestamps are not used to select H1 because the source does not document their timezone. Of 435,880 H1 2025 candidate lines, 351,176 have an exact result link (80.5671%); 84,704 remain without one. Of 461,080 H1 2026 candidate lines, 371,623 link (80.5984%); 89,457 remain without one. The linked subset grows 5.8224%, and aggregate coverage changes +0.0312 percentage points. This aggregate masks system variation: H1 2026 legacy coverage is 81.1753% and Nova coverage is 76.9062%; in Chennai and Jaipur the Nova rates are lower than legacy by 4.3170 and 4.9514 percentage points, respectively. These are slot-date cohorts of bookings with exact result links, not H1 result-event counts or a completed-test KPI. All 1,078,420 cleaned result rows are retained; 3,211 have blank/whitespace test codes. Nine extra result rows beyond one per key remain preserved outside the matchable nonblank-key join.

Collection linkage is at booking/visit grain, not test grain. Exact `booking_id` joins match 182,386/189,822 candidate booking records in H1 2025 and 187,581/196,474 in H1 2026. The output groups candidate lines under the exact collection status strings `collected` and `no_show`, plus `no_exact_collection_record`; it does not allocate a collection outcome to individual tests. The join audit also counts right-side records outside each H1 candidate cohort; all remain in their full cleaned tables. Missing results/collections are unknown links, not evidence of cancellation or non-performance.

New outputs: `brief_a_validation_period_summary.csv`, `brief_a_validation_coverage_segments.csv`, `brief_a_validation_collection_status.csv`, `brief_a_validation_join_audit.csv`, `brief_a_validation_reconciliation.csv`, `brief_a_validation_comparison.csv`, and `brief_a_validation_run_metadata.csv`. The helper completed in about 38 seconds on this machine. This is not a full-project cold run; the notebook itself, full cleaning pipeline, and test suite were not run.
