# Herdr Compose (`herdr-compose`)

[![CI](https://github.com/USERNAME/herdr-compose/actions/workflows/ci.yml/badge.svg)](https://github.com/ropali/herdr-compose/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**`herdr-compose`** is a declarative workspace layout manager for [Herdr](https://herdr.dev). 

It allows you to define complex Herdr workspace configurations (workspaces, tabs, split directions, pane sizes, initial commands, and environment variables) in clean, human-readable YAML files (`herdr-compose.yaml` or `herdrlayout.yaml`).

---

## 🚀 Key Features

- 📑 **Declarative Workspaces & Tabs**: Define multiple workspaces and tabs in human-readable YAML.
- 💾 **Save & Install Configs**: Save user layouts directly to `~/.config/herdr-compose/<filename>` with a single command.
- 🪟 **Explicit Split Directions & Sizes**: Split panes with intuitive directions (`direction: right` / `vertical`) and percentage sizes (`size: 30%` or `size: 0.3`).
- 🏷️ **Named Pane References**: Name panes (`name: main_editor`) and split directly from them (`from: main_editor`).
- ⚡ **Shorthand Syntax**: Concise single-line pane definitions (`- nvim`) and workspace-level pane lists.
- ⚙️ **Command Auto-Launch**: Automatically run commands in specific panes upon creation (`nvim`, `npm run dev`, `opencode`).
- 🔑 **Environment Variables**: Pass custom environment variables (`env`) per workspace, tab, or pane.
- 🔍 **Dry-Run & Inspection**: Preview commands with `--dry-run` or inspect layout structure visually with `herdr-compose show`.

---

## 📦 Installation

You can install `herdr-compose` locally using `uv` or `pip`:

```bash
# Using uv (recommended)
uv pip install -e .

# Or standard pip
pip install -e .

# Or install globally as a tool with uv
uv tool install --editable .
```

---

## 🛠️ Usage & Commands

You can run `herdr-compose` either directly (if installed on PATH) or via `uv run`:

### 1. Save Configuration to `~/.config/herdr-compose/`
Validate and copy any layout YAML file into your user config directory (preserving the source filename):

```bash
# Direct command
herdr-compose save layout.yaml

# Via uv
uv run herdr-compose save layout.yaml
```

### 2. Apply Layout
```bash
# Apply auto-detected layout file
herdr-compose
# or
uv run herdr-compose

# Apply specific layout file
herdr-compose apply path/to/herdr-compose.yaml

# Save to ~/.config/herdr-compose/ AND apply simultaneously
herdr-compose apply path/to/my-layout.yaml --save

# Perform a dry-run (preview herdr CLI commands without executing)
herdr-compose apply layout.yaml --dry-run
```

### 3. Validate Layout Configuration
```bash
herdr-compose validate path/to/herdr-compose.yaml
# or
uv run herdr-compose validate path/to/herdr-compose.yaml
```

### 4. Display Layout Hierarchy
```bash
herdr-compose show path/to/herdr-compose.yaml
# or
uv run herdr-compose show path/to/herdr-compose.yaml
```

*Sample output:*
```
Layout Summary:
Workspace 1: backend-api (focused) [root: ~/code/backend-api]
  ├─ Tab 1: editor
  │  ├─ Pane 1 [main_editor] [root pane] (focused) -> `nvim`
  │  ├─ Pane 2 [side_tool] [split right, size 0.3] -> `opencode`
  │  └─ Pane 3 [bottom_term] [split down, size 0.3] (from main_editor)
  └─ Tab 2: watch server
     └─ Pane 1 [root pane] -> `cargo check --watch`
```

### 5. Initialize Starter Configuration
```bash
herdr-compose init
```

---

## 🔍 Search Priority Order

When no file path is specified, `herdr-compose` searches in the following order:

1. CLI argument parameter (`herdr-compose layout.yaml`)
2. `HERDR_COMPOSE_CONFIG` environment variable
3. `./herdr-compose.yaml`, `./herdrcompose.yaml`, `./herdrlayout.yaml`, or `./layout.yaml` (Current Working Directory)
4. `~/.config/herdr-compose/herdr-compose.yaml`
5. `~/.config/herdr-compose/layout.yaml`
6. `~/.config/herdr-compose/config.yaml`
7. `~/dotfiles/herdr/.config/herdr/herdrlayout.yaml`
8. `~/.config/herdr/herdrlayout.yaml`

---

## 📄 Configuration Reference & Examples

Save your configuration file as `herdr-compose.yaml` or `layout.yaml`.

- For full detailed schema reference, see **[docs/CONFIG_SPEC.md](docs/CONFIG_SPEC.md)**.
- For complete sample files, see **[examples/](examples/)**:
  - [`examples/complex_multi_workspace.yaml`](examples/complex_multi_workspace.yaml)
  - [`examples/full_workspace.yaml`](examples/full_workspace.yaml)
  - [`examples/multi_tab_layout.yaml`](examples/multi_tab_layout.yaml)

### Clean & Explicit Layout Example

```yaml
workspaces:
  - name: backend-api
    root: ~/code/backend-api
    focus: true
    env:
      RUST_LOG: info
    tabs:
      - label: dev
        panes:
          - name: editor
            command: nvim
            focus: true

          - name: sidebar
            direction: right
            size: 25%
            command: opencode

          - name: terminal
            direction: down
            size: 30%
            from: editor
            command: git status
```

---

## 🧪 Testing

Run unit tests using `pytest` or `uv`:

```bash
uv run --with pytest pytest
```

---

## 📄 License

Distributed under the MIT License.
