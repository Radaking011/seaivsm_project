"""Initial VSM metrics. Definitions will be refined against the selected plant data."""

import pandas as pd


def calculate_order_metrics(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work["start_time"] = pd.to_datetime(work["start_time"])
    work["end_time"] = pd.to_datetime(work["end_time"])

    result = (
        work.groupby("case_id", as_index=False)
        .agg(
            order_start=("start_time", "min"),
            order_finish=("end_time", "max"),
            total_processing_minutes=("duration_minutes", "sum"),
            activity_count=("activity", "count"),
            rework_events=("is_rework", "sum"),
        )
    )
    result["lead_time_minutes"] = (
        result["order_finish"] - result["order_start"]
    ).dt.total_seconds() / 60
    result["waiting_time_estimate_minutes"] = (
        result["lead_time_minutes"] - result["total_processing_minutes"]
    ).clip(lower=0)
    result["process_cycle_efficiency_pct"] = (
        result["total_processing_minutes"]
        / result["lead_time_minutes"].replace(0, pd.NA)
        * 100
    )
    return result


def calculate_activity_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("activity", as_index=False)
        .agg(
            event_count=("event_id", "count"),
            mean_cycle_time_min=("duration_minutes", "mean"),
            median_cycle_time_min=("duration_minutes", "median"),
            std_cycle_time_min=("duration_minutes", "std"),
            total_processing_min=("duration_minutes", "sum"),
            rework_count=("is_rework", "sum"),
        )
        .sort_values("mean_cycle_time_min", ascending=False)
    )
