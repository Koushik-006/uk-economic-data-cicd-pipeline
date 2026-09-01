"""Transform source datasets into a consistent analytical shape."""

import pandas as pd


def transform_dataset(frame: pd.DataFrame, name: str, unit: str) -> pd.DataFrame:
    """Normalize dates and values and add dataset metadata."""
    required = {"date", "value"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    result = frame.loc[:, ["date", "value"]].copy()
    result["date"] = pd.to_datetime(result["date"], errors="raise").dt.date
    result["value"] = pd.to_numeric(result["value"], errors="raise")
    result.insert(0, "dataset", name)
    result["unit"] = unit
    return result.sort_values("date").drop_duplicates(["dataset", "date"], keep="last")

