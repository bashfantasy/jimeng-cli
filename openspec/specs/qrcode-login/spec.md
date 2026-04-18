# qrcode-login Specification

## Purpose

TBD - created by archiving change 'jimeng-cli-automation'. Update Purpose after archive.

## Requirements

### Requirement: Navigate to OAuth login page

The system SHALL open the Jimeng OAuth QR code login URL in a headless Chromium browser.

The login URL is:
```
https://open.douyin.com/platform/oauth/pc/auth?client_key=aw97st49sighch6k&response_type=code&scope=user_info&state=e53c3ce23gAToVCgoVPZIDJmOGFiYTUwNzFlNTgxZmRjZjc2ZWJmNWRiNjBhMGY1oU7ZOGh0dHBzOi8vamltZW5nLmppYW55aW5nLmNvbS9haS10b29sL3RoaXJkLXBhcnR5LWNhbGxiYWNroVYBoUkAoUQAoUHSAAfWn6FNAKFIs2ppbWVuZy5qaWFueWluZy5jb22hUgKiUEzROl6mQUNUSU9OoKFM2ShodHRwczovL2ppbWVuZy5qaWFueWluZy5jb20vYWktdG9vbC9ob21loVTZIGZmYzBjNzIxMGNiMzNlZGZkOGJlMTU5M2I1YmJmY2EyoVcAoUYAolNBAKFVwqJNTMI%3D&redirect_uri=https%3A%2F%2Fjimeng.jianying.com%2Fpassport%2Fweb%2Fweb_login_success
```

#### Scenario: Login page opens successfully

- **WHEN** `jimeng login` is executed
- **THEN** the system SHALL navigate to the OAuth URL and wait up to 15 seconds for the page DOM to be interactive


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
### Requirement: Detect and capture QR code image

After the login page loads, the system SHALL wait up to 30 seconds for the QR code image element to appear, then capture a screenshot of the QR code element and save it to the output directory.

#### Scenario: QR code element appears within timeout

- **WHEN** the QR code DOM element becomes visible within 30 seconds
- **THEN** the system SHALL take an element-level screenshot and save it as `qrcode.png` in the output directory
- **THEN** the system SHALL print the image file path to stdout

#### Scenario: QR code element not found within timeout

- **WHEN** no QR code element is detected within 30 seconds
- **THEN** the system SHALL save a full-page screenshot as `qrcode_fallback.png`
- **THEN** the system SHALL print a warning to stderr and continue polling for login completion


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
### Requirement: Poll for login completion

After capturing the QR code, the system SHALL continuously check the current page URL to detect whether the user has scanned the QR code and the OAuth redirect has occurred.

The system SHALL treat login as successful when the page URL contains `jimeng.jianying.com/ai-tool/third-party-callback`.

The system SHALL poll for up to 120 seconds before timing out.

#### Scenario: User scans QR code within timeout

- **WHEN** the page URL changes to contain `/ai-tool/third-party-callback` within 120 seconds
- **THEN** the system SHALL save the browser session state to `~/.jimeng/session.json`
- **THEN** the system SHALL print "Login successful" to stdout and exit with code 0

#### Scenario: Login timeout exceeded

- **WHEN** 120 seconds elapse without detecting the callback URL
- **THEN** the system SHALL print an error message to stderr and exit with a non-zero exit code


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
### Requirement: Anti-bot browser configuration

The headless Chromium instance SHALL be launched with settings designed to avoid bot detection.

#### Scenario: Browser launched with stealth settings

- **WHEN** any browser session is started
- **THEN** the system SHALL set a realistic `User-Agent` header (matching a recent Chrome on Linux)
- **THEN** the system SHALL disable the `AutomationControlled` blink feature
- **THEN** the system SHALL inject an init script that makes `navigator.webdriver` return `undefined`

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