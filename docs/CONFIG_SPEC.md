# Herdr Compose Configuration Specification

This document details the complete configuration schema for `herdr-compose` (`herdr-compose.yaml` or `herdrlayout.yaml`).

---

## 📋 Overview & Syntax Hierarchy

```
LayoutConfig (Root)
└── workspaces: [ WorkspaceConfig ]
    ├── name: string
    ├── root: string (optional)
    ├── focus: boolean (optional)
    ├── env: dict / list (optional)
    └── tabs: [ TabConfig ]  (or `panes` shorthand)
        ├── label: string (optional)
        ├── cwd: string (optional)
        └── panes: [ PaneConfig | string ]
            ├── name: string (optional)
            ├── command: string (optional)
            ├── direction: "right" | "down" | "horizontal" | "vertical"
            ├── size: percentage ("30%") or float (0.3)
            ├── from: "root" | "previous" | <pane_name> | <index>
            ├── focus: boolean (optional)
            └── env: dict / list (optional)
```

---

## 💡 Quick Examples

### 1. Minimal Shorthand Layout
```yaml
workspaces:
  - name: dev
    root: ~/src/app
    panes:
      - nvim
      - direction: right
        size: 30%
        command: npm run dev
```

### 2. Multi-Tab Layout with Named Panes
```yaml
workspaces:
  - name: backend
    root: ~/Workspace/backend
    focus: true
    env:
      RUST_LOG: info
    tabs:
      - label: code
        panes:
          - name: main_editor
            command: nvim
            focus: true

          - name: compiler
            direction: right
            size: 30%
            command: cargo check --watch

          - name: terminal
            direction: down
            size: 25%
            from: main_editor

      - label: database
        panes:
          - command: psql -U postgres
```

---

## ⚙️ Field Definitions

### 1. Workspace Configuration (`workspaces[]`)

| Property | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` / `workspace` | `string` | **Required** | Display label / name for the workspace. |
| `root` | `string` | `None` | Default working directory for the workspace (expands `~` and env vars). |
| `focus` | `boolean` | `false` | Whether to focus this workspace on creation. |
| `env` | `dict` / `list` | `{}` | Environment variables for processes launched in this workspace. |
| `panes` | `list` | `None` | **Shorthand**: Define panes directly on workspace if single tab. |
| `tabs` | `list` | `[]` | List of tab configurations. |

### 2. Tab Configuration (`tabs[]`)

| Property | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `label` / `name` | `string` | `None` | Display name for the tab. |
| `cwd` | `string` | `workspace.root` | Working directory for commands launched in this tab. |
| `env` | `dict` / `list` | `{}` | Environment variables for processes in this tab. |
| `panes` | `list` | `[]` | List of pane configurations or command strings. |

### 3. Pane Configuration (`panes[]`)

Panes can be specified either as a simple string (`- nvim`) or as a key-value object:

| Property | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` / `id` | `string` | `None` | Optional identifier so subsequent panes can reference it in `from`. |
| `command` / `run` | `string` | `None` | Command to execute in the pane. |
| `direction` / `split` | `string` | `"right"` | Split direction: `"right"`, `"down"`, `"horizontal"`, `"vertical"`. |
| `size` (or `ratio`) | `string` / `float` | `None` | Size allocated to **this new pane**. E.g., `"30%"`, `30%`, `0.3`. |
| `from` / `target` | `string` | `"previous"` | Source pane to split from: `"root"`, `"previous"`, `<pane_name>`, or index integer (`0`). |
| `focus` | `boolean` | `false` | Whether to focus this pane after creation. |
| `cwd` | `string` | `tab.cwd` | Working directory for this pane. |
| `env` | `dict` / `list` | `{}` | Environment variables for process launched in this pane. |

---

## 🎯 Split Direction Aliases

- **Horizontal splits**: `right`, `r`, `horizontal`, `h`
- **Vertical splits**: `down`, `d`, `bottom`, `vertical`, `v`

---

## 📏 Size Parameter Specification

The `size` property specifies the fraction/percentage of space given to **the new pane**:

- Percentage: `size: 30%` or `size: "30%"` (allocates 30% width/height to new pane).
- Float decimal: `size: 0.3` (allocates 30% width/height to new pane).
- `ratio` is also preserved as a backward-compatible alias for `size`.
