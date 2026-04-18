## ADDED Requirements

### Requirement: Save browser session state

After a successful login, the system SHALL serialize the Playwright browser context state (cookies and localStorage) and save it to `~/.jimeng/session.json`. The `~/.jimeng/` directory SHALL be created if it does not exist.

#### Scenario: Session saved after login

- **WHEN** a login flow completes successfully
- **THEN** the system SHALL call `browser_context.storage_state(path="~/.jimeng/session.json")`
- **THEN** the session file SHALL exist on disk and be readable JSON

### Requirement: Restore browser session state

Before navigating to any authenticated page, the system SHALL load the session from `~/.jimeng/session.json` and pass it to the new browser context.

#### Scenario: Valid session file exists

- **WHEN** `~/.jimeng/session.json` exists and is valid JSON
- **THEN** the system SHALL create a browser context with `storage_state` pointing to the session file

#### Scenario: Session file missing

- **WHEN** `~/.jimeng/session.json` does not exist
- **THEN** the system SHALL print an error message to stderr indicating session is missing and asking the user to run `jimeng login`
- **THEN** the system SHALL exit with a non-zero exit code

### Requirement: Clear session on logout

The `logout` subcommand SHALL delete `~/.jimeng/session.json` after navigating to the logout URL.

#### Scenario: Logout clears session file

- **WHEN** `jimeng logout` completes navigation to the logout URL
- **THEN** the system SHALL delete `~/.jimeng/session.json` if it exists
- **THEN** the system SHALL print "Logged out successfully." to stdout
