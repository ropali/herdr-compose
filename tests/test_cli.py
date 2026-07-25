from pathlib import Path
import pytest
from herdr_compose.cli import main


def test_cli_init_command_default(tmp_path, capsys, monkeypatch):
    config_dir = tmp_path / "user_config"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(config_dir))

    main(["init"], standalone_mode=False)

    captured = capsys.readouterr().out
    target = config_dir / "herdr-compose" / "herdr-compose.yaml"
    assert f"Created starter layout config at: {target.resolve()}" in captured
    assert target.exists()
    assert "workspaces:" in target.read_text(encoding="utf-8")


def test_cli_init_command_custom(tmp_path, capsys):
    target = tmp_path / "test_init_layout.yaml"
    main(["init", str(target)], standalone_mode=False)

    captured = capsys.readouterr().out
    assert f"Created starter layout config at: {target.resolve()}" in captured
    assert target.exists()
    assert "workspaces:" in target.read_text(encoding="utf-8")


def test_cli_use_command(tmp_path, capsys, monkeypatch):
    config_dir = tmp_path / "user_config"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(config_dir))

    target = tmp_path / "backend.yaml"
    target.write_text("workspaces:\n  - name: backend_ws\n", encoding="utf-8")

    main(["save", str(target)], standalone_mode=False)
    main(["use", "backend"], standalone_mode=False)

    captured = capsys.readouterr().out
    assert "Active default layout configuration set to: backend.yaml" in captured

    main(["list"], standalone_mode=False)
    captured_list = capsys.readouterr().out
    assert "★ [active default]" in captured_list


def test_cli_save_command(tmp_path, capsys, monkeypatch):
    config_dir = tmp_path / "user_config"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(config_dir))

    target = tmp_path / "custom_layout.yaml"
    target.write_text("workspaces:\n  - name: test_ws\n", encoding="utf-8")

    main(["save", str(target)], standalone_mode=False)
    captured = capsys.readouterr().out
    assert "Saved configuration file to" in captured

    saved_file = config_dir / "herdr-compose" / "custom_layout.yaml"
    assert saved_file.exists()


def test_cli_list_command(tmp_path, capsys, monkeypatch):
    config_dir = tmp_path / "user_config"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(config_dir))

    # Empty list check
    main(["list"], standalone_mode=False)
    captured = capsys.readouterr().out
    assert "No saved configuration files found" in captured

    # Save a file then list
    target = tmp_path / "app_layout.yaml"
    target.write_text("workspaces:\n  - name: app_ws\n", encoding="utf-8")
    main(["save", str(target)], standalone_mode=False)

    main(["list"], standalone_mode=False)
    captured_list = capsys.readouterr().out
    assert "Saved configuration files in" in captured_list
    assert "app_layout.yaml" in captured_list
    assert "(1 workspace)" in captured_list


def test_cli_remove_command(tmp_path, capsys, monkeypatch):
    config_dir = tmp_path / "user_config"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(config_dir))

    target = tmp_path / "to_delete.yaml"
    target.write_text("workspaces:\n  - name: delete_me\n", encoding="utf-8")

    main(["save", str(target)], standalone_mode=False)
    saved_file = config_dir / "herdr-compose" / "to_delete.yaml"
    assert saved_file.exists()

    # Remove using filename without extension
    main(["remove", "to_delete"], standalone_mode=False)
    captured = capsys.readouterr().out
    assert "Removed saved configuration file: to_delete.yaml" in captured
    assert not saved_file.exists()


def test_cli_validate_command(tmp_path, capsys):
    target = tmp_path / "valid.yaml"
    target.write_text("workspaces:\n  - name: test_ws\n", encoding="utf-8")

    main(["validate", str(target)], standalone_mode=False)
    captured = capsys.readouterr().out
    assert "Configuration file" in captured
    assert "is valid" in captured


def test_cli_show_command(tmp_path, capsys):
    target = tmp_path / "layout.yaml"
    target.write_text(
        """
workspaces:
  - name: my_ws
    tabs:
      - label: t1
        panes:
          - command: ls
""",
        encoding="utf-8",
    )

    main(["show", str(target)], standalone_mode=False)
    captured = capsys.readouterr().out
    assert "Workspace 1: my_ws" in captured
    assert "Tab 1: t1" in captured
    assert "Pane 1" in captured
    assert "-> `ls`" in captured


def test_cli_dry_run(tmp_path, capsys):
    target = tmp_path / "layout.yaml"
    target.write_text("workspaces:\n  - name: test_ws\n", encoding="utf-8")

    main(["apply", str(target), "--dry-run"], standalone_mode=False)
    captured = capsys.readouterr().out
    assert "[DRY-RUN] herdr workspace create --label test_ws" in captured
    assert "Layout created successfully!" in captured
