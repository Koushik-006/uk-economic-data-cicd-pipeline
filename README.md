# UK Economic Data CI/CD Pipeline

A small, reproducible ETL project that normalizes UK economic indicator samples,
checks their quality, and publishes consolidated CSV and SQLite outputs.

> [!NOTE]
> The committed CSV files are illustrative samples for demonstrating the pipeline.
> They are not an official or live statistical release. Production deployments
> should replace them with versioned extracts from the UK Office for National
> Statistics or another documented source.

## Architecture

```text
CSV inputs -> extract -> transform -> validate -> CSV + SQLite
                                      ^
                              tests and CI checks
```

The pipeline is intentionally split into small modules so extraction, business
rules, quality checks, and persistence can evolve independently.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m src.pipeline
pytest
```

Generated files are written to `data/processed/` and ignored by Git.

## Docker

```bash
docker compose up --build
```

The bind mount preserves generated outputs in `data/processed/`.

## Data contract

Every raw CSV must contain `date` and `value`. Configuration supplies the
indicator name and unit. The normalized table contains:

| Column | Meaning |
| --- | --- |
| `dataset` | Stable indicator identifier |
| `date` | Observation date |
| `value` | Numeric observation |
| `unit` | Measurement unit |

Validation rejects empty inputs, missing/null fields, duplicate observations,
and non-numeric values. GitHub Actions runs linting, tests with 80% coverage,
and a full pipeline smoke test on Python 3.11 and 3.12.

## Extending the pipeline

Add a CSV under `data/raw/`, register it in `config/datasets.yml`, and add tests
for any indicator-specific transformation. For production use, pin data-source
URLs and checksums, retain raw snapshots, and load with migrations instead of
replacing the analytical table.

## License

MIT

