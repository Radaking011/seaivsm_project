"""Basic data-quality checks for the normalized event-log format."""

import pandas as pd
from src.config import REQUIRED_COLUMNS


def validate_event_log(df: pd.DataFrame) -> list[str]:
    errors: list[str] = []

    missing_columns = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {missing_columns}")
        return errors

    if df.empty:
        errors.append("The event log contains no rows.")
        return errors

    if df["case_id"].isna().any():
        errors.append("case_id contains missing values.")
    if df["activity"].isna().any():
        errors.append("activity contains missing values.")

    start = pd.to_datetime(df["start_time"], errors="coerce")
    end = pd.to_datetime(df["end_time"], errors="coerce")

    if start.isna().any() or end.isna().any():
        errors.append("Some start_time or end_time values are invalid.")
    else:
        if (end < start).any():
            errors.append("Some events end before they start.")

    duration = pd.to_numeric(df["duration_minutes"], errors="coerce")
    if duration.isna().any() or (duration < 0).any():
        errors.append("duration_minutes must be numeric and non-negative.")

    return errors
