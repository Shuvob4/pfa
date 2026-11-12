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
