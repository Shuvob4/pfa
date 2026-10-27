import typer

app = typer.Typer(help="Local personal finance assistant.", no_args_is_help=True)


@app.command()
def init() -> None:
    """Create data folders and a config file."""
    typer.echo("init: not implemented yet.")


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
