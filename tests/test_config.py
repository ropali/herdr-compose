import os
import pytest
from herdr_compose.config import get_config_dir, load_config, resolve_config_path, save_config_file
from herdr_compose.exceptions import ConfigError


def test_resolve_config_path_explicit(tmp_path):
    f = tmp_path / "custom.yaml"
    f.write_text("workspaces: [{name: test}]", encoding="utf-8")

    res = resolve_config_path(f)
    assert res == f


def test_resolve_config_path_explicit_nonexistent():
    with pytest.raises(ConfigError, match="does not exist"):
        resolve_config_path("/tmp/non_existent_layout_123456.yaml")


def test_resolve_config_path_env(tmp_path, monkeypatch):
    f = tmp_path / "env_config.yaml"
    f.write_text("workspaces: [{name: env_ws}]", encoding="utf-8")

    monkeypatch.setenv("HERDR_COMPOSE_CONFIG", str(f))
    res = resolve_config_path()
    assert res == f


def test_save_config_file(tmp_path, monkeypatch):
    config_dir = tmp_path / "user_config"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(config_dir))

    src = tmp_path / "my_layout.yaml"
    src.write_text("workspaces: [{name: saved_ws}]", encoding="utf-8")

    saved_path = save_config_file(src)
    assert saved_path.exists()
    assert saved_path.name == "my_layout.yaml"
    assert saved_path.parent == config_dir / "herdr-compose"
    assert "saved_ws" in saved_path.read_text(encoding="utf-8")


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
