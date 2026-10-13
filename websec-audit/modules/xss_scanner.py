"""Cross-Site Scripting (XSS) Scanner"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from typing import List, Dict, Any
from modules.base_scanner import BaseScanner


class XSSScanner(BaseScanner):
    """Scanner for XSS vulnerabilities"""

    # XSS test payloads (safe, non-harmful payloads for testing)
    XSS_PAYLOADS = [
        '<script>alert("XSS")</script>',
        '<img src=x onerror=alert("XSS")>',
        '"><script>alert("XSS")</script>',
        "'><script>alert('XSS')</script>",
        '<svg/onload=alert("XSS")>',
        'javascript:alert("XSS")',
        '<iframe src="javascript:alert(\'XSS\')">',
    ]

    def scan(self) -> List[Dict[str, Any]]:
        """Scan for XSS vulnerabilities"""
        try:
            self.log(f"Scanning for XSS vulnerabilities at {self.target_url}")

            # Get the page
            response = requests.get(
                self.target_url,
                timeout=15,
                headers={'User-Agent': 'WebSecAudit/1.0 Security Scanner'}
            )

            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all forms
            forms = soup.find_all('form')
            self.log(f"Found {len(forms)} forms to test")

            # Test each form for XSS
            for idx, form in enumerate(forms[:5]):  # Limit to 5 forms to avoid too many requests
                self._test_form_xss(form, idx + 1)

            # Check for reflected parameters in URL
            self._check_url_reflection(response)

            # Check for DOM-based XSS indicators
            self._check_dom_xss_indicators(soup)

        except requests.exceptions.RequestException as e:
            self.log(f"Request error during XSS scan: {str(e)}")

        return self.findings

    def _test_form_xss(self, form, form_number: int):
        """Test a form for XSS vulnerabilities"""
        try:
            # Get form action and method
            action = form.get('action', '')
            method = form.get('method', 'get').lower()
            form_url = urljoin(self.target_url, action)

            self.log(f"Testing form #{form_number}: {method.upper()} {form_url}")

            # Get all input fields
            inputs = form.find_all(['input', 'textarea'])

            if not inputs:
                return

            # Build form data with XSS payload
            form_data = {}
            test_payload = self.XSS_PAYLOADS[0]  # Use first payload for testing

            for input_field in inputs:
                input_name = input_field.get('name')
                input_type = input_field.get('type', 'text')

                if input_name and input_type not in ['submit', 'button', 'hidden']:
                    form_data[input_name] = test_payload

            if not form_data:
                return

            # Send request with payload
            try:
                if method == 'post':
                    response = requests.post(form_url, data=form_data, timeout=10,
                                            headers={'User-Agent': 'WebSecAudit/1.0 Security Scanner'})
                else:
                    response = requests.get(form_url, params=form_data, timeout=10,
                                           headers={'User-Agent': 'WebSecAudit/1.0 Security Scanner'})

                # Check if payload is reflected in response
                if test_payload in response.text:
                    self.add_finding(
                        title=f'Potential XSS Vulnerability in Form #{form_number}',
                        severity='HIGH',
                        category='Cross-Site Scripting',
                        description='User input is reflected in the response without proper sanitization.',
                        evidence=f'Form action: {form_url}, Method: {method.upper()}, Payload reflected in response',
                        recommendation='Implement proper input validation and output encoding. Use Content-Security-Policy headers.',
                        references=[
                            'https://owasp.org/www-community/attacks/xss/',
                            'https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html'
                        ]
                    )
                    self.log(f"XSS payload reflected in form #{form_number}")

            except requests.exceptions.RequestException as e:
                self.log(f"Error testing form #{form_number}: {str(e)}")

        except Exception as e:
            self.log(f"Error processing form #{form_number}: {str(e)}")

    def _check_url_reflection(self, response):
        """Check if URL parameters are reflected in the response"""
        parsed_url = urlparse(self.target_url)
        params = parse_qs(parsed_url.query)

        if not params:
            return

        self.log("Checking for URL parameter reflection")

        # Check each parameter
        for param_name, param_values in params.items():
            for param_value in param_values:
                if param_value and param_value in response.text:
                    # Check if it's reflected without encoding
                    if '<' in param_value or '>' in param_value or '"' in param_value:
                        self.add_finding(
                            title='URL Parameter Reflected Without Encoding',
                            severity='HIGH',
                            category='Cross-Site Scripting',
                            description=f'URL parameter "{param_name}" is reflected in the response without proper encoding.',
                            evidence=f'Parameter: {param_name}={param_value}',
                            recommendation='Implement proper output encoding for all reflected user input.',
                            references=['https://owasp.org/www-community/attacks/xss/']
                        )

    def _check_dom_xss_indicators(self, soup: BeautifulSoup):
        """Check for DOM-based XSS indicators"""
        # Check for dangerous JavaScript functions with user input
        scripts = soup.find_all('script')

        dangerous_patterns = [
            'document.write(',
            'innerHTML',
            'outerHTML',
            'document.location',
            'document.URL',
            'document.documentURI',
            'location.href',
            'eval(',
            'setTimeout(',
            'setInterval(',
        ]

        for script in scripts:
            if script.string:
                script_content = script.string

                for pattern in dangerous_patterns:
                    if pattern in script_content:
                        # Check if it's using user-controlled input
                        if any(source in script_content for source in
                               ['location', 'document.URL', 'document.referrer', 'window.name']):
                            self.add_finding(
                                title='Potential DOM-Based XSS',
                                severity='MEDIUM',
                                category='Cross-Site Scripting',
                                description=f'JavaScript code uses potentially dangerous function "{pattern}" with user-controllable input.',
                                evidence=f'Pattern detected: {pattern}',
                                recommendation='Avoid using dangerous JavaScript functions with user input. Use safe APIs and sanitize input.',
                                references=[
                                    'https://owasp.org/www-community/attacks/DOM_Based_XSS',
                                    'https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html'
                                ]
                            )
                            break  # Only report once per script
