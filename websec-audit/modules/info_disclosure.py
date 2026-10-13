"""Information Disclosure Scanner"""

import requests
from bs4 import BeautifulSoup, Comment
from typing import List, Dict, Any
from modules.base_scanner import BaseScanner


class InfoDisclosureScanner(BaseScanner):
    """Scanner for information disclosure vulnerabilities"""

    # Common sensitive file paths to check
    SENSITIVE_FILES = [
        '/.git/HEAD',
        '/.git/config',
        '/.env',
        '/.env.local',
        '/.env.production',
        '/web.config',
        '/Web.config',
        '/.htaccess',
        '/phpinfo.php',
        '/info.php',
        '/test.php',
        '/README.md',
        '/readme.md',
        '/CHANGELOG.md',
        '/composer.json',
        '/package.json',
        '/.DS_Store',
        '/backup.zip',
        '/backup.sql',
        '/dump.sql',
        '/.svn/entries',
        '/crossdomain.xml',
        '/robots.txt',
        '/sitemap.xml',
    ]

    # Sensitive keywords to look for in comments
    SENSITIVE_KEYWORDS = [
        'password', 'passwd', 'pwd', 'secret', 'token', 'api_key', 'apikey',
        'private_key', 'access_key', 'secret_key', 'admin', 'root',
        'todo', 'fixme', 'hack', 'bug', 'debug'
    ]

    def scan(self) -> List[Dict[str, Any]]:
        """Scan for information disclosure issues"""
        try:
            self.log(f"Scanning for information disclosure at {self.target_url}")

            # Get the main page
            response = requests.get(
                self.target_url,
                timeout=15,
                headers={'User-Agent': 'WebSecAudit/1.0 Security Scanner'}
            )

            soup = BeautifulSoup(response.text, 'html.parser')

            # Check HTML comments
            self._check_html_comments(soup)

            # Check for exposed sensitive files
            self._check_sensitive_files()

            # Check for directory listing
            self._check_directory_listing(response)

            # Check for error messages
            self._check_error_messages(soup)

            # Check for exposed admin panels
            self._check_admin_panels()

        except requests.exceptions.RequestException as e:
            self.log(f"Request error during info disclosure scan: {str(e)}")

        return self.findings

    def _check_html_comments(self, soup: BeautifulSoup):
        """Check HTML comments for sensitive information"""
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))

        for comment in comments:
            comment_lower = comment.lower()

            # Check for sensitive keywords
            for keyword in self.SENSITIVE_KEYWORDS:
                if keyword in comment_lower:
                    # Truncate long comments
                    preview = comment[:100].strip() + ('...' if len(comment) > 100 else '')

                    self.add_finding(
                        title='Sensitive Information in HTML Comments',
                        severity='LOW',
                        category='Information Disclosure',
                        description=f'HTML comment contains potentially sensitive keyword: "{keyword}"',
                        evidence=f'Comment preview: {preview}',
                        recommendation='Remove sensitive information and developer comments from production code.',
                        references=['https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/05-Review_Webpage_Content_for_Information_Leakage']
                    )
                    break  # Only report once per comment

    def _check_sensitive_files(self):
        """Check for exposed sensitive files"""
        base_url = self.target_url.rstrip('/')

        found_files = []

        for file_path in self.SENSITIVE_FILES:
            try:
                url = base_url + file_path
                response = requests.get(
                    url,
                    timeout=5,
                    headers={'User-Agent': 'WebSecAudit/1.0 Security Scanner'},
                    allow_redirects=False
                )

                # Consider it found if status is 200
                if response.status_code == 200:
                    # Check if it's not a 404 page disguised as 200
                    if len(response.content) > 0 and '404' not in response.text.lower()[:200]:
                        found_files.append(file_path)
                        self.log(f"Found exposed file: {file_path}")

            except requests.exceptions.RequestException:
                # File doesn't exist or connection error
                continue

        if found_files:
            severity = 'CRITICAL' if any(f in found_files for f in ['/.git/HEAD', '/.env', '/web.config']) else 'HIGH'

            self.add_finding(
                title='Sensitive Files Exposed',
                severity=severity,
                category='Information Disclosure',
                description='Sensitive files are publicly accessible.',
                evidence=f'Exposed files: {", ".join(found_files)}',
                recommendation='Remove or restrict access to sensitive files. Use proper access controls.',
                references=['https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/03-Test_File_Extensions_Handling_for_Sensitive_Information']
            )

    def _check_directory_listing(self, response):
        """Check for directory listing vulnerability"""
        # Common indicators of directory listing
        listing_indicators = [
            'Index of /',
            'Directory Listing',
            'Parent Directory',
            '<title>Index of',
        ]

        response_text = response.text

        for indicator in listing_indicators:
            if indicator in response_text:
                self.add_finding(
                    title='Directory Listing Enabled',
                    severity='MEDIUM',
                    category='Information Disclosure',
                    description='Server has directory listing enabled.',
                    evidence=f'Indicator found: {indicator}',
                    recommendation='Disable directory listing in web server configuration.',
                    references=['https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/04-Review_Old_Backup_and_Unreferenced_Files_for_Sensitive_Information']
                )
                break

    def _check_error_messages(self, soup: BeautifulSoup):
        """Check for detailed error messages"""
        # Look for common error patterns
        error_patterns = [
            'stack trace',
            'exception',
            'fatal error',
            'mysql error',
            'postgresql error',
            'oracle error',
            'warning:',
            'traceback',
            'at line',
        ]

        page_text = soup.get_text().lower()

        for pattern in error_patterns:
            if pattern in page_text:
                self.add_finding(
                    title='Detailed Error Messages Exposed',
                    severity='MEDIUM',
                    category='Information Disclosure',
                    description='Application exposes detailed error messages.',
                    evidence=f'Error pattern detected: {pattern}',
                    recommendation='Configure application to show generic error messages to users. Log detailed errors server-side.',
                    references=['https://owasp.org/www-community/Improper_Error_Handling']
                )
                break

    def _check_admin_panels(self):
        """Check for exposed admin panels"""
        base_url = self.target_url.rstrip('/')

        admin_paths = [
            '/admin',
            '/administrator',
            '/admin.php',
            '/admin/',
            '/wp-admin',
            '/phpmyadmin',
            '/cpanel',
            '/admin/login',
            '/administrator/login',
        ]

        found_admin = []

        for path in admin_paths:
            try:
                url = base_url + path
                response = requests.get(
                    url,
                    timeout=5,
                    headers={'User-Agent': 'WebSecAudit/1.0 Security Scanner'},
                    allow_redirects=True
                )

                # Check if we got a login page or admin interface
                if response.status_code == 200:
                    response_lower = response.text.lower()
                    if any(keyword in response_lower for keyword in ['login', 'admin', 'dashboard', 'username', 'password']):
                        found_admin.append(path)
                        self.log(f"Found admin panel: {path}")

            except requests.exceptions.RequestException:
                continue

        if found_admin:
            self.add_finding(
                title='Admin Panel Publicly Accessible',
                severity='MEDIUM',
                category='Information Disclosure',
                description='Admin panel or login page is publicly accessible.',
                evidence=f'Admin paths found: {", ".join(found_admin)}',
                recommendation='Implement IP whitelisting, VPN access, or other access controls for admin panels. Use strong authentication and rate limiting.',
                references=['https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/']
            )
