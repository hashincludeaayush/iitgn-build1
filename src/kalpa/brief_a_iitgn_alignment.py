"""Brief A recalculation using the IITGN Build 1 cleaned booking definition.

This focused step reads existing IITGN intermediate/clean booking outputs and the
already-profiled H1 plan. It does not rerun the raw-to-clean pipeline or modify
source files. All IDs stay strings and source city labels are retained for the
exact-label plan comparison.
"""

from __future__ import annotations

import math
from pathlib import Path
from time import perf_counter

import pandas as pd


KEY = ["system", "booking_id"]
CITY_ALIASES = {"Bangalore": "Bengaluru"}
YEARS = (2025, 2026)


def _read(path: Path, *, usecols: list[str] | None = None, dtypes: dict[str, str] | None = None) -> pd.DataFrame:
    return pd.read_csv(
        path,
        compression="infer",
        dtype=dtypes,
        keep_default_na=False,
        low_memory=False,
        usecols=usecols,
    )


def _local_date(values: pd.Series) -> pd.Series:
    """Read the source-local YYYY-MM-DD prefix without shifting timezone offsets."""
    return pd.to_datetime(values.astype("string").str.slice(0, 10), format="%Y-%m-%d", errors="coerce")


def _period(frame: pd.DataFrame, year: int) -> pd.DataFrame:
    start = pd.Timestamp(f"{year}-01-01")
    end = pd.Timestamp(f"{year + 1}-01-01")
    return frame.loc[(frame["_slot_date"] >= start) & (frame["_slot_date"] < end) & (frame["_slot_date"].dt.month <= 6)].copy()


def _percent_change(later: float, earlier: float) -> float:
    return (later / earlier - 1.0) * 100.0 if earlier else float("nan")


def _assert_unique(frame: pd.DataFrame, columns: list[str], label: str) -> int:
    duplicates = int(frame.duplicated(columns, keep=False).sum())
    if duplicates:
        raise ValueError(f"{label} has {duplicates:,} duplicate rows on {columns}")
    return duplicates


def _tree_metrics(frame: pd.DataFrame, label: str) -> dict[str, object]:
    people = int(frame["person_id"].nunique())
    visits = int(frame["booking_id"].nunique())
    tests = int(frame["n_tests"].sum())
    if people <= 0 or visits <= 0:
        raise ValueError(f"{label} has an empty people or visit denominator")
    visits_per_person = visits / people
    tests_per_visit = tests / visits
    product = people * visits_per_person * tests_per_visit
    if abs(product - tests) > 1e-8:
        raise AssertionError(f"{label} identity does not reconcile: product={product}, tests={tests}")
    return {
        "period": label,
        "booking_rows": int(len(frame)),
        "distinct_booking_ids": visits,
        "distinct_patient_accounts": int(frame["patient_id"].nunique()),
        "distinct_person_ids": people,
        "test_lines": tests,
        "visits_per_person": visits_per_person,
        "test_lines_per_visit": tests_per_visit,
        "identity_product": product,
        "identity_difference": product - tests,
        "missing_booking_id_rows": int(frame["booking_id"].eq("").sum()),
        "missing_patient_id_rows": int(frame["patient_id"].eq("").sum()),
        "missing_person_id_rows": int(frame["person_id"].eq("").sum()),
        "nonpositive_test_count_rows": int((frame["n_tests"] <= 0).sum()),
    }


def _component_rows(metrics: dict[int, dict[str, object]]) -> pd.DataFrame:
    old, new = metrics[2025], metrics[2026]
    specifications = [
        ("test_lines", "sum(n_tests)", "test lines", old["test_lines"], new["test_lines"]),
        ("people", "nunique(person_id)", "distinct IITGN person_id values", old["distinct_person_ids"], new["distinct_person_ids"]),
        ("visits", "nunique(booking_id)", "distinct unchanged booking_id values after superseded-record removal", old["distinct_booking_ids"], new["distinct_booking_ids"]),
        ("visits_per_person", "visits / people", "distinct bookings / distinct person_id values", old["visits_per_person"], new["visits_per_person"]),
        ("test_lines_per_visit", "test_lines / visits", "sum(n_tests) / distinct booking_id values", old["test_lines_per_visit"], new["test_lines_per_visit"]),
    ]
    rows = []
    for metric, formula, unit, earlier, later in specifications:
        rows.append({
            "metric": metric,
            "formula": formula,
            "unit_or_identity": unit,
            "H1_2025": earlier,
            "H1_2026": later,
            "absolute_change": later - earlier,
            "percent_change": _percent_change(later, earlier),
            "log_change_percent": 100.0 * math.log(later / earlier) if earlier and later else float("nan"),
        })

    # The IITGN 05 method uses the exact log identity for the multiplicative tree.
    log_components = [
        100.0 * math.log(new["distinct_person_ids"] / old["distinct_person_ids"]),
        100.0 * math.log(new["visits_per_person"] / old["visits_per_person"]),
        100.0 * math.log(new["test_lines_per_visit"] / old["test_lines_per_visit"]),
    ]
    total_log = 100.0 * math.log(new["test_lines"] / old["test_lines"])
    if abs(sum(log_components) - total_log) > 1e-9:
        raise AssertionError("IITGN log growth components do not sum to test-line log growth")
    return pd.DataFrame(rows)


