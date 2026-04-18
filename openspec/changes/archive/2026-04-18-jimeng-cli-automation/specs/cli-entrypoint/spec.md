## ADDED Requirements

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

### Requirement: Output directory option

The CLI SHALL accept an `--output-dir` option (default: `~/.openclaw/media/browser`) for all subcommands that produce image files.

#### Scenario: Custom output directory specified

- **WHEN** the user provides `--output-dir /path/to/dir`
- **THEN** the system SHALL save all images to that directory, creating it if it does not exist

### Requirement: Verbose logging option

The CLI SHALL accept a `--verbose` flag that enables DEBUG-level log output.

#### Scenario: Verbose flag enabled

- **WHEN** the user provides `--verbose`
- **THEN** the system SHALL emit DEBUG and INFO logs to stdout
- **THEN** the system SHALL emit WARNING and ERROR logs to stderr
