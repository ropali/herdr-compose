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


def get_active_config_pointer_file() -> Path:
    """Return path to active config pointer file (~/.config/herdr-compose/.active)."""
    return get_config_dir() / ".active"


def set_active_config(filename: str | Path) -> Path:
    """Set the active default layout configuration file."""
    resolved_path = resolve_config_path(filename)
    pointer_file = get_active_config_pointer_file()
    pointer_file.parent.mkdir(parents=True, exist_ok=True)
    pointer_file.write_text(resolved_path.name, encoding="utf-8")
    return resolved_path


def get_active_config_name() -> str | None:
    """Get the name of the currently active default config file, if set and valid."""
    pointer_file = get_active_config_pointer_file()
    if pointer_file.is_file():
        name = pointer_file.read_text(encoding="utf-8").strip()
        if name and (get_config_dir() / name).is_file():
            return name
    return None


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
    if not filename.endswith((".yaml", ".yml")):
        filename += ".yaml"

    config_dir = get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)

    dest = config_dir / filename
    dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    # If no active config is set yet, make this newly saved file the active default
    if get_active_config_name() is None:
        set_active_config(dest.name)

    return dest


def remove_saved_config_file(filename: str | Path) -> Path:
    """Remove a saved layout configuration file from ~/.config/herdr-compose/."""
    raw_str = str(filename).strip()
    config_dir = get_config_dir()

    p_raw = Path(raw_str)
    if p_raw.suffix.lower() in (".yaml", ".yml"):
        exts = [""]
    else:
        exts = ["", ".yaml", ".yml"]

    for ext in exts:
        target_name = p_raw.name + ext
        target_path = config_dir / target_name
        if target_path.is_file():
            target_path.unlink()

            # Clear active pointer if deleted file was active
            active_name = get_active_config_name()
            if active_name and active_name == target_name:
                pointer_file = get_active_config_pointer_file()
                if pointer_file.is_file():
                    pointer_file.unlink()

            return target_path

    raise ConfigError(
        f"Saved configuration file '{filename}' not found in '{config_dir}'."
    )


def resolve_config_path(
    user_path: str | Path | None = None,
    extra_candidates: Sequence[str | Path] | None = None,
) -> Path:
    """Resolve the layout configuration file path.

    Search priority for explicit user_path:
    - If user_path has no .yaml/.yml extension, try user_path, user_path.yaml, user_path.yml.
    - Check exact paths first, then look in default config directory (~/.config/herdr-compose/).

    Search priority when user_path is None:
    1. HERDR_COMPOSE_CONFIG or HERDR_LAYOUT_CONFIG environment variable
    2. Active default setting (~/.config/herdr-compose/.active)
    3. Extra candidate paths if provided
    4. Default candidate path (~/.config/herdr-compose/herdr-compose.yaml)
    """
    if user_path:
        raw_str = str(user_path).strip()
        p_raw = Path(expand_path(raw_str))

        if p_raw.suffix.lower() in (".yaml", ".yml"):
            exts = [""]
        else:
            exts = ["", ".yaml", ".yml"]

        for ext in exts:
            candidate_str = raw_str + ext
            expanded_p = Path(expand_path(candidate_str))

            # 1. Exact path check
            if expanded_p.is_file():
                return expanded_p

            # 2. Check default user config directory (~/.config/herdr-compose/<filename>)
            config_dir_file = get_config_dir() / Path(candidate_str).name
            if config_dir_file.is_file():
                return config_dir_file

        raise ConfigError(
            f"Configuration file '{user_path}' (or '{user_path}.yaml') not found in default config directory ({get_config_dir()}) or specified path."
        )

    env_path = os.getenv("HERDR_COMPOSE_CONFIG") or os.getenv("HERDR_LAYOUT_CONFIG")
    if env_path:
        p = Path(expand_path(env_path))
        if p.is_file():
            return p
        raise ConfigError(
            f"Configuration file specified in environment variable does not exist: {env_path}"
        )

    active_name = get_active_config_name()
    if active_name:
        active_file = get_config_dir() / active_name
        if active_file.is_file():
            return active_file

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