def _city_tables(periods: dict[int, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame]:
    detail = []
    for year, frame in periods.items():
        grouped = frame.groupby("city", dropna=False, sort=True).agg(
            booking_rows=("booking_id", "size"),
            visits=("booking_id", "nunique"),
            people=("person_id", "nunique"),
            test_lines=("n_tests", "sum"),
        ).reset_index()
        grouped["visits_per_person"] = grouped["visits"] / grouped["people"]
        grouped["test_lines_per_visit"] = grouped["test_lines"] / grouped["visits"]
        grouped["period"] = f"H1_{year}"
        detail.append(grouped)
    long = pd.concat(detail, ignore_index=True)
    wide = long.pivot(index="city", columns="period", values=["booking_rows", "visits", "people", "test_lines", "visits_per_person", "test_lines_per_visit"])
    wide.columns = [f"{metric}_{period}" for metric, period in wide.columns]
    wide = wide.reset_index()
    for metric in ("booking_rows", "visits", "people", "test_lines", "visits_per_person", "test_lines_per_visit"):
        old_name, new_name = f"{metric}_H1_2025", f"{metric}_H1_2026"
        if old_name not in wide:
            wide[old_name] = 0
        if new_name not in wide:
            wide[new_name] = 0
        wide[f"{metric}_change"] = wide[new_name].fillna(0) - wide[old_name].fillna(0)
        wide[f"{metric}_change_pct"] = wide.apply(lambda row: _percent_change(row[new_name], row[old_name]) if row[old_name] else float("nan"), axis=1)
    total_change = float(wide["test_lines_change"].sum())
    wide["share_of_net_test_line_change_pct"] = wide["test_lines_change"] / total_change * 100.0 if total_change else float("nan")
    wide = wide.sort_values("test_lines_change", ascending=False).reset_index(drop=True)
    wide.insert(0, "rank_by_absolute_test_line_change", range(1, len(wide) + 1))
    return long, wide


def _channel_table(periods: dict[int, pd.DataFrame]) -> pd.DataFrame:
    records = []
    for year, frame in periods.items():
        grouped = frame.groupby(["system", "channel"], dropna=False, sort=True).agg(
            booking_records=("booking_id", "nunique"),
            test_lines=("n_tests", "sum"),
        ).reset_index()
        grouped["period"] = f"H1_{year}"
        records.append(grouped)
    long = pd.concat(records, ignore_index=True)
    wide = long.pivot(index=["system", "channel"], columns="period", values=["booking_records", "test_lines"]).fillna(0)
    wide.columns = [f"{metric}_{period}" for metric, period in wide.columns]
    wide = wide.reset_index()
    for metric in ("booking_records", "test_lines"):
        old_name, new_name = f"{metric}_H1_2025", f"{metric}_H1_2026"
        if old_name not in wide:
            wide[old_name] = 0
        if new_name not in wide:
            wide[new_name] = 0
        wide[f"{metric}_change"] = wide[new_name] - wide[old_name]
        wide[f"{metric}_change_pct"] = wide.apply(lambda row: _percent_change(row[new_name], row[old_name]) if row[old_name] else float("nan"), axis=1)
    return wide.sort_values(["system", "channel"]).reset_index(drop=True)


def _plan_comparison(
    actual: pd.DataFrame,
    plan: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    alias_actual = actual.assign(city_comparison=actual["source_city"].replace(CITY_ALIASES))
    exact_actual = actual.assign(city_comparison=actual["source_city"])
    alias_plan = plan.assign(city_comparison=plan["city"].replace(CITY_ALIASES))
    exact_plan = plan.assign(city_comparison=plan["city"])

    detail_frames = []
    summaries = []
    for scenario, act, tgt in (
        ("exact_source_labels", exact_actual, exact_plan),
        ("IITGN_Bangalore_to_Bengaluru_alias", alias_actual, alias_plan),
    ):
        left = act.groupby(["city_comparison", "month"], dropna=False, as_index=False).agg(actual_test_lines=("test_lines", "sum"))
        right = tgt.groupby(["city_comparison", "month"], dropna=False, as_index=False).agg(target_test_lines=("target_value", "sum"))
        _assert_unique(left, ["city_comparison", "month"], f"{scenario} actual city-month keys")
        _assert_unique(right, ["city_comparison", "month"], f"{scenario} plan city-month keys")
        merged = left.merge(right, on=["city_comparison", "month"], how="outer", indicator=True, validate="one_to_one")
        merged.insert(0, "scenario", scenario)
        merged["key_status"] = merged["_merge"].map({"both": "matched", "left_only": "actual_only", "right_only": "plan_only"})
        merged["actual_minus_target"] = merged["actual_test_lines"] - merged["target_test_lines"]
        merged["actual_vs_target_pct"] = merged.apply(
            lambda row: row["actual_minus_target"] / row["target_test_lines"] * 100.0
            if pd.notna(row["target_test_lines"]) and row["target_test_lines"] else float("nan"), axis=1
        )
        summaries.append({
            "scenario": scenario,
            "actual_city_month_keys": int(len(left)),
            "plan_city_month_keys": int(len(right)),
            "matched_city_month_keys": int((merged["_merge"] == "both").sum()),
            "actual_only_keys": int((merged["_merge"] == "left_only").sum()),
            "plan_only_keys": int((merged["_merge"] == "right_only").sum()),
            "actual_test_lines_all_keys": int(merged["actual_test_lines"].fillna(0).sum()),
            "target_test_lines_all_keys": int(merged["target_test_lines"].fillna(0).sum()),
            "matched_actual_test_lines": int(merged.loc[merged["_merge"] == "both", "actual_test_lines"].sum()),
            "matched_target_test_lines": int(merged.loc[merged["_merge"] == "both", "target_test_lines"].sum()),
            "matched_actual_minus_target": int(merged.loc[merged["_merge"] == "both", "actual_minus_target"].sum()),
            "matched_actual_vs_target_pct": (
                int(merged.loc[merged["_merge"] == "both", "actual_minus_target"].sum())
                / int(merged.loc[merged["_merge"] == "both", "target_test_lines"].sum()) * 100.0
                if (merged["_merge"] == "both").any() else float("nan")
            ),
        })
        detail_frames.append(merged.drop(columns="_merge"))

    detail = pd.concat(detail_frames, ignore_index=True)
    summary = pd.DataFrame(summaries)
    mapped = detail.loc[detail["scenario"] == "IITGN_Bangalore_to_Bengaluru_alias"].copy()
    city = mapped.groupby("city_comparison", dropna=False, as_index=False).agg(
        actual_test_lines=("actual_test_lines", "sum"),
        target_test_lines=("target_test_lines", "sum"),
        city_month_keys=("month", "nunique"),
    )
    city["actual_minus_target"] = city["actual_test_lines"] - city["target_test_lines"]
    city["actual_vs_target_pct"] = city.apply(
        lambda row: row["actual_minus_target"] / row["target_test_lines"] * 100.0 if row["target_test_lines"] else float("nan"), axis=1
    )
    city["share_of_total_target_gap_pct"] = city["actual_minus_target"] / city["actual_minus_target"].sum() * 100.0
    city = city.sort_values("actual_minus_target").reset_index(drop=True)
    return detail, summary, city


def run_brief_a_iitgn_alignment(
    project_root: Path | None = None,
    *,
    iitgn_clean_dir: Path | None = None,
    output_dir: Path | None = None,
) -> dict[str, Path]:
    """Recalculate Brief A using the cleaned bookings and prediction from IITGN Build 1."""
    started = perf_counter()
    project_root = Path(project_root) if project_root else Path(__file__).resolve().parents[2]
    clean_root = project_root.parent
    iitgn_clean_dir = Path(iitgn_clean_dir) if iitgn_clean_dir else clean_root / "iitgn-build1" / "data" / "clean"
    output_dir = Path(output_dir) if output_dir else project_root / "data" / "clean"
    output_dir.mkdir(parents=True, exist_ok=True)

    source_path = iitgn_clean_dir / "bookings_all.csv.gz"
    validated_path = iitgn_clean_dir / "bookings.csv.gz"
    clean_path = iitgn_clean_dir / "bookings_clean.csv.gz"
    source_city_path = project_root / "data" / "clean" / "bookings_source_rows.csv.gz"
    baseline_path = project_root / "data" / "clean" / "brief_a_metric_baseline_summary.csv"
    plan_path = project_root / "data" / "clean" / "plan_2026_H1_clean.csv"
    prior_recon_path = project_root / "data" / "clean" / "brief_a_driver_reconciliation.csv"
    for path in (source_path, validated_path, clean_path, source_city_path, baseline_path, plan_path, prior_recon_path):
        if not path.exists():
            raise FileNotFoundError(path)

    source = _read(source_path, usecols=["system", "booking_id", "slot_at", "city", "test_code"], dtypes={
        "system": "string", "booking_id": "string", "slot_at": "string", "city": "string", "test_code": "string",
    })
    validated = _read(validated_path, usecols=["system", "booking_id", "slot_at", "status_at_export", "n_tests"], dtypes={
        "system": "string", "booking_id": "string", "slot_at": "string", "status_at_export": "string", "n_tests": "string",
    })
    bookings = _read(clean_path, usecols=[
        "system", "booking_id", "slot_at", "city", "channel", "patient_id", "person_id", "n_tests", "status_at_export",
    ], dtypes={
        "system": "string", "booking_id": "string", "slot_at": "string", "city": "string", "channel": "string",
        "patient_id": "string", "person_id": "string", "n_tests": "string", "status_at_export": "string",
    })
    source_city_lines = _read(source_city_path, usecols=["system", "booking_id", "slot_at", "city", "test_code"], dtypes={
        "system": "string", "booking_id": "string", "slot_at": "string", "city": "string", "test_code": "string",
    })
    baseline = _read(baseline_path, dtypes={"metric": "string", "date_anchor": "string", "comparison_status": "string", "notes": "string"})
    prior_recon = _read(prior_recon_path, dtypes={"step": "string", "period": "string", "reason": "string"})
    plan = _read(plan_path, usecols=["city", "month", "target_value"], dtypes={"city": "string", "month": "string", "target_value": "string"})

    for frame in (source, validated, bookings):
        frame["_slot_date"] = _local_date(frame["slot_at"])
        if frame["_slot_date"].isna().any():
            raise ValueError("A booking table contains a blank or unparseable slot_at local date")
    source_city_lines["_slot_date"] = _local_date(source_city_lines["slot_at"])
    source["_test_code_nonblank"] = source["test_code"].astype("string").str.strip().ne("")
    source_city_lines["_test_code_nonblank"] = source_city_lines["test_code"].astype("string").str.strip().ne("")
    for frame in (validated, bookings):
        frame["n_tests"] = pd.to_numeric(frame["n_tests"], errors="raise").astype("int64")
    plan["target_value"] = pd.to_numeric(plan["target_value"], errors="raise").astype("int64")

    _assert_unique(validated, KEY, "IITGN validated bookings")
    _assert_unique(bookings, KEY, "IITGN cleaned bookings")
    _assert_unique(bookings, ["booking_id"], "IITGN cleaned booking_id")
    if (bookings["booking_id"].eq("") | bookings["person_id"].eq("") | bookings["patient_id"].eq("")).any():
        raise ValueError("IITGN cleaned booking identity fields contain blanks")
    if (bookings["n_tests"] <= 0).any():
        raise ValueError("IITGN clean bookings contain zero/negative n_tests")
    if bookings["status_at_export"].eq("rescheduled").any():
        raise ValueError("IITGN clean table still contains rows marked rescheduled")

    stored_slot = baseline.loc[baseline["metric"].str.startswith("Booked source test-code lines, slot date"), :]
    if len(stored_slot) != 1:
        raise ValueError("Expected one stored 05a slot-date baseline row")
    stored_2026 = int(stored_slot.iloc[0]["numerator"])
    stored_2025 = int(stored_slot.iloc[0]["denominator"])

    periods: dict[int, pd.DataFrame] = {}
    valid_periods: dict[int, pd.DataFrame] = {}
    source_periods: dict[int, pd.DataFrame] = {}
    recon_rows = []
    checkpoint_rows = []
    for year in YEARS:
        raw_h1 = _period(source, year)
        valid_h1 = _period(validated, year)
        clean_h1 = _period(bookings, year)
        source_periods[year] = raw_h1
        valid_periods[year] = valid_h1
        periods[year] = clean_h1

        raw_nonblank = raw_h1.loc[raw_h1["_test_code_nonblank"]].copy()
        accepted_keys = valid_h1[KEY].drop_duplicates()
        line_join = raw_nonblank.merge(accepted_keys, on=KEY, how="left", indicator=True, validate="many_to_one")
        accepted_raw_lines = int(line_join["_merge"].eq("both").sum())
        rejected_lines = int(line_join["_merge"].eq("left_only").sum())
        validated_test_lines = int(valid_h1["n_tests"].sum())
        if accepted_raw_lines != validated_test_lines:
            raise AssertionError(f"{year} accepted source line count {accepted_raw_lines} != validated n_tests {validated_test_lines}")

        superseded = valid_h1["status_at_export"].eq("rescheduled")
        superseded_records = int(superseded.sum())
        superseded_lines = int(valid_h1.loc[superseded, "n_tests"].sum())
        clean_lines = int(clean_h1["n_tests"].sum())
        clean_records = int(len(clean_h1))
        if validated_test_lines - superseded_lines != clean_lines:
            raise AssertionError(f"{year} validation/reschedule test-line reconciliation failed")
        if len(valid_h1) - superseded_records != clean_records:
            raise AssertionError(f"{year} validation/reschedule booking reconciliation failed")

        blank_rows = int((~raw_h1["_test_code_nonblank"]).sum())
        source_rows = int(len(raw_h1))
        if source_rows != blank_rows + rejected_lines + superseded_lines + clean_lines:
            raise AssertionError(f"{year} source = classified blank + rejected + superseded + kept test lines failed")

        recon_rows.append({
            "period": f"H1 {year}",
            "source_rows_including_blank_test_code": source_rows,
            "blank_test_code_rows_classified": blank_rows,
            "nonblank_source_test_lines": int(len(raw_nonblank)),
            "validation_rejected_test_lines": rejected_lines,
            "validated_test_lines_before_reschedule_rule": validated_test_lines,
            "superseded_records_removed": superseded_records,
            "test_lines_on_superseded_records_removed": superseded_lines,
            "retained_booking_records": clean_records,
            "retained_test_lines_primary": clean_lines,
            "source_rows_reconcile": source_rows == blank_rows + rejected_lines + superseded_lines + clean_lines,
        })

        stored_source = stored_2025 if year == 2025 else stored_2026
        period_label = f"H1 {year}"
        previous_reconciliation = prior_recon.loc[prior_recon["period"].eq(period_label)]
        if len(previous_reconciliation) != 1:
            raise ValueError(f"Expected one stored source reconciliation row for {period_label}")
        previous_source_rows = int(previous_reconciliation.iloc[0]["input_rows"])
        previous_blank_rows = int(previous_reconciliation.iloc[0]["classified_blank_or_whitespace_test_code_rows"])
        checkpoint_rows.append({
            "period": period_label,
            "stored_05a_nonblank_source_test_lines": stored_source,
            "recounted_iitgn_source_nonblank_test_lines": int(len(raw_nonblank)),
            "difference": int(len(raw_nonblank)) - stored_source,
            "checkpoint_matches": int(len(raw_nonblank)) == stored_source,
            "previous_build_source_rows_including_blank_code": previous_source_rows,
            "IITGN_flattened_source_rows_including_blank_code": source_rows,
            "difference_in_all_source_rows": source_rows - previous_source_rows,
            "previous_build_blank_code_rows": previous_blank_rows,
            "IITGN_flattened_blank_code_rows": blank_rows,
            "difference_in_blank_code_rows": blank_rows - previous_blank_rows,
            "IITGN_clean_test_lines_after_validation_and_reschedule_rule": clean_lines,
            "change_from_05a_candidate": clean_lines - stored_source,
        })

    if not all(row["checkpoint_matches"] for row in checkpoint_rows):
        raise AssertionError("The IITGN raw-line recount does not match the stored 05a checkpoint")

    source_city_lines["booking_id_trimmed"] = source_city_lines["booking_id"].str.strip()
    source["booking_id_trimmed"] = source["booking_id"].str.strip()
    source_copy_rows = []
    for year in YEARS:
        kalpa_h1 = _period(source_city_lines, year)
        iitgn_h1 = _period(source, year)
        kalpa_keys = kalpa_h1[["system", "booking_id_trimmed"]].drop_duplicates()
        iitgn_keys = iitgn_h1[["system", "booking_id_trimmed"]].drop_duplicates()
        key_comparison = kalpa_keys.merge(
            iitgn_keys,
            on=["system", "booking_id_trimmed"],
            how="outer",
            indicator=True,
            validate="one_to_one",
        )
        kalpa_only = key_comparison.loc[key_comparison["_merge"].eq("left_only"), ["system", "booking_id_trimmed"]]
        iitgn_only = key_comparison.loc[key_comparison["_merge"].eq("right_only"), ["system", "booking_id_trimmed"]]
        kalpa_only_rows = kalpa_h1.merge(kalpa_only, on=["system", "booking_id_trimmed"], how="inner", validate="many_to_one")
        iitgn_only_rows = iitgn_h1.merge(iitgn_only, on=["system", "booking_id_trimmed"], how="inner", validate="many_to_one")
        source_copy_rows.append({
            "period": f"H1 {year}",
            "kalpa_source_rows": int(len(kalpa_h1)),
            "iitgn_flattened_rows": int(len(iitgn_h1)),
            "kalpa_nonblank_test_code_lines": int(kalpa_h1["_test_code_nonblank"].sum()),
            "iitgn_nonblank_test_code_lines": int(iitgn_h1["_test_code_nonblank"].sum()),
            "kalpa_blank_test_code_rows": int((~kalpa_h1["_test_code_nonblank"]).sum()),
            "iitgn_blank_test_code_rows": int((~iitgn_h1["_test_code_nonblank"]).sum()),
            "kalpa_only_booking_keys": int(len(kalpa_only)),
            "iitgn_only_booking_keys": int(len(iitgn_only)),
            "nonblank_lines_on_kalpa_only_keys": int(kalpa_only_rows["_test_code_nonblank"].sum()),
            "nonblank_lines_on_iitgn_only_keys": int(iitgn_only_rows["_test_code_nonblank"].sum()),
            "kalpa_only_keys_all_blank_code": bool(len(kalpa_only) > 0 and not kalpa_only_rows["_test_code_nonblank"].any()),
        })
    for row in source_copy_rows:
        if row["kalpa_nonblank_test_code_lines"] != row["iitgn_nonblank_test_code_lines"]:
            raise AssertionError(f"{row['period']} source copies disagree on nonblank test-code lines")
        if row["kalpa_only_booking_keys"] and not row["kalpa_only_keys_all_blank_code"]:
            raise AssertionError(f"{row['period']} kalpa-only source keys contain nonblank test-code rows")

    metric_rows = [_tree_metrics(periods[year], f"H1 {year}") for year in YEARS]
    metric_by_year = {year: metric_rows[index] for index, year in enumerate(YEARS)}
    old, new = metric_by_year[2025], metric_by_year[2026]
    total_pct = _percent_change(new["test_lines"], old["test_lines"])
    log_components = [
        math.log(new["distinct_person_ids"] / old["distinct_person_ids"]),
        math.log(new["visits_per_person"] / old["visits_per_person"]),
        math.log(new["test_lines_per_visit"] / old["test_lines_per_visit"]),
    ]
    total_log = math.log(new["test_lines"] / old["test_lines"])
    if abs(sum(log_components) - total_log) > 1e-9:
        raise AssertionError("The identity's log changes do not reconcile to total test-line log growth")
    summary_rows = []
    for row in metric_rows:
        row["year_over_year_test_line_growth_pct"] = total_pct
        row["test_line_difference_vs_H1_2025"] = int(new["test_lines"] - old["test_lines"])
        row["total_log_growth_pct"] = 100.0 * total_log
        row["person_log_growth_pct"] = 100.0 * log_components[0]
        row["visits_per_person_log_growth_pct"] = 100.0 * log_components[1]
        row["test_lines_per_visit_log_growth_pct"] = 100.0 * log_components[2]
        summary_rows.append(row)

    component_table = _component_rows(metric_by_year)
    city_long, city_changes = _city_tables(periods)
    channel_changes = _channel_table(periods)
    if int(city_long.loc[city_long["period"] == "H1_2025", "test_lines"].sum()) != old["test_lines"]:
        raise AssertionError("H1 2025 city totals do not reconcile to overall test lines")
    if int(city_long.loc[city_long["period"] == "H1_2026", "test_lines"].sum()) != new["test_lines"]:
        raise AssertionError("H1 2026 city totals do not reconcile to overall test lines")
    if int(channel_changes["test_lines_H1_2025"].sum()) != old["test_lines"] or int(channel_changes["test_lines_H1_2026"].sum()) != new["test_lines"]:
        raise AssertionError("System/channel groups do not reconcile to overall test lines")

    # Restore the original city label from kalpa_healt-derived source rows.
    # IITGN's Booking contract strips outer whitespace from IDs, so profile the
    # exact join first and use that documented normalization only for this audit.
    source_city_lines["booking_id_trimmed"] = source_city_lines["booking_id"].str.strip()
    city_sources_exact = source_city_lines.groupby(KEY, dropna=False, as_index=False).agg(
        source_city=("city", "first"),
        source_city_labels=("city", "nunique"),
        source_slot_dates=("_slot_date", "nunique"),
        source_local_slot_date=("_slot_date", "first"),
        source_test_rows=("city", "size"),
    )
    city_sources = source_city_lines.groupby(["system", "booking_id_trimmed"], dropna=False, as_index=False).agg(
        source_city=("city", "first"),
        source_city_labels=("city", "nunique"),
        source_slot_dates=("_slot_date", "nunique"),
        source_local_slot_date=("_slot_date", "first"),
        source_test_rows=("city", "size"),
        source_booking_id_forms=("booking_id", "nunique"),
    )
    if (city_sources_exact["source_city_labels"] != 1).any() or (city_sources["source_city_labels"] != 1).any():
        raise ValueError("A source booking key has inconsistent city labels across test rows")
    if (city_sources_exact["source_slot_dates"] > 1).any() or (city_sources["source_slot_dates"] > 1).any():
        raise ValueError("A source booking key has inconsistent local slot dates across test rows")
    trim_key_collisions = int(city_sources["source_booking_id_forms"].gt(1).sum())
    if trim_key_collisions:
        raise ValueError(f"Trimming source booking IDs merges {trim_key_collisions:,} distinct source IDs")
    _assert_unique(city_sources_exact, KEY, "exact source city-by-booking table")
    _assert_unique(city_sources, ["system", "booking_id_trimmed"], "trimmed source city-by-booking table")
    exact_city_join = bookings.merge(city_sources_exact, on=KEY, how="left", indicator=True, validate="one_to_one")
    clean_for_city_join = bookings.assign(booking_id_trimmed=bookings["booking_id"].str.strip())
    city_join = clean_for_city_join.merge(
        city_sources,
        on=["system", "booking_id_trimmed"],
        how="left",
        indicator=True,
        validate="one_to_one",
    )
    if not city_join["_merge"].eq("both").all():
        raise AssertionError("Some IITGN clean bookings have no source-city key after the documented ID trim")
    if (city_join["source_slot_dates"] != 1).any() or not city_join["source_local_slot_date"].eq(city_join["_slot_date"]).all():
        raise AssertionError("A retained IITGN booking does not have one matching local slot date in the kalpa_healt source rows")
    city_join["expected_iitgn_city"] = city_join["source_city"].replace(CITY_ALIASES)
    city_join["model_city_matches_alias_rule"] = city_join["expected_iitgn_city"].eq(city_join["city"])
    if not city_join["model_city_matches_alias_rule"].all():
        raise AssertionError("IITGN clean city differs from source-city label beyond the documented alias")
    city_join["analysis_period"] = "outside_H1"
    for year in YEARS:
        mask = (city_join["_slot_date"] >= pd.Timestamp(f"{year}-01-01")) & (city_join["_slot_date"] < pd.Timestamp(f"{year}-07-01"))
        city_join.loc[mask, "analysis_period"] = f"H1_{year}"
    alias_evidence = city_join.loc[city_join["analysis_period"].ne("outside_H1")].groupby(
        ["analysis_period", "source_city", "city"], dropna=False, as_index=False
    ).agg(retained_booking_records=("booking_id", "size"), retained_test_lines=("n_tests", "sum"))
    alias_evidence["mapping_applied"] = alias_evidence["source_city"].ne(alias_evidence["city"])
    identity_checks = pd.DataFrame([{
        "source_table": "build1-starter-kit/data/clean/bookings_source_rows.csv.gz (loaded from kalpa_healt datapack)",
        "clean_table": "iitgn-build1/data/clean/bookings_clean.csv.gz",
        "source_rows_with_outer_whitespace_booking_id": int(source_city_lines["booking_id"].ne(source_city_lines["booking_id_trimmed"]).sum()),
        "distinct_source_keys_with_outer_whitespace_booking_id": int(source_city_lines.loc[source_city_lines["booking_id"].ne(source_city_lines["booking_id_trimmed"]), KEY].drop_duplicates().shape[0]),
        "distinct_source_ids_merged_by_trim": trim_key_collisions,
        "clean_bookings_matched_exact_system_booking_id": int(exact_city_join["_merge"].eq("both").sum()),
        "clean_bookings_unmatched_exact_system_booking_id": int(exact_city_join["_merge"].eq("left_only").sum()),
        "clean_bookings_matched_after_iitgn_str_strip_whitespace_rule": int(city_join["_merge"].eq("both").sum()),
        "clean_bookings_unmatched_after_trim": int(city_join["_merge"].eq("left_only").sum()),
        "city_mappings_changed_by_iitgn_model": int(city_join["source_city"].ne(city_join["city"]).sum()),
        "changed_city_mapping_rows_match_Bangalore_to_Bengaluru": bool(city_join["model_city_matches_alias_rule"].all()),
        "IDs_modified_in_clean_booking_table_by_this_helper": False,
    }])

    h26 = city_join.loc[(city_join["_slot_date"] >= pd.Timestamp("2026-01-01")) & (city_join["_slot_date"] < pd.Timestamp("2026-07-01"))].copy()
    h26["month"] = h26["_slot_date"].dt.to_period("M").astype("string")
    actual_by_source = h26.groupby(["source_city", "month"], dropna=False, as_index=False).agg(test_lines=("n_tests", "sum"))
    plan_copy = plan.copy()
    plan_copy["month"] = plan_copy["month"].astype("string")
    _assert_unique(plan_copy, ["city", "month"], "plan city-month keys")
    plan_detail, plan_summary, plan_city = _plan_comparison(actual_by_source, plan_copy)
    if int(plan_summary.loc[plan_summary["scenario"] == "IITGN_Bangalore_to_Bengaluru_alias", "matched_city_month_keys"].iloc[0]) != 36:
        raise AssertionError("The IITGN alias comparison did not match all 36 plan city-month keys")

    # Reproduce the notebook's endpoint exactly, then show what the full calendar
    # periods add after midnight on June 30.
    boundary_rows = []
    for year in YEARS:
        dt = pd.to_datetime(bookings["slot_at"].astype("string").str.slice(0, 19), format="%Y-%m-%dT%H:%M:%S", errors="coerce")
        if dt.isna().any():
            # Accept source timestamps using a space separator as well.
            dt = pd.to_datetime(bookings["slot_at"].astype("string").str.slice(0, 19), format="mixed", errors="coerce")
        h = periods[year]
        h_dt = dt.loc[h.index]
        as_coded = h.loc[h_dt.between(f"{year}-01-01", f"{year}-06-30", inclusive="both")]
        full_lines = int(h["n_tests"].sum())
        coded_lines = int(as_coded["n_tests"].sum())
        boundary_rows.append({
            "period": f"H1 {year}",
            "full_calendar_half_year_booking_records": int(len(h)),
            "full_calendar_half_year_test_lines": full_lines,
            "notebook_06_as_coded_booking_records": int(len(as_coded)),
            "notebook_06_as_coded_test_lines": coded_lines,
            "June_30_after_midnight_booking_records_omitted": int(len(h) - len(as_coded)),
            "June_30_after_midnight_test_lines_omitted": full_lines - coded_lines,
        })

    h_valid_2026 = valid_periods[2026]
    h_clean_2026 = periods[2026]
    h_raw_2026 = source_periods[2026]
    valid_key_h26 = h_valid_2026[KEY].drop_duplicates()
    clean_key_h26 = h_clean_2026[KEY].drop_duplicates()
    raw_city_h26 = city_sources.loc[
        (city_sources["source_local_slot_date"] >= pd.Timestamp("2026-01-01"))
        & (city_sources["source_local_slot_date"] < pd.Timestamp("2026-07-01"))
    ]
    raw_city_key_count = len(raw_city_h26)
    source_line_key_counts = h_raw_2026.groupby(KEY, dropna=False).size()
    audit_rows = [
        {
            "left_table": "IITGN raw H1 2026 nonblank source test lines",
            "right_table": "IITGN validated H1 2026 booking keys",
            "key": "system + booking_id",
            "join_type": "LEFT",
            "expected_cardinality": "many_to_one; raw rows are test-line grain",
            "left_rows": int(h_raw_2026["_test_code_nonblank"].sum()),
            "right_rows": int(len(valid_key_h26)),
            "rows_after": int(h_raw_2026["_test_code_nonblank"].sum()),
            "matched_left_rows": int(recon_rows[1]["validated_test_lines_before_reschedule_rule"]),
            "unmatched_left_rows": int(recon_rows[1]["validation_rejected_test_lines"]),
            "unmatched_right_rows": 0,
            "duplicate_left_key_rows_expected_at_test_line_grain": int(h_raw_2026.loc[h_raw_2026["_test_code_nonblank"]].duplicated(KEY, keep=False).sum()),
            "duplicate_right_keys": int(valid_key_h26.duplicated(KEY).sum()),
        },
        {
            "left_table": "IITGN accepted H1 2026 bookings before superseded-record rule",
            "right_table": "IITGN retained H1 2026 clean bookings",
            "key": "system + booking_id",
            "join_type": "LEFT",
            "expected_cardinality": "one_to_one",
            "left_rows": int(len(h_valid_2026)),
            "right_rows": int(len(h_clean_2026)),
            "rows_after": int(len(h_valid_2026)),
            "matched_left_rows": int(len(clean_key_h26)),
            "unmatched_left_rows": int(len(h_valid_2026) - len(clean_key_h26)),
            "unmatched_right_rows": 0,
            "duplicate_left_key_rows_expected_at_test_line_grain": 0,
            "duplicate_right_keys": int(clean_key_h26.duplicated(KEY).sum()),
        },
        {
            "left_table": "IITGN full clean bookings",
            "right_table": "kalpa_healt source city grouped by exact booking key",
            "key": "system + booking_id",
            "join_type": "LEFT",
            "expected_cardinality": "one_to_one after grouping raw source test rows to booking key",
            "left_rows": int(len(bookings)),
            "right_rows": int(len(city_sources_exact)),
            "rows_after": int(len(bookings)),
            "matched_left_rows": int(exact_city_join["_merge"].eq("both").sum()),
            "unmatched_left_rows": int(exact_city_join["_merge"].eq("left_only").sum()),
            "unmatched_right_rows": int((~city_sources_exact.set_index(KEY).index.isin(bookings.set_index(KEY).index)).sum()),
            "duplicate_left_key_rows_expected_at_test_line_grain": 0,
            "duplicate_right_keys": int(city_sources_exact.duplicated(KEY).sum()),
        },
        {
            "left_table": "IITGN full clean bookings",
            "right_table": "kalpa_healt source city grouped by IITGN-trimmed booking key",
            "key": "system + booking_id.str.strip()",
            "join_type": "LEFT",
            "expected_cardinality": "one_to_one after checking there are no normalized key collisions",
            "left_rows": int(len(bookings)),
            "right_rows": int(len(city_sources)),
            "rows_after": int(len(bookings)),
            "matched_left_rows": int(city_join["_merge"].eq("both").sum()),
            "unmatched_left_rows": int(city_join["_merge"].eq("left_only").sum()),
            "unmatched_right_rows": int(len(city_sources) - city_join["_merge"].eq("both").sum()),
            "duplicate_left_key_rows_expected_at_test_line_grain": 0,
            "duplicate_right_keys": int(city_sources.duplicated(["system", "booking_id_trimmed"]).sum()),
        },
    ]
    for _, row in plan_summary.iterrows():
        scenario_rows = plan_detail.loc[plan_detail["scenario"] == row["scenario"]]
        audit_rows.append({
            "left_table": f"IITGN H1 2026 actual city-months ({row['scenario']})",
            "right_table": f"H1 2026 plan city-months ({row['scenario']})",
            "key": "city + month",
            "join_type": "FULL OUTER",
            "expected_cardinality": "one_to_one",
            "left_rows": int(row["actual_city_month_keys"]),
            "right_rows": int(row["plan_city_month_keys"]),
            "rows_after": int(len(scenario_rows)),
            "matched_left_rows": int(row["matched_city_month_keys"]),
            "unmatched_left_rows": int(row["actual_only_keys"]),
            "unmatched_right_rows": int(row["plan_only_keys"]),
            "duplicate_left_key_rows_expected_at_test_line_grain": 0,
            "duplicate_right_keys": 0,
        })

    plan_full = plan_summary.loc[plan_summary["scenario"] == "IITGN_Bangalore_to_Bengaluru_alias"].iloc[0]
    plan_growth = _percent_change(int(plan["target_value"].sum()), int(old["test_lines"]))
    actual_plan_gap_pct = (int(new["test_lines"]) - int(plan["target_value"].sum())) / int(plan["target_value"].sum()) * 100.0
    implied_growth_gap_pp = total_pct - plan_growth
    metadata = pd.DataFrame([{
        "helper": "kalpa.brief_a_iitgn_alignment.run_brief_a_iitgn_alignment",
        "elapsed_seconds": round(perf_counter() - started, 3),
        "source_booking_lines": str(source_path),
        "source_city_rows_for_alias_validation": str(source_city_path),
        "validated_bookings": str(validated_path),
        "iitgn_clean_bookings": str(clean_path),
        "plan_table": str(plan_path),
        "period_rule": "local slot_at date; half-open [Jan 1, Jul 1) for each H1",
        "test_unit": "sum(n_tests) on IITGN validated bookings after status_at_export=rescheduled records were removed",
        "plan_target_total": int(plan["target_value"].sum()),
        "actual_vs_plan_gap": int(new["test_lines"] - plan["target_value"].sum()),
        "actual_vs_plan_gap_pct_of_target": actual_plan_gap_pct,
        "plan_implied_growth_from_H1_2025_pct": plan_growth,
        "actual_growth_minus_plan_implied_growth_pp": implied_growth_gap_pp,
        "source_raw_files_modified": False,
        "full_cleaning_pipeline_run": False,
    }])

    outputs = {
        "brief_a_iitgn_metric_summary.csv": pd.DataFrame(summary_rows),
        "brief_a_iitgn_component_changes.csv": component_table,
        "brief_a_iitgn_city_drivers.csv": city_long,
        "brief_a_iitgn_city_contributions.csv": city_changes,
        "brief_a_iitgn_channel_contributions.csv": channel_changes,
        "brief_a_iitgn_plan_city_month.csv": plan_detail,
        "brief_a_iitgn_plan_city_summary.csv": plan_summary,
        "brief_a_iitgn_plan_city_contributions.csv": plan_city,
        "brief_a_iitgn_reconciliation.csv": pd.DataFrame(recon_rows),
        "brief_a_iitgn_checkpoint_verification.csv": pd.DataFrame(checkpoint_rows),
        "brief_a_iitgn_source_copy_comparison.csv": pd.DataFrame(source_copy_rows),
        "brief_a_iitgn_boundary_sensitivity.csv": pd.DataFrame(boundary_rows),
        "brief_a_iitgn_city_alias_evidence.csv": alias_evidence,
        "brief_a_iitgn_identity_checks.csv": identity_checks,
        "brief_a_iitgn_join_audit.csv": pd.DataFrame(audit_rows),
        "brief_a_iitgn_run_metadata.csv": metadata,
    }
    paths: dict[str, Path] = {}
    for filename, frame in outputs.items():
        if filename == "brief_a_iitgn_run_metadata.csv":
            continue
        path = output_dir / filename
        frame.to_csv(path, index=False)
        paths[filename] = path
    metadata["elapsed_seconds"] = round(perf_counter() - started, 3)
    metadata_path = output_dir / "brief_a_iitgn_run_metadata.csv"
    metadata.to_csv(metadata_path, index=False)
    paths["brief_a_iitgn_run_metadata.csv"] = metadata_path

    # Headline and audit contracts needed by the downstream report.
    if int(old["test_lines"]) != 433611 or int(new["test_lines"]) != 455383:
        raise AssertionError("The IITGN-aligned H1 headline differs from the verified clean-table values")
    if int(plan_full["matched_actual_minus_target"]) != int(new["test_lines"] - plan["target_value"].sum()):
        raise AssertionError("Mapped city-month plan totals do not reconcile to the overall plan gap")
    if (pd.DataFrame(audit_rows)["duplicate_right_keys"] != 0).any():
        raise AssertionError("A right-side join key is duplicated")
    return paths
