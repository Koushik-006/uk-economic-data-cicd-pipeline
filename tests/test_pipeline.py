from src.pipeline import run_pipeline


def test_run_pipeline_end_to_end(tmp_path):
    raw_dir = tmp_path / "data" / "raw"
    raw_dir.mkdir(parents=True)
    (raw_dir / "gdp.csv").write_text("date,value\n2025-01-01,101.2\n", encoding="utf-8")
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config = config_dir / "datasets.yml"
    config.write_text(
        "datasets:\n  - name: gdp\n    path: data/raw/gdp.csv\n    unit: index\noutput_dir: output\n",
        encoding="utf-8",
    )

    result = run_pipeline(config)

    assert result.iloc[0]["dataset"] == "gdp"
    assert (tmp_path / "output" / "uk_economic_indicators.csv").is_file()
    assert (tmp_path / "output" / "economic_data.db").is_file()
