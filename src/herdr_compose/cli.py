"""CLI entry point for herdr-compose using Typer."""

from pathlib import Path
import sys
from typing import Optional

import typer

from herdr_compose import __version__
from herdr_compose.config import (
    get_config_dir,
    list_saved_config_files,
    load_config,
    remove_saved_config_file,
    resolve_config_path,
    save_config_file,
)
from herdr_compose.exceptions import HerdrComposeError
from herdr_compose.runner import HerdrRunner
from herdr_compose.utils import generate_starter_template, render_layout_tree

app = typer.Typer(
    name="herdr-compose",
    help="""
Declarative workspace layout manager for Herdr terminal workspace manager.

[bold]Examples:[/bold]
  $ herdr-compose                             # Apply auto-detected layout file
  $ herdr-compose --dry-run layout.yaml       # Preview commands without executing
  $ herdr-compose save layout.yaml            # Save layout into ~/.config/herdr-compose/
  $ herdr-compose list                        # List all saved layout configuration files
  $ herdr-compose remove layout               # Remove a saved layout configuration file
  $ herdr-compose show layout.yaml            # Inspect visual layout hierarchy tree
    """,
    add_completion=False,
    no_args_is_help=False,
    rich_markup_mode="rich",
)


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"herdr-compose {__version__}")
        raise typer.Exit()


@app.command("apply", help="Apply a layout configuration file")
def apply_cmd(
    config_file: Optional[Path] = typer.Argument(
        None, help="Path to layout YAML file (defaults to standard search paths)"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Print herdr commands without executing them"
    ),
    verbose: bool = typer.Option(
        False, "-v", "--verbose", help="Print verbose execution info"
    ),
    save: bool = typer.Option(
        False, "--save", help="Save layout file to ~/.config/herdr-compose/"
    ),
) -> None:
    """
    Apply a YAML layout configuration file to create Herdr workspaces, tabs, and panes.

    [bold]Examples:[/bold]
      $ herdr-compose apply
      $ herdr-compose apply layout.yaml
      $ herdr-compose apply my-layout.yaml --dry-run
      $ herdr-compose apply my-layout.yaml --save
      $ herdr-compose apply my-layout.yaml -v
    """
    _run_apply(config_file, dry_run=dry_run, verbose=verbose, save_flag=save)


