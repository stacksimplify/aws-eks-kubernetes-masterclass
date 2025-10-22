"""CORS and CSRF Security Scanner"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from modules.base_scanner import BaseScanner


class CORSScanner(BaseScanner):
    """Scanner for CORS and CSRF vulnerabilities"""

    def scan(self) -> List[Dict[str, Any]]:
        """Scan for CORS and CSRF issues"""
        try:
            self.log(f"Scanning for CORS/CSRF issues at {self.target_url}")

            # Check CORS configuration
            self._check_cors_configuration()

            # Check for CSRF protection
            response = requests.get(
                self.target_url,
                timeout=15,
                headers={'User-Agent': 'WebSecAudit/1.0 Security Scanner'}
            )

            soup = BeautifulSoup(response.text, 'html.parser')
            self._check_csrf_protection(soup)

        except requests.exceptions.RequestException as e:
            self.log(f"Request error during CORS/CSRF scan: {str(e)}")

        return self.findings

    def _check_cors_configuration(self):
        """Check CORS configuration"""
        try:
            # Test with a malicious origin
            test_origin = 'https://evil.com'

            response = requests.get(
                self.target_url,
                timeout=10,
                headers={
                    'User-Agent': 'WebSecAudit/1.0 Security Scanner',
                    'Origin': test_origin
                }
            )

            # Check CORS headers
            acao = response.headers.get('Access-Control-Allow-Origin')
            acac = response.headers.get('Access-Control-Allow-Credentials')

            if acao:
                self.log(f"CORS enabled: {acao}")

                # Check for wildcard with credentials
                if acao == '*':
                    if acac and acac.lower() == 'true':
                        self.add_finding(
                            title='CORS Misconfiguration: Wildcard with Credentials',
                            severity='CRITICAL',
                            category='CORS',
                            description='CORS allows all origins (*) with credentials enabled.',
                            evidence=f'Access-Control-Allow-Origin: *, Access-Control-Allow-Credentials: true',
                            recommendation='Never use wildcard (*) origin with credentials. Specify exact origins.',
                            references=[
                                'https://owasp.org/www-community/attacks/CORS_OriginHeaderScrutiny',
                                'https://portswigger.net/web-security/cors'
                            ]
                        )
                    else:
                        self.add_finding(
                            title='CORS Allows All Origins',
                            severity='MEDIUM',
                            category='CORS',
                            description='CORS policy allows requests from any origin (*).',
                            evidence='Access-Control-Allow-Origin: *',
                            recommendation='Restrict CORS to specific trusted origins instead of using wildcard.',
                            references=['https://owasp.org/www-community/attacks/CORS_OriginHeaderScrutiny']
                        )

                # Check if it reflects our malicious origin
                elif acao == test_origin:
                    self.add_finding(
                        title='CORS Reflects Arbitrary Origins',
                        severity='HIGH',
                        category='CORS',
                        description='CORS policy reflects the Origin header without validation.',
                        evidence=f'Origin header: {test_origin}, Reflected: {acao}',
                        recommendation='Validate Origin header against a whitelist of trusted domains.',
                        references=['https://owasp.org/www-community/attacks/CORS_OriginHeaderScrutiny']
                    )

                # Check for null origin
                response_null = requests.get(
                    self.target_url,
                    timeout=10,
                    headers={
                        'User-Agent': 'WebSecAudit/1.0 Security Scanner',
                        'Origin': 'null'
                    }
                )

                acao_null = response_null.headers.get('Access-Control-Allow-Origin')
                if acao_null == 'null':
                    self.add_finding(
                        title='CORS Allows Null Origin',
                        severity='HIGH',
                        category='CORS',
                        description='CORS policy allows the null origin.',
                        evidence='Access-Control-Allow-Origin: null',
                        recommendation='Never allow null origin. Validate against specific trusted domains.',
                        references=['https://portswigger.net/web-security/cors']
                    )

        except requests.exceptions.RequestException as e:
            self.log(f"Error checking CORS: {str(e)}")

    def _check_csrf_protection(self, soup: BeautifulSoup):
        """Check for CSRF protection mechanisms"""
        forms = soup.find_all('form')

        if not forms:
            return

        self.log(f"Checking {len(forms)} forms for CSRF protection")

        for idx, form in enumerate(forms[:10]):  # Check up to 10 forms
            method = form.get('method', 'get').lower()

            # CSRF is primarily a concern for state-changing requests (POST, PUT, DELETE)
            if method not in ['post', 'put', 'delete']:
                continue

            # Look for CSRF token fields
            csrf_token_found = False
            inputs = form.find_all('input', {'type': 'hidden'})

            csrf_keywords = [
                'csrf', 'token', 'authenticity_token', 'xsrf',
                '_token', 'csrftoken', 'csrf_token', '__requestverificationtoken'
            ]

            for input_field in inputs:
                input_name = input_field.get('name', '').lower()
                if any(keyword in input_name for keyword in csrf_keywords):
                    csrf_token_found = True
                    self.log(f"CSRF token found in form #{idx + 1}")
                    break

            if not csrf_token_found:
                # Get form identifier
                form_id = form.get('id', '')
                form_action = form.get('action', '')
                form_identifier = f"ID: {form_id}" if form_id else f"Action: {form_action}" if form_action else f"Form #{idx + 1}"

                self.add_finding(
                    title=f'Missing CSRF Protection in Form',
                    severity='HIGH',
                    category='CSRF',
                    description=f'Form ({form_identifier}) does not appear to have CSRF protection.',
                    evidence=f'POST form without visible CSRF token field',
                    recommendation='Implement CSRF tokens for all state-changing operations. Use framework-provided CSRF protection.',
                    references=[
                        'https://owasp.org/www-community/attacks/csrf',
                        'https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html'
                    ]
                )
