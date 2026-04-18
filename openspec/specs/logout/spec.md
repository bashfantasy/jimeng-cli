# logout Specification

## Purpose

TBD - created by archiving change 'jimeng-cli-automation'. Update Purpose after archive.

## Requirements

### Requirement: Navigate to logout URL

The `logout` subcommand SHALL navigate the browser to the Jimeng logout URL.

The logout URL is: `https://jimeng.jianying.com/passport/web/logout`

The system SHALL wait up to 10 seconds for the page to load before proceeding.

#### Scenario: Logout navigation succeeds

- **WHEN** `jimeng logout` is executed
- **THEN** the system SHALL open a browser and navigate to the logout URL
- **THEN** the system SHALL wait for the page to finish loading

#### Scenario: Logout navigation fails due to timeout or network error

- **WHEN** the logout URL cannot be loaded within 10 seconds
- **THEN** the system SHALL log a warning to stderr but SHALL still proceed to delete the local session file

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