@app.command("validate", help="Validate a YAML layout configuration file")
def validate_cmd(
    config_file: Optional[Path] = typer.Argument(
        None, help="Path to layout YAML file to validate"
    ),
) -> None:
    """
    Validate the syntax, split directions, ratios/sizes, and schema of a layout YAML file.

    [bold]Examples:[/bold]
      $ herdr-compose validate
      $ herdr-compose validate layout.yaml
      $ herdr-compose validate path/to/custom-layout.yaml
    """
    try:
        path = resolve_config_path(config_file)
        config = load_config(path)
        typer.secho(f"✓ Configuration file '{path}' is valid.", fg=typer.colors.GREEN, bold=True)
        typer.echo(f"  Defined workspaces: {len(config.workspaces)}")
    except HerdrComposeError as e:
        typer.secho(f"Error: {e}", err=True, fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command("show", help="Display layout tree structure without applying")
def show_cmd(
    config_file: Optional[Path] = typer.Argument(
        None, help="Path to layout YAML file to display"
    ),
) -> None:
    """
    Display a visual tree representation of the workspace layout hierarchy.

    [bold]Examples:[/bold]
      $ herdr-compose show
      $ herdr-compose show layout.yaml
      $ herdr-compose show examples/complex_multi_workspace.yaml
    """
    try:
        path = resolve_config_path(config_file)
        config = load_config(path)
        typer.echo(f"Layout loaded from '{path}':\n")
        typer.echo(render_layout_tree(config))
    except HerdrComposeError as e:
        typer.secho(f"Error: {e}", err=True, fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command("init", help="Generate a starter herdr-compose.yaml configuration file")
def init_cmd(
    path: Path = typer.Argument(
        Path("herdr-compose.yaml"), help="Target output path (default: herdr-compose.yaml)"
    ),
) -> None:
    """
    Generate a starter herdr-compose.yaml configuration file.

    [bold]Examples:[/bold]
      $ herdr-compose init
      $ herdr-compose init my-starter-layout.yaml
    """
    try:
        created = generate_starter_template(path)
        typer.secho(f"Created starter layout config at: {created}", fg=typer.colors.GREEN, bold=True)
    except Exception as e:
        typer.secho(f"Error: {e}", err=True, fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command("save", help="Save a layout YAML file into ~/.config/herdr-compose/")
def save_cmd(
    config_file: Optional[Path] = typer.Argument(
        None, help="Path to layout YAML file to save into ~/.config/herdr-compose/"
    ),
) -> None:
    """
    Validate and copy a layout YAML file into ~/.config/herdr-compose/<filename>.

    [bold]Examples:[/bold]
      $ herdr-compose save layout.yaml
      $ herdr-compose save my-custom-layout.yaml
    """
    try:
        path = resolve_config_path(config_file)
        saved_path = save_config_file(path)
        typer.secho(f"✓ Saved configuration file to: {saved_path}", fg=typer.colors.GREEN, bold=True)
    except HerdrComposeError as e:
        typer.secho(f"Error: {e}", err=True, fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command("list", help="List all saved layout configuration files")
def list_cmd() -> None:
    """
    List all saved layout configuration files stored in ~/.config/herdr-compose/.

    [bold]Examples:[/bold]
      $ herdr-compose list
    """
    config_dir = get_config_dir()
    saved_files = list_saved_config_files()

    if not saved_files:
        typer.echo(f"No saved configuration files found in '{config_dir}'")
        typer.echo("Tip: Run 'herdr-compose save <file.yaml>' to save a layout configuration.")
        return

    typer.echo(f"Saved configuration files in '{config_dir}':\n")
    for idx, file_path in enumerate(saved_files, start=1):
        try:
            config = load_config(file_path)
            ws_count = len(config.workspaces)
            ws_str = f"({ws_count} workspace{'s' if ws_count != 1 else ''})"
        except Exception:
            ws_str = "(invalid configuration)"

        styled_name = typer.style(file_path.name, bold=True, fg=typer.colors.CYAN)
        typer.echo(f"  {idx}. {styled_name} {ws_str}")


@app.command("remove", help="Remove a saved layout configuration file")
def remove_cmd(
    filename: Path = typer.Argument(
        ..., help="Name of saved layout configuration file to remove"
    ),
) -> None:
    """
    Remove a saved layout configuration file from ~/.config/herdr-compose/.

    [bold]Examples:[/bold]
      $ herdr-compose remove layout
      $ herdr-compose remove my-custom-layout.yaml
    """
    try:
        removed_path = remove_saved_config_file(filename)
        typer.secho(
            f"✓ Removed saved configuration file: {removed_path.name}",
            fg=typer.colors.GREEN,
            bold=True,
        )
    except HerdrComposeError as e:
        typer.secho(f"Error: {e}", err=True, fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command("rm", hidden=True)
def rm_cmd(filename: Path = typer.Argument(...)) -> None:
    """Alias for remove."""
    remove_cmd(filename)


@app.command("delete", hidden=True)
def delete_cmd(filename: Path = typer.Argument(...)) -> None:
    """Alias for remove."""
    remove_cmd(filename)


def _run_apply(
    config_file: Optional[Path], dry_run: bool, verbose: bool, save_flag: bool
) -> None:
    try:
        config_path = resolve_config_path(config_file)

        if save_flag:
            saved_path = save_config_file(config_path)
            typer.secho(f"✓ Saved configuration file to: {saved_path}", fg=typer.colors.GREEN, bold=True)

        typer.echo(f"Applying layout from {config_path}...")
        config = load_config(config_path)

        runner = HerdrRunner(dry_run=dry_run, verbose=verbose)
        runner.apply_layout(config)
        typer.secho("Layout created successfully!", fg=typer.colors.GREEN, bold=True)
    except HerdrComposeError as e:
        typer.secho(f"Error: {e}", err=True, fg=typer.colors.RED)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.secho(f"Unexpected error: {e}", err=True, fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.callback()
def main_callback(
    version: Optional[bool] = typer.Option(
        None,
        "-V",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Print version and exit",
    ),
) -> None:
    """
    Declarative workspace layout manager for Herdr terminal workspace manager.
    """
    pass


def main(argv: list[str] | None = None, standalone_mode: bool = True) -> None:
    if argv is None:
        argv = sys.argv[1:]

    known_subcommands = {
        "apply",
        "validate",
        "show",
        "init",
        "save",
        "list",
        "remove",
        "rm",
        "delete",
        "--help",
        "-h",
        "--version",
        "-V",
        "-v",
    }

    # If first argument is a file path or flag (not a subcommand), route to apply
    if not argv or (argv[0] not in known_subcommands and not argv[0].startswith("-")):
        argv = ["apply"] + list(argv)

    app(args=argv, standalone_mode=standalone_mode)


if __name__ == "__main__":
    main()
