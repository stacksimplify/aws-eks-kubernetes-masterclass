"""Authentication and Session Security Scanner"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from modules.base_scanner import BaseScanner


class AuthScanner(BaseScanner):
    """Scanner for authentication and session security issues"""

    def scan(self) -> List[Dict[str, Any]]:
        """Scan for authentication and session security issues"""
        try:
            self.log(f"Scanning authentication and session security at {self.target_url}")

            # Get the page
            response = requests.get(
                self.target_url,
                timeout=15,
                headers={'User-Agent': 'WebSecAudit/1.0 Security Scanner'}
            )

            soup = BeautifulSoup(response.text, 'html.parser')

            # Check for login forms
            self._check_login_forms(soup, response)

            # Check password reset functionality
            self._check_password_fields(soup)

            # Check for session token exposure
            self._check_session_exposure(soup, response)

            # Check authentication over HTTP
            if self.target_url.startswith('http://'):
                self._check_http_authentication(soup)

        except requests.exceptions.RequestException as e:
            self.log(f"Request error during auth scan: {str(e)}")

        return self.findings

    def _check_login_forms(self, soup: BeautifulSoup, response):
        """Check login forms for security issues"""
        forms = soup.find_all('form')

        for form in forms:
            # Check if it's a login form
            password_inputs = form.find_all('input', {'type': 'password'})

            if password_inputs:
                self.log("Found login form")

                # Check if form action is HTTPS
                action = form.get('action', '')
                if action and action.startswith('http://'):
                    self.add_finding(
                        title='Login Form Submits Over HTTP',
                        severity='CRITICAL',
                        category='Authentication',
                        description='Login form submits credentials over unencrypted HTTP connection.',
                        evidence=f'Form action: {action}',
                        recommendation='Use HTTPS for all authentication forms to protect credentials in transit.',
                        references=['https://owasp.org/www-community/vulnerabilities/Unencrypted_sensitive_data']
                    )

                # Check for autocomplete on password fields
                for pwd_input in password_inputs:
                    autocomplete = pwd_input.get('autocomplete', '').lower()
                    if autocomplete not in ['off', 'new-password', 'current-password']:
                        self.add_finding(
                            title='Password Field Allows Autocomplete',
                            severity='LOW',
                            category='Authentication',
                            description='Password field does not disable autocomplete.',
                            recommendation='Set autocomplete="off" or use appropriate autocomplete values for password fields.',
                            references=['https://owasp.org/www-community/vulnerabilities/Sensitive_Data_Exposure']
                        )
                        break

    def _check_password_fields(self, soup: BeautifulSoup):
        """Check password field implementations"""
        password_inputs = soup.find_all('input', {'type': 'password'})

        for pwd_input in password_inputs:
            # Check for password fields in non-HTTPS pages
            if self.target_url.startswith('http://'):
                self.add_finding(
                    title='Password Field on Non-HTTPS Page',
                    severity='CRITICAL',
                    category='Authentication',
                    description='Password input field found on a non-HTTPS page.',
                    recommendation='All pages with password fields must be served over HTTPS.',
                    references=['https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/09-Testing_for_Weak_Cryptography/03-Testing_for_Sensitive_Information_Sent_via_Unencrypted_Channels']
                )
                break

            # Check for visible password options
            parent_form = pwd_input.find_parent('form')
            if parent_form:
                # Look for show/hide password functionality
                show_password = parent_form.find_all(text=lambda text: text and 'show' in text.lower())
                if show_password:
                    self.log("Password visibility toggle found")

    def _check_session_exposure(self, soup: BeautifulSoup, response):
        """Check for session token exposure in URLs or JavaScript"""
        # Check for session tokens in URLs
        links = soup.find_all('a', href=True)

        session_keywords = ['sessionid', 'session_id', 'sid', 'token', 'auth', 'jsessionid']

        for link in links:
            href = link['href'].lower()
            for keyword in session_keywords:
                if keyword in href:
                    self.add_finding(
                        title='Potential Session Token in URL',
                        severity='HIGH',
                        category='Authentication',
                        description='Session token or authentication credential appears to be passed in URL.',
                        evidence=f'Link contains "{keyword}" parameter',
                        recommendation='Use HTTP-only cookies for session management. Never pass session tokens in URLs.',
                        references=[
                            'https://owasp.org/www-community/vulnerabilities/Session_ID_in_URL_Rewriting',
                            'https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html'
                        ]
                    )
                    break

        # Check for session tokens in JavaScript
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                script_lower = script.string.lower()
                for keyword in session_keywords:
                    if keyword in script_lower:
                        self.add_finding(
                            title='Potential Session Token in JavaScript',
                            severity='MEDIUM',
                            category='Authentication',
                            description='Possible session token or credential found in JavaScript code.',
                            evidence=f'JavaScript contains "{keyword}"',
                            recommendation='Avoid exposing session tokens in client-side code. Use HTTP-only cookies.',
                            references=['https://owasp.org/www-community/vulnerabilities/Session_fixation']
                        )
                        break

    def _check_http_authentication(self, soup: BeautifulSoup):
        """Check for authentication forms on HTTP pages"""
        forms = soup.find_all('form')

        for form in forms:
            inputs = form.find_all('input')

            # Check for authentication-related forms
            auth_indicators = ['password', 'username', 'email', 'login']

            for input_field in inputs:
                input_type = input_field.get('type', '').lower()
                input_name = input_field.get('name', '').lower()

                if input_type in auth_indicators or any(indicator in input_name for indicator in auth_indicators):
                    self.add_finding(
                        title='Authentication Form on HTTP Page',
                        severity='CRITICAL',
                        category='Authentication',
                        description='Authentication form found on unencrypted HTTP page.',
                        recommendation='Serve all authentication pages over HTTPS only.',
                        references=['https://owasp.org/www-community/vulnerabilities/Unencrypted_sensitive_data']
                    )
                    return
