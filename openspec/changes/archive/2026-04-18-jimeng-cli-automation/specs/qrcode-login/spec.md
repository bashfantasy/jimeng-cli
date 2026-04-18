## ADDED Requirements

### Requirement: Navigate to OAuth login page

The system SHALL open the Jimeng OAuth QR code login URL in a headless Chromium browser.

The login URL is:
```
https://open.douyin.com/platform/oauth/pc/auth?client_key=aw97st49sighch6k&response_type=code&scope=user_info&state=e53c3ce23gAToVCgoVPZIDJmOGFiYTUwNzFlNTgxZmRjZjc2ZWJmNWRiNjBhMGY1oU7ZOGh0dHBzOi8vamltZW5nLmppYW55aW5nLmNvbS9haS10b29sL3RoaXJkLXBhcnR5LWNhbGxiYWNroVYBoUkAoUQAoUHSAAfWn6FNAKFIs2ppbWVuZy5qaWFueWluZy5jb22hUgKiUEzROl6mQUNUSU9OoKFM2ShodHRwczovL2ppbWVuZy5qaWFueWluZy5jb20vYWktdG9vbC9ob21loVTZIGZmYzBjNzIxMGNiMzNlZGZkOGJlMTU5M2I1YmJmY2EyoVcAoUYAolNBAKFVwqJNTMI%3D&redirect_uri=https%3A%2F%2Fjimeng.jianying.com%2Fpassport%2Fweb%2Fweb_login_success
```

#### Scenario: Login page opens successfully

- **WHEN** `jimeng login` is executed
- **THEN** the system SHALL navigate to the OAuth URL and wait up to 15 seconds for the page DOM to be interactive

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

### Requirement: Anti-bot browser configuration

The headless Chromium instance SHALL be launched with settings designed to avoid bot detection.

#### Scenario: Browser launched with stealth settings

- **WHEN** any browser session is started
- **THEN** the system SHALL set a realistic `User-Agent` header (matching a recent Chrome on Linux)
- **THEN** the system SHALL disable the `AutomationControlled` blink feature
- **THEN** the system SHALL inject an init script that makes `navigator.webdriver` return `undefined`
