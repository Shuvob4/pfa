from importlib.resources import files

import typer

from fpa.config import find_config_file, load_config, user_config_path

app = typer.Typer(help="Local personal finance assistant.", no_args_is_help=True)


@app.command()
def init() -> None:
    """Create data folders and a config file."""
    cfg = load_config()
    for folder in (cfg.data_dir, cfg.inbox_dir, cfg.raw_dir):
        folder.mkdir(parents=True, exist_ok=True)

    config_file = find_config_file() or user_config_path()
    if config_file.exists():
        status = "kept"
    else:
        config_file.parent.mkdir(parents=True, exist_ok=True)
        template = files("fpa").joinpath("fpa.example.toml").read_text(encoding="utf-8")
        config_file.write_text(template, encoding="utf-8")
        status = "created"

    typer.echo(f"Config:   {config_file} ({status})")
    typer.echo(f"Data:     {cfg.data_dir}")
    typer.echo(f"Inbox:    {cfg.inbox_dir}  <- drop statements here")
    typer.echo(f"Database: {cfg.db_path}")


@app.command()
def ingest() -> None:
    """Fingerprint and register new files from the inbox."""
    typer.echo("ingest: not implemented yet.")


@app.command()
def parse() -> None:
    """Parse and clean ingested datasets."""
    typer.echo("parser: not implemented yet.")


@app.command()
def build() -> None:
    """Build production ready data artifacts"""
    typer.echo("build: not implemented yet.")


@app.command()
def categorize() -> None:
    """Categorize and Tag merchandise and transactions"""
    typer.echo("categorize: not implemented yet.")


@app.command()
def run() -> None:
    """Execute the pipeline"""
    typer.echo("run: not implemented yet.")


@app.command(name="app")
def launch_app() -> None:
    """Launch the Streamlit dashboard."""
    typer.echo("app: not implemented yet.")
