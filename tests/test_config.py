import os
import pytest
from herdr_compose.config import (
    get_config_dir,
    list_saved_config_files,
    load_config,
    remove_saved_config_file,
    resolve_config_path,
    save_config_file,
)
from herdr_compose.exceptions import ConfigError


def test_resolve_config_path_explicit(tmp_path):
    f = tmp_path / "custom.yaml"
    f.write_text("workspaces: [{name: test}]", encoding="utf-8")

    res = resolve_config_path(f)
    assert res == f


def test_resolve_config_path_without_extension(tmp_path):
    f = tmp_path / "my_stack.yaml"
    f.write_text("workspaces: [{name: stack_ws}]", encoding="utf-8")

    res = resolve_config_path(tmp_path / "my_stack")
    assert res == f


def test_resolve_config_path_explicit_nonexistent():
    with pytest.raises(ConfigError, match="not found in default config directory"):
        resolve_config_path("non_existent_layout_123456.yaml")


def test_resolve_config_path_config_dir(tmp_path, monkeypatch):
    config_dir = tmp_path / "user_config"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(config_dir))

    target_dir = config_dir / "herdr-compose"
    target_dir.mkdir(parents=True, exist_ok=True)
    f = target_dir / "my_saved_layout.yaml"
    f.write_text("workspaces: [{name: saved}]", encoding="utf-8")

    assert resolve_config_path("my_saved_layout.yaml") == f
    assert resolve_config_path("my_saved_layout") == f


def test_save_and_list_and_remove_config_files(tmp_path, monkeypatch):
    config_dir = tmp_path / "user_config"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(config_dir))

    assert list_saved_config_files() == []

    src = tmp_path / "my_layout.yaml"
    src.write_text("workspaces: [{name: saved_ws}]", encoding="utf-8")

    saved_path = save_config_file(src)
    assert saved_path.exists()

    saved_list = list_saved_config_files()
    assert len(saved_list) == 1
    assert saved_list[0].name == "my_layout.yaml"

    # Remove file without extension
    removed = remove_saved_config_file("my_layout")
    assert removed == saved_path
    assert not saved_path.exists()
    assert list_saved_config_files() == []


def test_remove_nonexistent_file(tmp_path, monkeypatch):
    config_dir = tmp_path / "user_config"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(config_dir))

    with pytest.raises(ConfigError, match="not found"):
        remove_saved_config_file("non_existent")


def test_load_config_valid(tmp_path):
    f = tmp_path / "layout.yaml"
    f.write_text(
        """
workspaces:
  - name: demo
    root: ~/demo
    tabs:
      - label: main
        panes:
          - command: htop
""",
        encoding="utf-8",
    )
    cfg = load_config(f)
    assert len(cfg.workspaces) == 1
    assert cfg.workspaces[0].name == "demo"


def test_load_config_invalid_yaml(tmp_path):
    f = tmp_path / "bad.yaml"
    f.write_text("workspaces: [unclosed_bracket", encoding="utf-8")

    with pytest.raises(ConfigError, match="Failed to parse YAML"):
        load_config(f)
