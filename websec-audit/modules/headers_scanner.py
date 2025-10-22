"""HTTP Security Headers Scanner"""

import requests
from typing import List, Dict, Any
from modules.base_scanner import BaseScanner


class HeadersScanner(BaseScanner):
    """Scanner for HTTP security headers"""

    # Security headers that should be present
    SECURITY_HEADERS = {
        'Strict-Transport-Security': {
            'severity': 'HIGH',
            'description': 'HTTP Strict Transport Security (HSTS) is not set.',
            'recommendation': 'Add Strict-Transport-Security header: max-age=31536000; includeSubDomains; preload',
            'references': ['https://owasp.org/www-project-secure-headers/#http-strict-transport-security']
        },
        'X-Frame-Options': {
            'severity': 'MEDIUM',
            'description': 'X-Frame-Options header is missing.',
            'recommendation': 'Add X-Frame-Options header: DENY or SAMEORIGIN to prevent clickjacking.',
            'references': ['https://owasp.org/www-project-secure-headers/#x-frame-options']
        },
        'X-Content-Type-Options': {
            'severity': 'MEDIUM',
            'description': 'X-Content-Type-Options header is missing.',
            'recommendation': 'Add X-Content-Type-Options: nosniff to prevent MIME type sniffing.',
            'references': ['https://owasp.org/www-project-secure-headers/#x-content-type-options']
        },
        'Content-Security-Policy': {
            'severity': 'HIGH',
            'description': 'Content-Security-Policy (CSP) header is missing.',
            'recommendation': 'Implement a Content-Security-Policy to prevent XSS and injection attacks.',
            'references': ['https://owasp.org/www-project-secure-headers/#content-security-policy']
        },
        'X-XSS-Protection': {
            'severity': 'LOW',
            'description': 'X-XSS-Protection header is missing.',
            'recommendation': 'Add X-XSS-Protection: 1; mode=block (Note: CSP is preferred).',
            'references': ['https://owasp.org/www-project-secure-headers/#x-xss-protection']
        },
        'Referrer-Policy': {
            'severity': 'LOW',
            'description': 'Referrer-Policy header is missing.',
            'recommendation': 'Add Referrer-Policy header: no-referrer or strict-origin-when-cross-origin',
            'references': ['https://owasp.org/www-project-secure-headers/#referrer-policy']
        },
        'Permissions-Policy': {
            'severity': 'LOW',
            'description': 'Permissions-Policy header is missing.',
            'recommendation': 'Add Permissions-Policy to control browser features and APIs.',
            'references': ['https://owasp.org/www-project-secure-headers/#permissions-policy']
        }
    }

    # Headers that should NOT be present (information disclosure)
    DANGEROUS_HEADERS = {
        'Server': 'Server version information disclosed',
        'X-Powered-By': 'Technology stack information disclosed',
        'X-AspNet-Version': 'ASP.NET version information disclosed',
        'X-AspNetMvc-Version': 'ASP.NET MVC version information disclosed'
    }

    def scan(self) -> List[Dict[str, Any]]:
        """Scan HTTP security headers"""
        try:
            self.log(f"Fetching headers from {self.target_url}")

            # Make request with timeout
            response = requests.get(
                self.target_url,
                timeout=15,
                allow_redirects=True,
                verify=True,
                headers={'User-Agent': 'WebSecAudit/1.0 Security Scanner'}
            )

            headers = response.headers
            self.log(f"Received {len(headers)} headers")

            # Check for missing security headers
            self._check_missing_security_headers(headers)

            # Check for insecure header values
            self._check_insecure_header_values(headers)

            # Check for information disclosure headers
            self._check_information_disclosure(headers)

            # Check cookie security
            self._check_cookie_security(response)

        except requests.exceptions.SSLError as e:
            self.add_finding(
                title='SSL Certificate Error',
                severity='HIGH',
                category='HTTP Headers',
                description='SSL certificate validation failed.',
                evidence=str(e),
                recommendation='Ensure a valid SSL certificate is properly configured.'
            )
        except requests.exceptions.Timeout:
            self.add_finding(
                title='Connection Timeout',
                severity='MEDIUM',
                category='HTTP Headers',
                description='Connection to the server timed out.',
                recommendation='Verify that the server is accessible and responsive.'
            )
        except requests.exceptions.RequestException as e:
            self.log(f"Request error: {str(e)}")
            self.add_finding(
                title='Connection Error',
                severity='MEDIUM',
                category='HTTP Headers',
                description='Unable to connect to the server.',
                evidence=str(e),
                recommendation='Verify that the URL is correct and the server is accessible.'
            )

        return self.findings

    def _check_missing_security_headers(self, headers: Dict):
        """Check for missing security headers"""
        for header_name, header_info in self.SECURITY_HEADERS.items():
            if header_name not in headers:
                self.add_finding(
                    title=f'Missing Security Header: {header_name}',
                    severity=header_info['severity'],
                    category='HTTP Headers',
                    description=header_info['description'],
                    recommendation=header_info['recommendation'],
                    references=header_info['references']
                )

    def _check_insecure_header_values(self, headers: Dict):
        """Check for insecure values in existing headers"""

        # Check HSTS header value
        if 'Strict-Transport-Security' in headers:
            hsts_value = headers['Strict-Transport-Security']
            if 'max-age' in hsts_value:
                try:
                    # Extract max-age value
                    for part in hsts_value.split(';'):
                        if 'max-age' in part:
                            max_age = int(part.split('=')[1].strip())
                            if max_age < 31536000:  # Less than 1 year
                                self.add_finding(
                                    title='Weak HSTS max-age Value',
                                    severity='MEDIUM',
                                    category='HTTP Headers',
                                    description=f'HSTS max-age is set to {max_age} seconds, which is less than recommended.',
                                    evidence=f'Strict-Transport-Security: {hsts_value}',
                                    recommendation='Set HSTS max-age to at least 31536000 (1 year).'
                                )
                except:
                    pass

        # Check X-Frame-Options
        if 'X-Frame-Options' in headers:
            xfo_value = headers['X-Frame-Options'].upper()
            if xfo_value == 'ALLOW-FROM':
                self.add_finding(
                    title='Deprecated X-Frame-Options Value',
                    severity='LOW',
                    category='HTTP Headers',
                    description='X-Frame-Options ALLOW-FROM is deprecated.',
                    evidence=f'X-Frame-Options: {headers["X-Frame-Options"]}',
                    recommendation='Use Content-Security-Policy frame-ancestors directive instead.'
                )

        # Check CSP
        if 'Content-Security-Policy' in headers:
            csp_value = headers['Content-Security-Policy'].lower()

            if 'unsafe-inline' in csp_value:
                self.add_finding(
                    title='Weak CSP: unsafe-inline Detected',
                    severity='MEDIUM',
                    category='HTTP Headers',
                    description="CSP contains 'unsafe-inline' which weakens XSS protection.",
                    evidence='unsafe-inline directive found in CSP',
                    recommendation="Remove 'unsafe-inline' and use nonces or hashes for inline scripts."
                )

            if 'unsafe-eval' in csp_value:
                self.add_finding(
                    title='Weak CSP: unsafe-eval Detected',
                    severity='MEDIUM',
                    category='HTTP Headers',
                    description="CSP contains 'unsafe-eval' which weakens XSS protection.",
                    evidence='unsafe-eval directive found in CSP',
                    recommendation="Remove 'unsafe-eval' to prevent code injection via eval()."
                )

    def _check_information_disclosure(self, headers: Dict):
        """Check for headers that disclose sensitive information"""
        for header_name, description in self.DANGEROUS_HEADERS.items():
            if header_name in headers:
                self.add_finding(
                    title=f'Information Disclosure: {header_name}',
                    severity='LOW',
                    category='HTTP Headers',
                    description=description,
                    evidence=f'{header_name}: {headers[header_name]}',
                    recommendation=f'Remove or obfuscate the {header_name} header to avoid disclosing version information.',
                    references=['https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/02-Fingerprint_Web_Server']
                )

    def _check_cookie_security(self, response):
        """Check cookie security attributes"""
        if 'Set-Cookie' in response.headers:
            cookies = response.headers.get('Set-Cookie', '')
            cookie_headers = response.raw.headers.getlist('Set-Cookie') if hasattr(response.raw.headers, 'getlist') else [cookies]

            for cookie in cookie_headers:
                cookie_lower = cookie.lower()

                # Check for HttpOnly flag
                if 'httponly' not in cookie_lower:
                    self.add_finding(
                        title='Cookie Missing HttpOnly Flag',
                        severity='MEDIUM',
                        category='HTTP Headers',
                        description='Cookie is set without the HttpOnly flag.',
                        evidence=cookie[:100] + ('...' if len(cookie) > 100 else ''),
                        recommendation='Set the HttpOnly flag on cookies to prevent XSS attacks from accessing them.',
                        references=['https://owasp.org/www-community/HttpOnly']
                    )

                # Check for Secure flag on HTTPS sites
                if self.target_url.startswith('https://') and 'secure' not in cookie_lower:
                    self.add_finding(
                        title='Cookie Missing Secure Flag',
                        severity='MEDIUM',
                        category='HTTP Headers',
                        description='Cookie is set without the Secure flag on an HTTPS site.',
                        evidence=cookie[:100] + ('...' if len(cookie) > 100 else ''),
                        recommendation='Set the Secure flag on cookies to ensure they are only sent over HTTPS.',
                        references=['https://owasp.org/www-community/controls/SecureCookieAttribute']
                    )

                # Check for SameSite attribute
                if 'samesite' not in cookie_lower:
                    self.add_finding(
                        title='Cookie Missing SameSite Attribute',
                        severity='MEDIUM',
                        category='HTTP Headers',
                        description='Cookie is set without the SameSite attribute.',
                        evidence=cookie[:100] + ('...' if len(cookie) > 100 else ''),
                        recommendation='Set the SameSite attribute (Strict or Lax) to prevent CSRF attacks.',
                        references=['https://owasp.org/www-community/SameSite']
                    )
