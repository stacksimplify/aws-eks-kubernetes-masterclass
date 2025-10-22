# WebSecAudit - Comprehensive Website Security Scanner

A state-of-the-art security scanning tool that performs comprehensive vulnerability assessments on web applications.

## Features

WebSecAudit is a powerful security scanner that checks for vulnerabilities across multiple security domains:

### Security Categories Tested

- **SSL/TLS Security**
  - Certificate validation and expiration
  - Protocol version checks (SSLv3, TLS 1.0, 1.1, 1.2, 1.3)
  - Weak cipher suite detection
  - Self-signed certificate detection

- **HTTP Security Headers**
  - HSTS (HTTP Strict Transport Security)
  - Content Security Policy (CSP)
  - X-Frame-Options (Clickjacking protection)
  - X-Content-Type-Options
  - X-XSS-Protection
  - Referrer-Policy
  - Permissions-Policy
  - Cookie security attributes (Secure, HttpOnly, SameSite)

- **Cross-Site Scripting (XSS)**
  - Reflected XSS detection
  - DOM-based XSS indicators
  - Form input validation testing

- **SQL Injection**
  - Error-based SQL injection detection
  - Form and URL parameter testing
  - Database error message detection

- **Authentication & Session Security**
  - Insecure authentication forms
  - Password field security
  - Session token exposure
  - HTTP vs HTTPS authentication

- **CORS & CSRF**
  - CORS misconfiguration detection
  - Wildcard origin issues
  - Null origin vulnerabilities
  - CSRF token validation

- **Information Disclosure**
  - Sensitive file exposure (.env, .git, backups)
  - HTML comment analysis
  - Directory listing detection
  - Admin panel discovery
  - Detailed error messages
  - Version information disclosure

- **Technology Fingerprinting**
  - Web framework detection
  - Server identification
  - JavaScript library detection
  - CMS detection (WordPress, Drupal, Joomla, etc.)

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. Clone or download the tool:
```bash
cd websec-audit
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make the scanner executable (Linux/Mac):
```bash
chmod +x scanner.py
```

## Usage

### Basic Scan

```bash
python scanner.py https://example.com
```

### With Verbose Output

```bash
python scanner.py https://2rbc-ai.com -v
```

### URL Without Protocol

The tool automatically adds HTTPS if no protocol is specified:

```bash
python scanner.py example.com
```

### Command-Line Options

```
usage: scanner.py [-h] [-v] [--version] url

positional arguments:
  url             Target URL to scan (e.g., https://example.com)

optional arguments:
  -h, --help      Show this help message and exit
  -v, --verbose   Enable verbose output for debugging
  --version       Show program's version number and exit
```

## Output

WebSecAudit generates three types of output:

### 1. Console Output

Real-time scan progress and summary displayed in the terminal with color-coded severity levels:
- **CRITICAL** - Immediate action required
- **HIGH** - Important security issues
- **MEDIUM** - Moderate security concerns
- **LOW** - Minor issues or best practice violations
- **INFO** - Informational findings

### 2. HTML Report

A beautiful, detailed HTML report saved as `report_<hostname>_<timestamp>.html`

Features:
- Executive summary with severity breakdown
- Detailed findings organized by severity
- Color-coded issues
- Recommendations and references
- Professional formatting

### 3. JSON Report

Machine-readable JSON format saved as `report_<hostname>_<timestamp>.json`

Perfect for:
- Integration with other tools
- Automated processing
- Custom analysis
- CI/CD pipelines

## Example Output

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              WebSecAudit - Security Scanner v1.0             ║
║          Comprehensive Website Vulnerability Scanner         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

Target: https://example.com
Scan Started: 2025-01-15 10:30:45

[*] Initializing security scanners...

[+] Running TechFingerprint...
    ✓ TechFingerprint completed - Found 1 issues

[+] Running SSLScanner...
    ✓ SSLScanner completed - Found 2 issues

[+] Running HeadersScanner...
    ✓ HeadersScanner completed - Found 5 issues

... (more scanners) ...

======================================================================
                      SCAN SUMMARY
======================================================================

Target URL:      https://example.com
Scan Duration:   12.45 seconds
Total Issues:    15

Issues by Severity:
  ● CRITICAL  : 1
  ● HIGH      : 3
  ● MEDIUM    : 6
  ● LOW       : 4
  ● INFO      : 1

[✓] HTML Report saved: report_example.com_20250115_103057.html
[✓] JSON Report saved: report_example.com_20250115_103057.json
```

## Security Best Practices

### Ethical Use

**IMPORTANT**: Only scan websites you own or have explicit permission to test!

Unauthorized security scanning may be illegal and could be considered:
- Hacking attempts
- Network intrusion
- Violation of computer fraud laws

### Responsible Disclosure

If you find vulnerabilities:
1. Report them to the website owner privately
2. Give them reasonable time to fix issues
3. Don't publicly disclose until patched
4. Follow responsible disclosure practices

## Architecture

WebSecAudit uses a modular architecture:

```
websec-audit/
├── scanner.py              # Main orchestrator
├── modules/                # Security scanner modules
│   ├── ssl_scanner.py     # SSL/TLS checks
│   ├── headers_scanner.py # HTTP headers
│   ├── xss_scanner.py     # XSS detection
│   ├── injection_scanner.py # SQL injection
│   ├── auth_scanner.py    # Authentication
│   ├── cors_scanner.py    # CORS/CSRF
│   ├── info_disclosure.py # Information leaks
│   └── tech_fingerprint.py # Technology detection
├── utils/                  # Utility modules
│   ├── reporter.py        # Report generation
│   └── colors.py          # Terminal colors
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Extending the Tool

You can easily add new scanners:

1. Create a new scanner in `modules/`
2. Inherit from `BaseScanner`
3. Implement the `scan()` method
4. Add it to the scanner list in `scanner.py`

Example:

```python
from modules.base_scanner import BaseScanner

class MyScanner(BaseScanner):
    def scan(self):
        # Your scanning logic
        self.add_finding(
            title='Issue Title',
            severity='HIGH',
            category='My Category',
            description='Issue description',
            recommendation='How to fix it'
        )
        return self.findings
```

## Limitations

- This tool performs automated testing and may not catch all vulnerabilities
- False positives are possible - verify findings manually
- Some tests are basic and don't replace manual security audits
- Rate limiting may affect scan completeness
- Does not test authenticated areas without credentials
- Cannot detect all business logic vulnerabilities

## Contributing

Contributions are welcome! Areas for improvement:

- Additional scanner modules
- Enhanced detection capabilities
- Performance optimizations
- Better reporting formats
- Multi-threading support
- Authentication support
- API testing capabilities

## License

This tool is provided for educational and authorized security testing purposes only.

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)

## Support

For issues, questions, or contributions, please refer to the project repository.

---

**Remember**: With great power comes great responsibility. Use this tool ethically!
