import pytest
from herdr_compose.exceptions import ConfigError
from herdr_compose.models import LayoutConfig, PaneConfig, TabConfig, WorkspaceConfig, parse_size_or_ratio


def test_parse_size_or_ratio():
    assert parse_size_or_ratio(0.3) == 0.3
    assert parse_size_or_ratio(30) == 0.3
    assert parse_size_or_ratio("30%") == 0.3
    assert parse_size_or_ratio("75%") == 0.75
    assert parse_size_or_ratio("0.8") == 0.8


def test_pane_config_string_shorthand():
    p = PaneConfig.from_dict_or_str("nvim")
    assert p.command == "nvim"
    assert p.split == "right"


def test_pane_config_explicit_direction_and_size():
    p = PaneConfig.from_dict_or_str({
        "name": "sidebar",
        "direction": "vertical",
        "size": "30%",
        "command": "htop",
    })
    assert p.name == "sidebar"
    assert p.split == "down"
    assert p.size == 0.3
    assert p.ratio == 0.3
    assert p.command == "htop"


def test_workspace_panes_shorthand():
    ws = WorkspaceConfig.from_dict({
        "name": "quick",
        "panes": [
            "nvim",
            {"direction": "right", "size": "40%", "command": "opencode"},
        ],
    })
    assert ws.name == "quick"
    assert len(ws.tabs) == 1
    assert len(ws.tabs[0].panes) == 2
    assert ws.tabs[0].panes[0].command == "nvim"
    assert ws.tabs[0].panes[1].size == 0.4


def test_pane_config_invalid_direction():
    with pytest.raises(ConfigError, match="Invalid split direction"):
        PaneConfig.from_dict_or_str({"direction": "diagonal"})
