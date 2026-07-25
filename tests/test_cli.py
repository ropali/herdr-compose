from pathlib import Path
import pytest
from herdr_compose.cli import main


def test_cli_init_command(tmp_path, capsys):
    target = tmp_path / "test_init_layout.yaml"
    main(["init", str(target)], standalone_mode=False)

    captured = capsys.readouterr().out
    assert "Created starter layout config at" in captured
    assert target.exists()
    assert "workspaces:" in target.read_text(encoding="utf-8")


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
