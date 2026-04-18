# image-generation Specification

## Purpose

TBD - created by archiving change 'jimeng-cli-automation'. Update Purpose after archive.

## Requirements

### Requirement: Navigate to image generation page

The system SHALL navigate to the Jimeng image generation URL after restoring the session state.

The image generation URL is: `https://jimeng.jianying.com/ai-tool/home?type=image&workspace=undefined`

#### Scenario: Navigation to generation page

- **WHEN** `jimeng generate` is executed
- **THEN** the system SHALL restore session from `~/.jimeng/session.json` and navigate to the image generation URL
- **WHEN** the page redirects to the login URL instead
- **THEN** the system SHALL print an error message to stderr indicating session expiration and asking the user to run `jimeng login`
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
### Requirement: Dismiss modal dialogs

After the image generation page loads, the system SHALL attempt to close any modal dialogs or overlays that appear before interacting with the prompt input.

The system SHALL try a predefined list of close button selectors and SHALL click the first one that is visible. The system SHALL wait no longer than 5 seconds for modals to appear before proceeding.

#### Scenario: Modal dialog present

- **WHEN** a modal close button matching a known selector is visible within 5 seconds of page load
- **THEN** the system SHALL click the close button
- **THEN** the system SHALL wait 1 second and check again until no more modals are detected or 5 seconds total have elapsed

#### Scenario: Unknown modal not matched by selectors

- **WHEN** no known modal close selector is matched but an overlay still blocks interaction
- **THEN** the system SHALL send the `Escape` key as a fallback modal-dismiss action

#### Scenario: No modal dialog present

- **WHEN** no modal close button is detected within 5 seconds
- **THEN** the system SHALL proceed without error


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
### Requirement: Verify image generation mode

After dismissing modals, the system SHALL verify that the creative mode is set to image generation (not Agent mode).

#### Scenario: Agent mode detected on page load

- **WHEN** the page shows text indicating Agent mode is active (e.g., text matching "Agent" or "智能体" near the prompt area)
- **THEN** the system SHALL reload the page (up to 3 retries)
- **THEN** the system SHALL repeat modal dismissal and mode verification after each reload

#### Scenario: Image generation mode confirmed

- **WHEN** the prompt input area is visible and Agent mode text is NOT detected
- **THEN** the system SHALL proceed to prompt submission


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
### Requirement: Submit generation prompt

The system SHALL write a debug HTML snapshot to `debug_dom.html` before trying to locate the prompt input. The system SHALL locate the prompt input text area, type the user-supplied prompt text into it, and trigger generation by pressing the Enter key.

#### Scenario: Successful prompt submission

- **WHEN** the prompt input element is found and the prompt string is non-empty
- **THEN** the system SHALL click the input element, type the prompt text, and press Enter
- **THEN** the system SHALL log "Prompt submitted, waiting for generation..." to stdout

#### Scenario: Prompt input not found on first attempt

- **WHEN** the prompt input element is not found within 15 seconds
- **THEN** the system SHALL reload the page and retry prompt submission
- **THEN** the system SHALL retry up to 2 attempts total

#### Scenario: Prompt input still not found after retries

- **WHEN** prompt submission still fails after 2 total attempts
- **THEN** the system SHALL print an error to stderr and exit with a non-zero exit code


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
### Requirement: Wait for and save newly generated images

The system SHALL identify the set of image elements already present on the page before submitting the prompt. After submission, it SHALL wait for exactly 4 new image elements (whose src URLs are not in the pre-submission set) to appear, then download and save them.

The system SHALL wait up to the configured timeout (default: 180 seconds) for all 4 new images to appear.

The system SHALL treat new image URLs as a set-difference result, so download order SHALL NOT be required to match the on-page visual order.

#### Scenario: 4 new images appear within timeout

- **WHEN** 4 image elements with new src URLs become visible in the generation results area
- **THEN** the system SHALL start downloading those images by src URL and save successful downloads as `image_1.png`, `image_2.png`, `image_3.png`, `image_4.png` in the output directory
- **THEN** the system SHALL print each successful saved file path to stdout

#### Scenario: Generation timeout exceeded

- **WHEN** fewer than 4 new images appear within the timeout period
- **THEN** the system SHALL print an error to stderr indicating how many images were found and exit with a non-zero exit code

#### Scenario: Partial download success

- **WHEN** 4 new image URLs are detected but only some downloads succeed
- **THEN** the system SHALL complete successfully if at least 1 image is saved

#### Scenario: All downloads fail

- **WHEN** no image is saved after download attempts
- **THEN** the system SHALL print an error to stderr and exit with a non-zero exit code

#### Scenario: Generation page redirects to login

- **WHEN** the page URL changes to a login URL during the wait period
- **THEN** the system SHALL print an error message to stderr indicating session expiration during generation and asking the user to run `jimeng login`
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