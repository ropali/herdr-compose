"""Utility functions for herdr-compose (formatting, template generation, tree display)."""

from pathlib import Path
from herdr_compose.models import LayoutConfig

DEFAULT_STARTER_TEMPLATE = """# Herdr Compose Workspace Layout Configuration
# Learn more about Herdr at https://herdr.dev

workspaces:
  - name: main
    root: ~/Workspace/my-project
    focus: true
    tabs:
      - label: editor
        cwd: ~/Workspace/my-project
        panes:
          - name: main_editor
            command: nvim
            focus: true

          - name: sidebar
            direction: right
            size: 20%
            command: opencode

          - name: status
            direction: down
            size: 30%
            from: main_editor
            command: git status

      - label: dev-server
        panes:
          - command: npm run dev
"""


def generate_starter_template(target_path: Path, overwrite: bool = False) -> Path:
    """Generate a starter herdr-compose.yaml template file and return its absolute path."""
    abs_path = target_path.resolve()
    if abs_path.exists() and not overwrite:
        raise FileExistsError(f"Target template file already exists: {abs_path}")

    abs_path.parent.mkdir(parents=True, exist_ok=True)
    abs_path.write_text(DEFAULT_STARTER_TEMPLATE, encoding="utf-8")
    return abs_path


def render_layout_tree(config: LayoutConfig) -> str:
    """Render a text representation of the layout hierarchy."""
    lines = ["Layout Summary:"]
    for ws_idx, ws in enumerate(config.workspaces, start=1):
        focus_str = " (focused)" if ws.focus else ""
        root_str = f" [root: {ws.root}]" if ws.root else ""
        lines.append(f"Workspace {ws_idx}: {ws.name}{focus_str}{root_str}")

        if not ws.tabs:
            lines.append("  └─ (default tab)")
            continue

        for tab_idx, tab in enumerate(ws.tabs, start=1):
            is_last_tab = tab_idx == len(ws.tabs)
            tab_prefix = "  └─ " if is_last_tab else "  ├─ "
            sub_prefix = "     " if is_last_tab else "  │  "

            label_str = tab.label or f"tab-{tab_idx}"
            cwd_str = f" [cwd: {tab.cwd}]" if tab.cwd else ""
            lines.append(f"{tab_prefix}Tab {tab_idx}: {label_str}{cwd_str}")

            if not tab.panes:
                lines.append(f"{sub_prefix}└─ (root pane)")
                continue

            for pane_idx, pane in enumerate(tab.panes, start=1):
                is_last_pane = pane_idx == len(tab.panes)
                pane_connector = "└─ " if is_last_pane else "├─ "
                p_focus = " (focused)" if pane.focus else ""
                p_cmd = f" -> `{pane.command}`" if pane.command else ""
                p_name = f" [{pane.name}]" if pane.name else ""
                p_size = f" [split {pane.split}, size {pane.size}]" if pane_idx > 1 else " [root pane]"
                p_from = f" (from {pane.from_ref})" if pane_idx > 1 and pane.from_ref != "previous" else ""

                lines.append(
                    f"{sub_prefix}{pane_connector}Pane {pane_idx}{p_name}{p_size}{p_from}{p_focus}{p_cmd}"
                )

    return "\n".join(lines)
