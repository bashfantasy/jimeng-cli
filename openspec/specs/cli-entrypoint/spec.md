# cli-entrypoint Specification

## Purpose

TBD - created by archiving change 'jimeng-cli-automation'. Update Purpose after archive.

## Requirements

### Requirement: CLI entry point with subcommands

The CLI tool SHALL be invocable as `jimeng` and SHALL support three subcommands: `login`, `generate`, and `logout`. Each subcommand SHALL display `--help` usage when invoked with the `-h` or `--help` flag.

#### Scenario: Invoking login subcommand

- **WHEN** the user runs `jimeng login`
- **THEN** the system SHALL start the QR code login flow

#### Scenario: Invoking generate subcommand

- **WHEN** the user runs `jimeng generate "a beautiful landscape"`
- **THEN** the system SHALL start the image generation flow with the given prompt

#### Scenario: Invoking logout subcommand

- **WHEN** the user runs `jimeng logout`
- **THEN** the system SHALL navigate to the logout URL and clear the local session file

#### Scenario: Unknown subcommand

- **WHEN** the user runs an unknown subcommand (e.g., `jimeng foo`)
- **THEN** the system SHALL print an error message and exit with a non-zero exit code


<!-- @trace
source: jimeng-cli-automation
updated: 2026-04-18
code:
  - monitor.log
  - src/jimeng_cli/browser.py
  - src/jimeng_cli/selectors.py
  - src/jimeng_cli/__init__.py
  - src/jimeng_cli/__pycache__/selectors.cpython-312.pyc
  - .agents/skills/spectra-ingest/SKILL.md
  - src/jimeng_cli/__pycache__/__init__.cpython-312.pyc
  - main.py
  - .agents/skills/spectra-debug/SKILL.md
  - .agents/skills/spectra-ask/SKILL.md
  - .python-version
  - README.md
  - src/jimeng_cli/commands/__init__.py
  - src/jimeng_cli/commands/__pycache__/login.cpython-312.pyc
  - uv.lock
  - .agents/skills/spectra-archive/SKILL.md
  - .agents/skills/spectra-audit/SKILL.md
  - .agents/skills/spectra-propose/SKILL.md
  - .agents/skills/spectra-apply/SKILL.md
  - shot_qrcode.png
  - src/jimeng_cli/__pycache__/main.cpython-312.pyc
  - CLAUDE.md
  - src/jimeng_cli/commands/__pycache__/logout.cpython-312.pyc
  - qrcode.png
  - shot_fullpage.png
  - src/jimeng_cli/__pycache__/browser.cpython-312.pyc
  - src/jimeng_cli/main.py
  - src/jimeng_cli/commands/generate.py
  - src/jimeng_cli/commands/__pycache__/__init__.cpython-312.pyc
  - debug_dom.html
  - shot_debug_page.png
  - full_monitor.log
  - .agents/skills/spectra-discuss/SKILL.md
  - src/jimeng_cli/commands/logout.py
  - src/jimeng_cli/commands/__pycache__/generate.cpython-312.pyc
  - AGENTS.md
  - jimeng_login_page.png
  - pyproject.toml
  - src/jimeng_cli/commands/login.py
  - .spectra.yaml
-->

---
### Requirement: Output directory option

The CLI SHALL accept an `--output-dir` option (default: `~/.openclaw/media/browser`) for all subcommands that produce image files.

#### Scenario: Custom output directory specified

- **WHEN** the user provides `--output-dir /path/to/dir`
- **THEN** the system SHALL save all images to that directory, creating it if it does not exist


