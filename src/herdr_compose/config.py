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


def list_saved_config_files() -> list[Path]:
    """List all saved YAML layout configuration files in ~/.config/herdr-compose/."""
    config_dir = get_config_dir()
    if not config_dir.is_dir():
        return []

    files = [
        p
        for p in config_dir.iterdir()
        if p.is_file() and p.suffix.lower() in (".yaml", ".yml")
    ]
    return sorted(files, key=lambda p: p.name.lower())


def save_config_file(
    source_path: str | Path, target_filename: str | None = None
) -> Path:
    """Validate and copy a configuration file to ~/.config/herdr-compose/<filename>."""
    src = resolve_config_path(source_path)
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

    Search priority for explicit user_path:
    1. Exact path if provided (e.g., ./examples/complex_multi_workspace.yaml)
    2. Default user config directory: ~/.config/herdr-compose/<filename>

    Search priority when user_path is None:
    1. HERDR_COMPOSE_CONFIG or HERDR_LAYOUT_CONFIG environment variable
    2. Extra candidate paths if provided
    3. Default candidate path (~/.config/herdr-compose/herdr-compose.yaml)
    """
    if user_path:
        raw_str = str(user_path).strip()
        expanded_str = expand_path(raw_str)
        p = Path(expanded_str)

        # 1. Exact path check
        if p.is_file():
            return p

        # 2. Check default user config directory (~/.config/herdr-compose/<filename>)
        config_dir_file = get_config_dir() / Path(raw_str).name
        if config_dir_file.is_file():
            return config_dir_file

        raise ConfigError(
            f"Configuration file '{user_path}' not found in default config directory ({get_config_dir()}) or specified path."
        )

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
