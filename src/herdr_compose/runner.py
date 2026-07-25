"""Runner engine to execute herdr layout commands."""

import json
import shutil
import subprocess
from typing import Any

from herdr_compose.exceptions import HerdrCmdError, HerdrNotInstalledError
from herdr_compose.models import LayoutConfig, PaneConfig, TabConfig, WorkspaceConfig


class HerdrRunner:
    """Executes or simulates Herdr CLI commands according to a LayoutConfig."""

    def __init__(self, dry_run: bool = False, verbose: bool = False):
        self.dry_run = dry_run
        self.verbose = verbose

    def _check_herdr_installed(self) -> None:
        if not self.dry_run and shutil.which("herdr") is None:
            raise HerdrNotInstalledError()

    def run_cmd(self, cmd_args: list[str]) -> dict[str, Any]:
        """Run a herdr subcommand and return parsed JSON output or raw dict."""
        if self.dry_run:
            print(f"[DRY-RUN] herdr {' '.join(cmd_args)}")
            return {}

        if self.verbose:
            print(f"[EXEC] herdr {' '.join(cmd_args)}")

        res = subprocess.run(["herdr"] + cmd_args, capture_output=True, text=True)
        if res.returncode != 0:
            raise HerdrCmdError(cmd_args, res.returncode, res.stderr)

        try:
            return json.loads(res.stdout)
        except json.JSONDecodeError:
            return {"raw": res.stdout}

    def apply_layout(self, config: LayoutConfig) -> None:
        """Apply a complete LayoutConfig."""
        self._check_herdr_installed()

        for ws_idx, ws in enumerate(config.workspaces, start=1):
            self._apply_workspace(ws, ws_idx)

    def _apply_workspace(self, ws: WorkspaceConfig, ws_idx: int) -> None:
        first_tab = ws.tabs[0] if ws.tabs else None
        first_pane = first_tab.panes[0] if (first_tab and first_tab.panes) else None
        ws_cwd = (
            (first_pane.cwd if (first_pane and first_pane.cwd) else None)
            or (first_tab.cwd if first_tab else None)
            or ws.root
        )

        cmd = ["workspace", "create", "--label", ws.name]
        if ws_cwd:
            cmd.extend(["--cwd", ws_cwd])
        if ws.focus:
            cmd.append("--focus")
        else:
            cmd.append("--no-focus")

        for k, v in ws.env.items():
            cmd.extend(["--env", f"{k}={v}"])

        ws_res = self.run_cmd(cmd)

        if self.dry_run:
            ws_id = f"w{ws_idx}"
            tab_id = f"{ws_id}:t1"
            root_pane_id = f"{ws_id}:p1"
        else:
            ws_result = ws_res.get("result", {})
            ws_id = ws_result.get("workspace", {}).get("workspace_id")
            tab_id = ws_result.get("tab", {}).get("tab_id")
            root_pane_id = ws_result.get("root_pane", {}).get("pane_id")

        for tab_idx, tab in enumerate(ws.tabs):
            self._apply_tab(
                tab=tab,
                tab_idx=tab_idx,
                ws=ws,
                ws_id=ws_id,
                initial_tab_id=tab_id,
                initial_root_pane_id=root_pane_id,
            )

    def _apply_tab(
        self,
        tab: TabConfig,
        tab_idx: int,
        ws: WorkspaceConfig,
        ws_id: str,
        initial_tab_id: str,
        initial_root_pane_id: str,
    ) -> None:
        first_pane = tab.panes[0] if tab.panes else None
        effective_tab_cwd = (
            (first_pane.cwd if (first_pane and first_pane.cwd) else None)
            or tab.cwd
            or ws.root
        )

        if tab_idx == 0:
            tab_id = initial_tab_id
            root_pane_id = initial_root_pane_id
            if tab.label:
                self.run_cmd(["tab", "rename", tab_id, tab.label])
        else:
            tab_cmd = ["tab", "create", "--workspace", ws_id]
            if effective_tab_cwd:
                tab_cmd.extend(["--cwd", effective_tab_cwd])
            if tab.label:
                tab_cmd.extend(["--label", tab.label])
            for k, v in tab.env.items():
                tab_cmd.extend(["--env", f"{k}={v}"])

            tab_res = self.run_cmd(tab_cmd)

            if self.dry_run:
                root_pane_id = f"{ws_id}:t{tab_idx + 1}:p1"
            else:
                root_pane_id = (
                    tab_res.get("result", {}).get("root_pane", {}).get("pane_id")
                )

        panes_list: list[str] = [root_pane_id]
        pane_name_map: dict[str, str] = {}

        for pane_idx, pane in enumerate(tab.panes):
            current_pane_id = self._apply_pane(
                pane=pane,
                pane_idx=pane_idx,
                tab_cwd=effective_tab_cwd,
                root_pane_id=root_pane_id,
                panes_list=panes_list,
                pane_name_map=pane_name_map,
                ws_id=ws_id,
                tab_idx=tab_idx,
            )
            if pane.name:
                pane_name_map[pane.name.lower()] = current_pane_id

            if pane_idx > 0:
                panes_list.append(current_pane_id)

    def _apply_pane(
        self,
        pane: PaneConfig,
        pane_idx: int,
        tab_cwd: str | None,
        root_pane_id: str,
        panes_list: list[str],
        pane_name_map: dict[str, str],
        ws_id: str,
        tab_idx: int,
    ) -> str:
        pane_cwd = pane.cwd or tab_cwd

        if pane_idx == 0:
            current_pane_id = root_pane_id
        else:
            from_ref = pane.from_ref.lower()
            if from_ref in pane_name_map:
                source_pane_id = pane_name_map[from_ref]
            elif from_ref in ["root", "first", "0"]:
                source_pane_id = panes_list[0]
            elif from_ref in ["previous", "prev"]:
                source_pane_id = panes_list[-1]
            elif from_ref.isdigit():
                idx = int(from_ref)
                source_pane_id = (
                    panes_list[idx] if idx < len(panes_list) else panes_list[-1]
                )
            else:
                source_pane_id = panes_list[-1]

            split_cmd = [
                "pane",
                "split",
                source_pane_id,
                "--direction",
                pane.split,
            ]
            if pane.size is not None:
                herdr_ratio = round(1.0 - pane.size, 4)
                split_cmd.extend(["--ratio", str(herdr_ratio)])

            if pane_cwd:
                split_cmd.extend(["--cwd", pane_cwd])
            if pane.focus:
                split_cmd.append("--focus")
            else:
                split_cmd.append("--no-focus")
            for k, v in pane.env.items():
                split_cmd.extend(["--env", f"{k}={v}"])

            split_res = self.run_cmd(split_cmd)
            if self.dry_run:
                current_pane_id = f"{ws_id}:t{tab_idx + 1}:p{pane_idx + 1}"
            else:
                current_pane_id = (
                    split_res.get("result", {}).get("pane", {}).get("pane_id")
                )

        if pane.command:
            self.run_cmd(["pane", "run", current_pane_id, pane.command])

        return current_pane_id