<!-- @trace
source: jimeng-cli-automation
updated: 2026-04-18
code:
  - monitor.log
  - src/jimeng_cli/browser.py
  - src/jimeng_cli/selectors.py
  - src/jimeng_cli/__init__.py
  - src/jimeng_cli/__pycache__/selectors.cpython-312.pyc
  - .agents/skills/spectra-ingest/SKILL.md
  - src/jimeng_cli/__pycache__/__init__.cpython-312.pyc
  - main.py
  - .agents/skills/spectra-debug/SKILL.md
  - .agents/skills/spectra-ask/SKILL.md
  - .python-version
  - README.md
  - src/jimeng_cli/commands/__init__.py
  - src/jimeng_cli/commands/__pycache__/login.cpython-312.pyc
  - uv.lock
  - .agents/skills/spectra-archive/SKILL.md
  - .agents/skills/spectra-audit/SKILL.md
  - .agents/skills/spectra-propose/SKILL.md
  - .agents/skills/spectra-apply/SKILL.md
  - shot_qrcode.png
  - src/jimeng_cli/__pycache__/main.cpython-312.pyc
  - CLAUDE.md
  - src/jimeng_cli/commands/__pycache__/logout.cpython-312.pyc
  - qrcode.png
  - shot_fullpage.png
  - src/jimeng_cli/__pycache__/browser.cpython-312.pyc
  - src/jimeng_cli/main.py
  - src/jimeng_cli/commands/generate.py
  - src/jimeng_cli/commands/__pycache__/__init__.cpython-312.pyc
  - debug_dom.html
  - shot_debug_page.png
  - full_monitor.log
  - .agents/skills/spectra-discuss/SKILL.md
  - src/jimeng_cli/commands/logout.py
  - src/jimeng_cli/commands/__pycache__/generate.cpython-312.pyc
  - AGENTS.md
  - jimeng_login_page.png
  - pyproject.toml
  - src/jimeng_cli/commands/login.py
  - .spectra.yaml
-->

---
### Requirement: Verbose logging option

The CLI SHALL accept a `--verbose` flag that enables DEBUG-level log output.

#### Scenario: Verbose flag enabled

- **WHEN** the user provides `--verbose`
- **THEN** the system SHALL emit DEBUG and INFO logs to stdout
- **THEN** the system SHALL emit WARNING and ERROR logs to stderr

<!-- @trace
source: jimeng-cli-automation
updated: 2026-04-18
code:
  - monitor.log
  - src/jimeng_cli/browser.py
  - src/jimeng_cli/selectors.py
  - src/jimeng_cli/__init__.py
  - src/jimeng_cli/__pycache__/selectors.cpython-312.pyc
  - .agents/skills/spectra-ingest/SKILL.md
  - src/jimeng_cli/__pycache__/__init__.cpython-312.pyc
  - main.py
  - .agents/skills/spectra-debug/SKILL.md
  - .agents/skills/spectra-ask/SKILL.md
  - .python-version
  - README.md
  - src/jimeng_cli/commands/__init__.py
  - src/jimeng_cli/commands/__pycache__/login.cpython-312.pyc
  - uv.lock
  - .agents/skills/spectra-archive/SKILL.md
  - .agents/skills/spectra-audit/SKILL.md
  - .agents/skills/spectra-propose/SKILL.md
  - .agents/skills/spectra-apply/SKILL.md
  - shot_qrcode.png
  - src/jimeng_cli/__pycache__/main.cpython-312.pyc
  - CLAUDE.md
  - src/jimeng_cli/commands/__pycache__/logout.cpython-312.pyc
  - qrcode.png
  - shot_fullpage.png
  - src/jimeng_cli/__pycache__/browser.cpython-312.pyc
  - src/jimeng_cli/main.py
  - src/jimeng_cli/commands/generate.py
  - src/jimeng_cli/commands/__pycache__/__init__.cpython-312.pyc
  - debug_dom.html
  - shot_debug_page.png
  - full_monitor.log
  - .agents/skills/spectra-discuss/SKILL.md
  - src/jimeng_cli/commands/logout.py
  - src/jimeng_cli/commands/__pycache__/generate.cpython-312.pyc
  - AGENTS.md
  - jimeng_login_page.png
  - pyproject.toml
  - src/jimeng_cli/commands/login.py
  - .spectra.yaml
-->