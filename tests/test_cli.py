import typer
from typer.testing import CliRunner

from fpa.cli import app

runner = CliRunner()
EXPECTED = {"init", "ingest", "parse", "build", "categorize", "run", "app"}


def test_help_lists_all_commands():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    commands = set(typer.main.get_command(app).commands)
    assert commands == EXPECTED


def test_init_creates_folders_and_is_idempotent(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    cfg_file = tmp_path / "fpa.toml"
    cfg_file.write_text(f'[paths]\ndata_dir = "{data_dir.as_posix()}"\n', encoding="utf-8")
    monkeypatch.setenv("FPA_CONFIG", str(cfg_file))

    before = cfg_file.read_text(encoding="utf-8")

    first = runner.invoke(app, ["init"])
    second = runner.invoke(app, ["init"])
    assert first.exit_code == 0
    assert second.exit_code == 0
    assert (data_dir / "inbox").is_dir()
    assert (data_dir / "raw").is_dir()
    assert "kept" in second.output

    after = cfg_file.read_text(encoding="utf-8")

    assert after == before
