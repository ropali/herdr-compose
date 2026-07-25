# Herdr Compose (`herdr-compose`)

[![CI](https://github.com/USERNAME/herdr-compose/actions/workflows/ci.yml/badge.svg)](https://github.com/USERNAME/herdr-compose/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**`herdr-compose`** is a declarative workspace layout manager for [Herdr](https://herdr.dev) — the terminal workspace manager for AI coding agents and developers.

It allows you to define complex Herdr workspace configurations (workspaces, tabs, split directions, pane sizes, initial commands, and environment variables) in clean, human-readable YAML files (`herdr-compose.yaml` or `herdrlayout.yaml`).

---

## 🚀 Key Features

- 📑 **Declarative Workspaces & Tabs**: Define multiple workspaces and tabs in human-readable YAML.
- 💾 **Save & Manage Layouts**: Save your layout files into `~/.config/herdr-compose/` and list them easily with `herdr-compose list`.
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
uv pip install -e ".[dev]"

# Or standard pip
pip install -e .

# Or install globally as a tool with uv
uv tool install --editable .
```

---

## 🛠️ Usage & Commands

You can run `herdr-compose` either directly (if installed on PATH) or via `uv run`:

### 1. Save & List Configurations in `~/.config/herdr-compose/`
Validate and save any layout YAML file to your user config directory, and view all saved files:

```bash
# Save layout to ~/.config/herdr-compose/
herdr-compose save layout.yaml
# or
uv run herdr-compose save layout.yaml

# List all saved configurations in ~/.config/herdr-compose/
herdr-compose list
# or
uv run herdr-compose list
```

*Sample list output:*
```
Saved configuration files in '~/.config/herdr-compose':

  1. layout.yaml (2 workspaces)
  2. my-backend-stack.yaml (1 workspace)
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
```

### 4. Display Layout Hierarchy
```bash
herdr-compose show path/to/herdr-compose.yaml
```

### 5. Initialize Starter Configuration
```bash
herdr-compose init
```

---

## 🔍 Search Priority Order

When no file path is specified, `herdr-compose` searches in the following order:

1. CLI argument parameter (e.g., `herdr-compose path/to/file.yaml`)
2. `HERDR_COMPOSE_CONFIG` environment variable
3. Default candidate path: `~/.config/herdr-compose/herdr-compose.yaml`

---

## 📄 Configuration Reference & Examples

Save your configuration file as `herdr-compose.yaml` or `layout.yaml`.

- For full detailed schema reference, see **[docs/CONFIG_SPEC.md](docs/CONFIG_SPEC.md)**.
- For complete sample files, see **[examples/](examples/)**:
  - [`examples/complex_multi_workspace.yaml`](examples/complex_multi_workspace.yaml)
  - [`examples/full_workspace.yaml`](examples/full_workspace.yaml)
  - [`examples/multi_tab_layout.yaml`](examples/multi_tab_layout.yaml)

---

## 🧪 Testing

Run unit tests using `pytest` or `uv`:

```bash
uv run pytest
```

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
