"""Extract configured CSV datasets from disk."""

from pathlib import Path

import pandas as pd
import yaml


def load_config(path: str | Path) -> dict:
    """Load and minimally validate the dataset configuration."""
    with Path(path).open(encoding="utf-8") as stream:
        config = yaml.safe_load(stream)
    if not isinstance(config, dict) or not config.get("datasets"):
        raise ValueError("Configuration must define at least one dataset")
    return config


def extract_dataset(path: str | Path) -> pd.DataFrame:
    """Read one CSV file, failing clearly when it is missing or empty."""
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(f"Dataset not found: {source}")
    frame = pd.read_csv(source)
    if frame.empty:
        raise ValueError(f"Dataset is empty: {source}")
    return frame

