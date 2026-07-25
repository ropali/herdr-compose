# Herdr Compose (`herdr-compose`)

[![CI](https://github.com/USERNAME/herdr-compose/actions/workflows/ci.yml/badge.svg)](https://github.com/USERNAME/herdr-compose/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**`herdr-compose`** is a declarative workspace layout manager for [Herdr](https://herdr.dev) — the terminal workspace manager for AI coding agents and developers.

It allows you to define complex Herdr workspace configurations (workspaces, tabs, split directions, pane sizes, initial commands, and environment variables) in clean, human-readable YAML files (`herdr-compose.yaml` or `herdrlayout.yaml`).

---

## 🚀 Key Features

- 📑 **Declarative Workspaces & Tabs**: Define multiple workspaces and tabs in human-readable YAML.
- ⭐ **Active Default Layout Selection**: Set your active default configuration with `herdr-compose use <name>`, allowing seamless default execution without typing file paths every time.
- 💾 **Save & Manage Layouts**: Save your layout files into `~/.config/herdr-compose/`, list them with `herdr-compose list`, or remove them with `herdr-compose remove`.
- ⚙️ **Starter Template Initialization**: Instantly generate starter configuration files in `~/.config/herdr-compose/` with `herdr-compose init`.
- 🔍 **Visual Layout Inspection**: Inspect the full workspace/tab/pane hierarchy tree using `herdr-compose show`.
- 🪟 **Explicit Split Directions & Sizes**: Split panes with intuitive directions (`direction: right` / `vertical`) and percentage sizes (`size: 30%` or `size: 0.3`).
- 🏷️ **Named Pane References**: Name panes (`name: main_editor`) and split directly from them (`from: main_editor`).
- ⚡ **Shorthand Syntax**: Concise single-line pane definitions (`- nvim`) and workspace-level pane lists.
- ⚙️ **Command Auto-Launch**: Automatically run commands in specific panes upon creation (`nvim`, `npm run dev`, `opencode`).
- 🔑 **Environment Variables**: Pass custom environment variables (`env`) per workspace, tab, or pane.
- 🔍 **Dry-Run Mode**: Preview generated `herdr` CLI execution commands with `herdr-compose apply --dry-run`.

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

### 1. Set Active Default Layout (`use`)
Set the active default layout configuration file. When running `herdr-compose` without arguments, it automatically executes your active default layout:

```bash
# Set active default configuration (extension optional)
herdr-compose use backend
# or
herdr-compose use frontend.yaml

# Aliases
herdr-compose select backend
herdr-compose set-default backend
```

---

### 2. Save, List & Remove Configurations in `~/.config/herdr-compose/`

```bash
# Save layout to ~/.config/herdr-compose/
herdr-compose save layout.yaml

# List all saved configurations (shows active default with ★ tag)
herdr-compose list

# Remove a saved layout configuration file (extension optional)
herdr-compose remove layout
# or aliases
herdr-compose rm layout
herdr-compose delete layout.yaml
```

*Sample list output:*
```
Saved configuration files in '/home/user/.config/herdr-compose':

  1. backend.yaml (1 workspace) ★ [active default]
  2. frontend.yaml (2 workspaces)
  3. layout.yaml (2 workspaces)
```

---

### 3. Inspect Layout Hierarchy Tree (`show`)
Display an ASCII tree visualization of the workspace, tab, and pane hierarchy without executing any terminal commands.

```bash
# Inspect active default layout
herdr-compose show

# Inspect specific saved layout (extension optional)
herdr-compose show backend

# Inspect explicit file path
herdr-compose show examples/complex_multi_workspace.yaml
```

---

### 4. Apply Layout (`apply`)
Create workspaces, tabs, panes, and run configured commands:

```bash
# Apply active default layout (~/.config/herdr-compose/.active)
herdr-compose

# Apply specific layout file (extension optional)
herdr-compose apply backend

# Save to ~/.config/herdr-compose/ AND set as active default simultaneously
herdr-compose save my-layout.yaml --use

# Perform a dry-run (preview generated herdr commands without executing)
herdr-compose apply --dry-run
```

---

### 5. Initialize Starter Configuration (`init`)
Generate a starter configuration file directly inside `~/.config/herdr-compose/`:

```bash
# Generates ~/.config/herdr-compose/herdr-compose.yaml & sets as active default
herdr-compose init

# Generates ~/.config/herdr-compose/my-custom-layout.yaml
herdr-compose init my-custom-layout
```

---

## 🔍 Search Priority Order

When no file path is specified, `herdr-compose` searches in the following order:

1. **CLI argument parameter** (e.g., `herdr-compose apply backend` or `herdr-compose apply path/to/file.yaml`)
2. **`HERDR_COMPOSE_CONFIG` environment variable**
3. **Active default configuration** (`~/.config/herdr-compose/.active`)
4. **Default candidate path**: `~/.config/herdr-compose/herdr-compose.yaml`

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
