"""SQL Injection and Other Injection Vulnerability Scanner"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from typing import List, Dict, Any
from modules.base_scanner import BaseScanner


class InjectionScanner(BaseScanner):
    """Scanner for SQL Injection and other injection vulnerabilities"""

    # SQL injection test payloads
    SQL_PAYLOADS = [
        "'",
        "' OR '1'='1",
        "' OR '1'='1' --",
        "' OR '1'='1' /*",
        "admin' --",
        "1' OR '1' = '1",
        "' UNION SELECT NULL--",
    ]

    # SQL error patterns
    SQL_ERROR_PATTERNS = [
        'sql syntax',
        'mysql_fetch',
        'mysql_num_rows',
        'ora-01',
        'postgresql',
        'pg_query',
        'sqlite_',
        'unclosed quotation mark',
        'quoted string not properly terminated',
        'microsoft sql server',
        'odbc sql server driver',
        'microsoft ole db provider',
    ]

    # Command injection payloads
    COMMAND_PAYLOADS = [
        '; ls',
        '| ls',
        '& dir',
        '; cat /etc/passwd',
        '`whoami`',
        '$(whoami)',
    ]

    def scan(self) -> List[Dict[str, Any]]:
        """Scan for injection vulnerabilities"""
        try:
            self.log(f"Scanning for injection vulnerabilities at {self.target_url}")

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
            self.log(f"Found {len(forms)} forms to test for injection")

            # Test each form
            for idx, form in enumerate(forms[:5]):  # Limit to 5 forms
                self._test_sql_injection(form, idx + 1)

            # Check URL parameters for SQL injection
            self._check_url_sql_injection()

        except requests.exceptions.RequestException as e:
            self.log(f"Request error during injection scan: {str(e)}")

        return self.findings

    def _test_sql_injection(self, form, form_number: int):
        """Test a form for SQL injection vulnerabilities"""
        try:
            # Get form action and method
            action = form.get('action', '')
            method = form.get('method', 'get').lower()
            form_url = urljoin(self.target_url, action)

            self.log(f"Testing form #{form_number} for SQL injection")

            # Get all input fields
            inputs = form.find_all(['input', 'textarea'])

            if not inputs:
                return

            # Test with SQL payloads
            for payload in self.SQL_PAYLOADS[:3]:  # Test with first 3 payloads
                form_data = {}

                for input_field in inputs:
                    input_name = input_field.get('name')
                    input_type = input_field.get('type', 'text')

                    if input_name and input_type not in ['submit', 'button']:
                        # Use payload for text inputs, normal values for others
                        if input_type in ['text', 'email', 'search', 'url'] or input_field.name == 'textarea':
                            form_data[input_name] = payload
                        elif input_type == 'hidden':
                            form_data[input_name] = input_field.get('value', '')
                        else:
                            form_data[input_name] = 'test'

                if not form_data:
                    continue

                try:
                    # Send request
                    if method == 'post':
                        response = requests.post(form_url, data=form_data, timeout=10,
                                                headers={'User-Agent': 'WebSecAudit/1.0 Security Scanner'})
                    else:
                        response = requests.get(form_url, params=form_data, timeout=10,
                                               headers={'User-Agent': 'WebSecAudit/1.0 Security Scanner'})

                    response_text = response.text.lower()

                    # Check for SQL error messages
                    for error_pattern in self.SQL_ERROR_PATTERNS:
                        if error_pattern in response_text:
                            self.add_finding(
                                title=f'Potential SQL Injection in Form #{form_number}',
                                severity='CRITICAL',
                                category='SQL Injection',
                                description='SQL error message detected in response, indicating possible SQL injection vulnerability.',
                                evidence=f'Form: {form_url}, Method: {method.upper()}, Error pattern: {error_pattern}, Payload: {payload}',
                                recommendation='Use parameterized queries (prepared statements) to prevent SQL injection. Never concatenate user input into SQL queries.',
                                references=[
                                    'https://owasp.org/www-community/attacks/SQL_Injection',
                                    'https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html'
                                ]
                            )
                            self.log(f"SQL error detected in form #{form_number}")
                            return  # Found vulnerability, no need to test more

                    # Check for unusual response (timing-based detection could be added here)
                    # This is a simplified check
                    if response.status_code == 500:
                        self.add_finding(
                            title=f'Server Error on SQL Payload in Form #{form_number}',
                            severity='HIGH',
                            category='SQL Injection',
                            description='Server returned 500 error when SQL payload was submitted.',
                            evidence=f'Form: {form_url}, Method: {method.upper()}, Payload: {payload}',
                            recommendation='Investigate server-side error handling and implement proper input validation.',
                            references=['https://owasp.org/www-community/attacks/SQL_Injection']
                        )
                        return

                except requests.exceptions.RequestException as e:
                    self.log(f"Error testing SQL injection in form #{form_number}: {str(e)}")
                    continue

        except Exception as e:
            self.log(f"Error processing form #{form_number} for SQL injection: {str(e)}")

    def _check_url_sql_injection(self):
        """Check URL parameters for SQL injection"""
        parsed_url = urlparse(self.target_url)
        params = parse_qs(parsed_url.query)

        if not params:
            return

        self.log("Checking URL parameters for SQL injection")

        # Test each parameter
        for param_name, param_values in params.items():
            for payload in self.SQL_PAYLOADS[:2]:  # Test with first 2 payloads
                test_params = params.copy()
                test_params[param_name] = [payload]

                # Build test URL
                test_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

                try:
                    response = requests.get(test_url, params=test_params, timeout=10,
                                           headers={'User-Agent': 'WebSecAudit/1.0 Security Scanner'})

                    response_text = response.text.lower()

                    # Check for SQL errors
                    for error_pattern in self.SQL_ERROR_PATTERNS:
                        if error_pattern in response_text:
                            self.add_finding(
                                title=f'Potential SQL Injection in URL Parameter: {param_name}',
                                severity='CRITICAL',
                                category='SQL Injection',
                                description='SQL error message detected when testing URL parameter.',
                                evidence=f'Parameter: {param_name}, Payload: {payload}, Error: {error_pattern}',
                                recommendation='Use parameterized queries and proper input validation for all URL parameters.',
                                references=['https://owasp.org/www-community/attacks/SQL_Injection']
                            )
                            return

                except requests.exceptions.RequestException as e:
                    self.log(f"Error testing SQL injection in URL parameter {param_name}: {str(e)}")
                    continue
