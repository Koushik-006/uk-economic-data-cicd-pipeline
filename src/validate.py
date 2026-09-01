"""Data-quality checks applied before loading."""

import pandas as pd


def validate_dataset(frame: pd.DataFrame) -> None:
    """Raise ValueError when the normalized dataset violates its contract."""
    required = ["dataset", "date", "value", "unit"]
    missing = set(required).difference(frame.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    if frame.empty:
        raise ValueError("Dataset must contain at least one row")
    if frame[required].isna().any().any():
        raise ValueError("Required fields cannot contain null values")
    if frame.duplicated(["dataset", "date"]).any():
        raise ValueError("Dataset contains duplicate observations")
    if not pd.api.types.is_numeric_dtype(frame["value"]):
        raise ValueError("Values must be numeric")

