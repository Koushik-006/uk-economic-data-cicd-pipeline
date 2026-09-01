import pandas as pd
import pytest

from src.validate import validate_dataset


def test_validate_dataset_accepts_valid_frame():
    frame = pd.DataFrame({"dataset": ["gdp"], "date": ["2025-01-01"], "value": [1.0], "unit": ["index"]})
    validate_dataset(frame)


def test_validate_dataset_rejects_nulls():
    frame = pd.DataFrame({"dataset": ["gdp"], "date": ["2025-01-01"], "value": [None], "unit": ["index"]})
    with pytest.raises(ValueError, match="null"):
        validate_dataset(frame)


@pytest.mark.parametrize(
    ("frame", "message"),
    [
        (pd.DataFrame(columns=["dataset", "date", "value", "unit"]), "at least one"),
        (pd.DataFrame({"dataset": ["gdp", "gdp"], "date": ["2025-01-01"] * 2, "value": [1.0, 2.0], "unit": ["index"] * 2}), "duplicate"),
        (pd.DataFrame({"dataset": ["gdp"], "date": ["2025-01-01"], "value": ["bad"], "unit": ["index"]}), "numeric"),
        (pd.DataFrame({"dataset": ["gdp"]}), "Missing columns"),
    ],
)
def test_validate_dataset_rejects_contract_violations(frame, message):
    with pytest.raises(ValueError, match=message):
        validate_dataset(frame)

