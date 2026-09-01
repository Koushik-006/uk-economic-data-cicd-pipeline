"""Load validated observations into durable outputs."""

import sqlite3
from pathlib import Path

import pandas as pd


def load_outputs(frame: pd.DataFrame, output_dir: str | Path) -> tuple[Path, Path]:
    """Write a consolidated CSV and atomically replace the SQLite table."""
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    csv_path = destination / "uk_economic_indicators.csv"
    database_path = destination / "economic_data.db"
    frame.to_csv(csv_path, index=False)
    with sqlite3.connect(database_path) as connection:
        frame.to_sql("economic_indicators", connection, if_exists="replace", index=False)
    return csv_path, database_path

