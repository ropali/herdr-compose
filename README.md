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

### 1. List Saved Configurations (`list`)
List all saved configuration files residing in `~/.config/herdr-compose/` along with workspace count metadata:

```bash
herdr-compose list
# or
uv run herdr-compose list
```

*Sample terminal output:*
```
Saved configuration files in '/home/user/.config/herdr-compose':

  1. layout.yaml (2 workspaces)
  2. backend-stack.yaml (1 workspace)
```

---

### 2. Inspect Layout Hierarchy Tree (`show`)
Display an ASCII tree visualization of the workspace, tab, and pane hierarchy without executing any terminal commands.

`show` supports flexible path resolution:
- **Explicit File Path**: `herdr-compose show path/to/my-layout.yaml`
- **Saved Filename**: `herdr-compose show layout.yaml` (automatically looks in `~/.config/herdr-compose/`)
- **Default**: `herdr-compose show` (inspects `~/.config/herdr-compose/herdr-compose.yaml`)

```bash
herdr-compose show layout.yaml
# or
uv run herdr-compose show examples/complex_multi_workspace.yaml
```

*Sample tree output:*
```
Layout loaded from '/home/user/code/herdr-compose/examples/complex_multi_workspace.yaml':

Layout Summary:
Workspace 1: backend-api (focused) [root: ~/code/backend-api]
  ├─ Tab 1: editor
  │  ├─ Pane 1 [main_editor] [root pane] (focused) -> `nvim`
  │  ├─ Pane 2 [side_tool] [split right, size 0.3] -> `opencode`
  │  └─ Pane 3 [bottom_term] [split down, size 0.3] (from main_editor)
  └─ Tab 2: watch server
     └─ Pane 1 [root pane] -> `cargo check --watch`
Workspace 2: docs-server [root: ~/code/docs-server]
  ├─ Tab 1: editor
  │  ├─ Pane 1 [main_editor] [root pane] (focused) -> `nvim`
  │  ├─ Pane 2 [side_tool] [split right, size 0.3] -> `opencode`
  │  └─ Pane 3 [bottom_term] [split down, size 0.3] (from main_editor)
  └─ Tab 2: watch server
     └─ Pane 1 [root pane] -> `mdbook serve --open`
```

---

### 3. Save Configuration (`save`)
Validate and save any user layout file to your `~/.config/herdr-compose/` user directory:

```bash
# Saves to ~/.config/herdr-compose/layout.yaml
herdr-compose save layout.yaml

# Save and apply simultaneously
herdr-compose apply layout.yaml --save
```

---

### 4. Apply Layout (`apply`)
Create workspaces, tabs, panes, and run configured commands:

```bash
# Apply default layout (~/.config/herdr-compose/herdr-compose.yaml)
herdr-compose

# Apply specific layout file
herdr-compose apply path/to/herdr-compose.yaml

# Perform a dry-run (preview generated herdr commands without executing)
herdr-compose apply layout.yaml --dry-run
```

---

### 5. Validate Configuration (`validate`)
Check if a layout YAML file is valid:

```bash
herdr-compose validate path/to/herdr-compose.yaml
```

---

### 6. Initialize Starter Configuration (`init`)
Generate a starter `herdr-compose.yaml` file:

```bash
herdr-compose init
```

---

## 🔍 Search Priority Order

When no file path is specified, `herdr-compose` searches in the following order:

1. **CLI argument parameter** (e.g., `herdr-compose apply path/to/file.yaml`)
2. **`HERDR_COMPOSE_CONFIG` environment variable**
3. **Default candidate path**: `~/.config/herdr-compose/herdr-compose.yaml`

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
