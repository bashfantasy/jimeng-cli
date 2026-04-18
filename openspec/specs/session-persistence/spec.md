# session-persistence Specification

## Purpose

TBD - created by archiving change 'jimeng-cli-automation'. Update Purpose after archive.

## Requirements

### Requirement: Save browser session state

After a successful login, the system SHALL serialize the Playwright browser context state (cookies and localStorage) and save it to `~/.jimeng/session.json`. The `~/.jimeng/` directory SHALL be created if it does not exist.

#### Scenario: Session saved after login

- **WHEN** a login flow completes successfully
- **THEN** the system SHALL call `browser_context.storage_state(path="~/.jimeng/session.json")`
- **THEN** the session file SHALL exist on disk and be readable JSON


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
### Requirement: Restore browser session state

Before navigating to any authenticated page, the system SHALL load the session from `~/.jimeng/session.json` and pass it to the new browser context.

#### Scenario: Valid session file exists

- **WHEN** `~/.jimeng/session.json` exists and is valid JSON
- **THEN** the system SHALL create a browser context with `storage_state` pointing to the session file

#### Scenario: Session file missing

- **WHEN** `~/.jimeng/session.json` does not exist
- **THEN** the system SHALL print an error message to stderr indicating session is missing and asking the user to run `jimeng login`
- **THEN** the system SHALL exit with a non-zero exit code


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
### Requirement: Clear session on logout

The `logout` subcommand SHALL delete `~/.jimeng/session.json` after navigating to the logout URL.

#### Scenario: Logout clears session file

- **WHEN** `jimeng logout` completes navigation to the logout URL
- **THEN** the system SHALL delete `~/.jimeng/session.json` if it exists
- **THEN** the system SHALL print "Logged out successfully." to stdout

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