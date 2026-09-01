import pandas as pd
import pytest

from src.transform import transform_dataset


def test_transform_dataset_normalizes_and_deduplicates():
    source = pd.DataFrame({"date": ["2025-01-01", "2025-01-01"], "value": [1, 2]})
    result = transform_dataset(source, "gdp", "index")
    assert result.to_dict("records") == [
        {"dataset": "gdp", "date": pd.Timestamp("2025-01-01").date(), "value": 2, "unit": "index"}
    ]


def test_transform_dataset_rejects_missing_columns():
    with pytest.raises(ValueError, match="value"):
        transform_dataset(pd.DataFrame({"date": ["2025-01-01"]}), "gdp", "index")
