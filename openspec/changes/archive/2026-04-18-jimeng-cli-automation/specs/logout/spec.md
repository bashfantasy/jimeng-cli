## ADDED Requirements

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
