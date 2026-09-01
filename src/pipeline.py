"""Command-line orchestration for the UK economic data pipeline."""

import argparse
import logging
from pathlib import Path

import pandas as pd

from src.extract import extract_dataset, load_config
from src.load import load_outputs
from src.transform import transform_dataset
from src.validate import validate_dataset

LOGGER = logging.getLogger(__name__)


def run_pipeline(config_path: str | Path = "config/datasets.yml") -> pd.DataFrame:
    """Run extraction, transformation, validation, and loading."""
    config_file = Path(config_path)
    config = load_config(config_file)
    project_root = config_file.resolve().parent.parent
    frames: list[pd.DataFrame] = []

    for dataset in config["datasets"]:
        LOGGER.info("Processing %s", dataset["name"])
        raw = extract_dataset(project_root / dataset["path"])
        transformed = transform_dataset(raw, dataset["name"], dataset["unit"])
        validate_dataset(transformed)
        frames.append(transformed)

    combined = pd.concat(frames, ignore_index=True).sort_values(["dataset", "date"])
    load_outputs(combined, project_root / config.get("output_dir", "data/processed"))
    LOGGER.info("Loaded %d observations", len(combined))
    return combined


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/datasets.yml")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    run_pipeline(args.config)

