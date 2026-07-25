# Herdr Compose (`herdr-compose`)

[![CI](https://github.com/USERNAME/herdr-compose/actions/workflows/ci.yml/badge.svg)](https://github.com/USERNAME/herdr-compose/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**`herdr-compose`** is a declarative workspace layout manager for [Herdr](https://herdr.dev) — the terminal workspace manager for AI coding agents and developers.

It allows you to define complex Herdr workspace configurations (workspaces, tabs, split directions, pane sizes, initial commands, and environment variables) in clean, human-readable YAML files (`herdr-compose.yaml` or `herdrlayout.yaml`).

---

## 🚀 Key Features

- 📑 **Declarative Workspaces & Tabs**: Define multiple workspaces and tabs in human-readable YAML.
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

### 1. Initialize Starter Configuration (`init`)
Generate a starter configuration file directly inside `~/.config/herdr-compose/` and print its full absolute file path:

```bash
# Generates ~/.config/herdr-compose/herdr-compose.yaml
herdr-compose init

# Generates ~/.config/herdr-compose/my-custom-layout.yaml
herdr-compose init my-custom-layout

# Generates explicit local path ./local-layout.yaml
herdr-compose init ./local-layout.yaml
```

*Sample terminal output:*
```
✓ Created starter layout config at: /home/user/.config/herdr-compose/herdr-compose.yaml
```

---

### 2. Save, List & Remove Configurations in `~/.config/herdr-compose/`

```bash
# Save layout to ~/.config/herdr-compose/
herdr-compose save layout.yaml

# List all saved configurations in ~/.config/herdr-compose/
herdr-compose list

# Remove a saved layout configuration file (extension optional)
herdr-compose remove layout
# or aliases
herdr-compose rm layout
herdr-compose delete layout.yaml
```

---

### 3. Inspect Layout Hierarchy Tree (`show`)
Display an ASCII tree visualization of the workspace, tab, and pane hierarchy without executing any terminal commands.

`show` supports extension-agnostic path resolution:
- **Saved Filename**: `herdr-compose show layout` (automatically finds `~/.config/herdr-compose/layout.yaml`)
- **Explicit File Path**: `herdr-compose show path/to/my-layout.yaml`
- **Default**: `herdr-compose show` (inspects `~/.config/herdr-compose/herdr-compose.yaml`)

```bash
herdr-compose show layout
# or
uv run herdr-compose show examples/complex_multi_workspace.yaml
```

---

### 4. Apply Layout (`apply`)
Create workspaces, tabs, panes, and run configured commands:

```bash
# Apply default layout (~/.config/herdr-compose/herdr-compose.yaml)
herdr-compose

# Apply specific layout file (extension optional)
herdr-compose apply layout

# Save to ~/.config/herdr-compose/ AND apply simultaneously
herdr-compose apply path/to/my-layout.yaml --save

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

## 🔍 Search Priority Order

When no file path is specified, `herdr-compose` searches in the following order:

1. **CLI argument parameter** (e.g., `herdr-compose apply path/to/file.yaml` or `herdr-compose apply file`)
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
