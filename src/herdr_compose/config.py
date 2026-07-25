"""Config loader and path resolution module for herdr-compose."""

import os
from pathlib import Path
from typing import Sequence

import yaml

from herdr_compose.exceptions import ConfigError
from herdr_compose.models import LayoutConfig, expand_path

DEFAULT_CANDIDATE_PATHS = [
    "~/.config/herdr-compose/herdr-compose.yaml",
]


def get_config_dir() -> Path:
    """Return the user configuration directory (~/.config/herdr-compose)."""
    xdg = os.getenv("XDG_CONFIG_HOME")
    if xdg:
        base = Path(expand_path(xdg))
    else:
        base = Path.home() / ".config"
    return base / "herdr-compose"


def save_config_file(
    source_path: str | Path, target_filename: str | None = None
) -> Path:
    """Validate and copy a configuration file to ~/.config/herdr-compose/<filename>."""
    src = Path(expand_path(str(source_path)))
    if not src.is_file():
        raise ConfigError(f"Source config file not found: {source_path}")

    # Validate schema before saving
    load_config(src)

    filename = target_filename or src.name
    config_dir = get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)

    dest = config_dir / filename
    dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return dest


def resolve_config_path(
    user_path: str | Path | None = None,
    extra_candidates: Sequence[str | Path] | None = None,
) -> Path:
    """Resolve the layout configuration file path.

    Search priority:
    1. Direct user_path parameter (CLI arg)
    2. HERDR_COMPOSE_CONFIG or HERDR_LAYOUT_CONFIG environment variable
    3. Extra candidate paths if provided
    4. Default candidate paths
    """
    if user_path:
        p = Path(expand_path(str(user_path)))
        if p.is_file():
            return p
        raise ConfigError(f"Specified configuration file does not exist: {user_path}")

    env_path = os.getenv("HERDR_COMPOSE_CONFIG") or os.getenv("HERDR_LAYOUT_CONFIG")
    if env_path:
        p = Path(expand_path(env_path))
        if p.is_file():
            return p
        raise ConfigError(
            f"Configuration file specified in environment variable does not exist: {env_path}"
        )

    candidates = list(extra_candidates or []) + DEFAULT_CANDIDATE_PATHS
    for cand in candidates:
        expanded = expand_path(str(cand))
        if expanded and os.path.isfile(expanded):
            return Path(expanded)

    searched = "\n  - ".join([c for c in candidates])
    raise ConfigError(
        f"No layout YAML file found. Checked paths:\n  - {searched}\n"
        "Provide a path via CLI or set HERDR_COMPOSE_CONFIG."
    )


def load_config(config_path: str | Path) -> LayoutConfig:
    """Load and parse layout configuration from a YAML file."""
    path = Path(config_path)
    if not path.is_file():
        raise ConfigError(f"Config file not found: {config_path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ConfigError(f"Failed to parse YAML file {config_path}: {e}") from e
    except Exception as e:
        raise ConfigError(f"Failed to read file {config_path}: {e}") from e

    return LayoutConfig.from_dict(data)
