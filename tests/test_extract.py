import pandas as pd
import pytest

from src.extract import extract_dataset, load_config


def test_extract_dataset_reads_csv(tmp_path):
    source = tmp_path / "sample.csv"
    pd.DataFrame({"date": ["2025-01-01"], "value": [1.2]}).to_csv(source, index=False)
    assert extract_dataset(source).to_dict("records") == [{"date": "2025-01-01", "value": 1.2}]


def test_extract_dataset_rejects_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        extract_dataset(tmp_path / "missing.csv")


def test_load_config_reads_valid_yaml(tmp_path):
    config = tmp_path / "datasets.yml"
    config.write_text("datasets:\n  - name: gdp\n", encoding="utf-8")
    assert load_config(config)["datasets"][0]["name"] == "gdp"


def test_load_config_rejects_missing_datasets(tmp_path):
    config = tmp_path / "datasets.yml"
    config.write_text("output_dir: output\n", encoding="utf-8")
    with pytest.raises(ValueError, match="at least one"):
        load_config(config)


def test_extract_dataset_rejects_empty_csv(tmp_path):
    source = tmp_path / "empty.csv"
    source.write_text("date,value\n", encoding="utf-8")
    with pytest.raises(ValueError, match="empty"):
        extract_dataset(source)
