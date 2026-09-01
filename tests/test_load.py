import sqlite3

import pandas as pd

from src.load import load_outputs


def test_load_outputs_writes_csv_and_database(tmp_path):
    frame = pd.DataFrame({"dataset": ["gdp"], "date": ["2025-01-01"], "value": [1.0], "unit": ["index"]})
    csv_path, database_path = load_outputs(frame, tmp_path / "processed")

    assert pd.read_csv(csv_path).shape == (1, 4)
    with sqlite3.connect(database_path) as connection:
        count = connection.execute("SELECT COUNT(*) FROM economic_indicators").fetchone()[0]
    assert count == 1

