"""Data models and validation for Herdr layouts."""

from dataclasses import dataclass, field
import os
import re
from typing import Any

from herdr_compose.exceptions import ConfigError


def expand_path(p: str | None) -> str | None:
    if not p:
        return None
    return os.path.expanduser(os.path.expandvars(p))


def parse_size_or_ratio(val: Any) -> float | None:
    """Parse size or ratio value into a float between 0.0 and 1.0."""
    if val is None:
        return None

    if isinstance(val, (int, float)):
        num = float(val)
        if 0.0 < num < 1.0:
            return round(num, 4)
        if 1 <= num < 100:
            return round(num / 100.0, 4)
        raise ConfigError(
            f"Size numeric value must be between 0.0 and 1.0 (or percentage 1..99), got {val}"
        )

    val_str = str(val).strip()
    match = re.match(r"^(\d+(?:\.\d+)?)\s*%?$", val_str)
    if match:
        num = float(match.group(1))
        if "%" in val_str or num > 1.0:
            num = num / 100.0
        if 0.0 < num < 1.0:
            return round(num, 4)

    raise ConfigError(
        f"Invalid size '{val}'. Specify a percentage (e.g. '30%') or float (e.g. 0.3)"
    )


def normalize_direction(data: dict[str, Any]) -> str:
    """Normalize split direction from direction or split keys."""
    raw = data.get("direction") or data.get("split") or "right"
    val = str(raw).lower().strip()

    if val in ("right", "r", "horizontal", "h"):
        return "right"
    if val in ("down", "d", "bottom", "vertical", "v"):
        return "down"

    raise ConfigError(
        f"Invalid split direction '{raw}'. Supported values: 'right', 'down', 'horizontal', 'vertical'."
    )


@dataclass
class PaneConfig:
    name: str | None = None
    command: str | None = None
    split: str = "right"  # 'right' or 'down'
    size: float | None = None  # Fraction of space desired for THIS new pane (0.0 .. 1.0)
    focus: bool = False
    cwd: str | None = None
    from_ref: str = "previous"
    env: dict[str, str] = field(default_factory=dict)

    @property
    def ratio(self) -> float | None:
        """Backward compatible alias for size."""
        return self.size

    @classmethod
    def from_dict_or_str(cls, data: Any) -> "PaneConfig":
        if isinstance(data, str):
            return cls(command=data)

        if not isinstance(data, dict):
            raise ConfigError(f"Pane definition must be a string or dictionary, got {type(data)}")

        name = data.get("name") or data.get("id")
        split_dir = normalize_direction(data)

        raw_size = data.get("size") if "size" in data else data.get("ratio")
        size = parse_size_or_ratio(raw_size)

        from_ref = str(data.get("from") or data.get("target") or "previous").strip()

        env_raw = data.get("env", {})
        env = {}
        if isinstance(env_raw, dict):
            env = {str(k): str(v) for k, v in env_raw.items()}
        elif isinstance(env_raw, list):
            for item in env_raw:
                if "=" in str(item):
                    k, v = str(item).split("=", 1)
                    env[k] = v

        return cls(
            name=str(name) if name else None,
            command=data.get("command") or data.get("run"),
            split=split_dir,
            size=size,
            focus=bool(data.get("focus", False)),
            cwd=expand_path(data.get("cwd")),
            from_ref=from_ref,
            env=env,
        )


@dataclass
class TabConfig:
    label: str | None = None
    cwd: str | None = None
    panes: list[PaneConfig] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TabConfig":
        if not isinstance(data, dict):
            raise ConfigError("Tab configuration must be a dictionary")

        panes_raw = data.get("panes", [])
        panes = [PaneConfig.from_dict_or_str(p) for p in panes_raw]

        env_raw = data.get("env", {})
        env = {}
        if isinstance(env_raw, dict):
            env = {str(k): str(v) for k, v in env_raw.items()}
        elif isinstance(env_raw, list):
            for item in env_raw:
                if "=" in str(item):
                    k, v = str(item).split("=", 1)
                    env[k] = v

        return cls(
            label=data.get("label") or data.get("name"),
            cwd=expand_path(data.get("cwd")),
            panes=panes,
            env=env,
        )


@dataclass
class WorkspaceConfig:
    name: str
    root: str | None = None
    focus: bool = False
    tabs: list[TabConfig] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WorkspaceConfig":
        if not isinstance(data, dict):
            raise ConfigError("Workspace configuration must be a dictionary")

        name = data.get("name") or data.get("workspace") or data.get("label")
        if not name:
            raise ConfigError("Workspace missing required field 'name'")

        env_raw = data.get("env", {})
        env = {}
        if isinstance(env_raw, dict):
            env = {str(k): str(v) for k, v in env_raw.items()}
        elif isinstance(env_raw, list):
            for item in env_raw:
                if "=" in str(item):
                    k, v = str(item).split("=", 1)
                    env[k] = v

        # Shorthand: workspace directly has `panes` instead of `tabs`
        if "panes" in data and "tabs" not in data:
            panes_raw = data.get("panes", [])
            panes = [PaneConfig.from_dict_or_str(p) for p in panes_raw]
            default_tab = TabConfig(label=str(name), cwd=expand_path(data.get("root")), panes=panes, env=env)
            tabs = [default_tab]
        else:
            tabs_raw = data.get("tabs", [])
            tabs = [TabConfig.from_dict(t) for t in tabs_raw]

        return cls(
            name=str(name),
            root=expand_path(data.get("root")),
            focus=bool(data.get("focus", False)),
            tabs=tabs,
            env=env,
        )


@dataclass
class LayoutConfig:
    workspaces: list[WorkspaceConfig] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LayoutConfig":
        if not isinstance(data, dict):
            raise ConfigError("YAML root must be a dictionary/mapping")

        ws_raw = data.get("workspaces")
        if not ws_raw or not isinstance(ws_raw, list):
            raise ConfigError(
                "Layout configuration must contain a non-empty 'workspaces' list"
            )

        workspaces = [WorkspaceConfig.from_dict(ws) for ws in ws_raw]
        return cls(workspaces=workspaces)
