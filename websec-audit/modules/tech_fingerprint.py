"""Technology Fingerprinting Scanner"""

import requests
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from modules.base_scanner import BaseScanner


class TechFingerprint(BaseScanner):
    """Scanner for technology stack fingerprinting"""

    # Technology signatures
    TECH_SIGNATURES = {
        'WordPress': {
            'patterns': ['/wp-content/', '/wp-includes/', 'wp-json'],
            'headers': {},
            'meta': ['generator']
        },
        'Drupal': {
            'patterns': ['/sites/default/', 'Drupal.settings', '/misc/drupal.js'],
            'headers': {'X-Generator': 'Drupal'},
            'meta': []
        },
        'Joomla': {
            'patterns': ['/components/com_', '/media/jui/', 'Joomla!'],
            'headers': {},
            'meta': ['generator']
        },
        'Django': {
            'patterns': ['csrfmiddlewaretoken'],
            'headers': {},
            'meta': []
        },
        'Laravel': {
            'patterns': ['laravel_session', '_token'],
            'headers': {},
            'meta': []
        },
        'React': {
            'patterns': ['react.js', 'react.min.js', 'react-dom'],
            'headers': {},
            'meta': []
        },
        'Angular': {
            'patterns': ['ng-version', 'angular.js', 'angular.min.js'],
            'headers': {},
            'meta': []
        },
        'Vue.js': {
            'patterns': ['vue.js', 'vue.min.js', 'data-v-'],
            'headers': {},
            'meta': []
        },
        'jQuery': {
            'patterns': ['jquery.js', 'jquery.min.js', 'jQuery'],
            'headers': {},
            'meta': []
        },
        'Bootstrap': {
            'patterns': ['bootstrap.css', 'bootstrap.min.css', 'bootstrap.js'],
            'headers': {},
            'meta': []
        },
        'ASP.NET': {
            'patterns': ['__VIEWSTATE', '__EVENTVALIDATION', 'aspnet'],
            'headers': {'X-AspNet-Version': '', 'X-AspNetMvc-Version': ''},
            'meta': []
        },
        'PHP': {
            'patterns': ['.php', 'PHPSESSID'],
            'headers': {'X-Powered-By': 'PHP'},
            'meta': []
        },
        'Apache': {
            'patterns': [],
            'headers': {'Server': 'Apache'},
            'meta': []
        },
        'Nginx': {
            'patterns': [],
            'headers': {'Server': 'nginx'},
            'meta': []
        },
        'IIS': {
            'patterns': [],
            'headers': {'Server': 'Microsoft-IIS'},
            'meta': []
        },
        'Cloudflare': {
            'patterns': [],
            'headers': {'Server': 'cloudflare', 'CF-Ray': ''},
            'meta': []
        },
    }

    def scan(self) -> List[Dict[str, Any]]:
        """Fingerprint technology stack"""
        try:
            self.log(f"Fingerprinting technology stack at {self.target_url}")

            response = requests.get(
                self.target_url,
                timeout=15,
                headers={'User-Agent': 'WebSecAudit/1.0 Security Scanner'}
            )

            soup = BeautifulSoup(response.text, 'html.parser')

            detected_techs = []

            # Check each technology
            for tech_name, signatures in self.TECH_SIGNATURES.items():
                detected = False

                # Check headers
                for header_name, header_value in signatures['headers'].items():
                    if header_name in response.headers:
                        if not header_value or header_value.lower() in response.headers[header_name].lower():
                            detected = True
                            self.log(f"Detected {tech_name} via header: {header_name}")
                            break

                # Check content patterns
                if not detected:
                    for pattern in signatures['patterns']:
                        if pattern in response.text:
                            detected = True
                            self.log(f"Detected {tech_name} via pattern: {pattern}")
                            break

                # Check meta tags
                if not detected and signatures['meta']:
                    meta_tags = soup.find_all('meta')
                    for meta in meta_tags:
                        if meta.get('name', '').lower() in signatures['meta']:
                            content = meta.get('content', '').lower()
                            if tech_name.lower() in content:
                                detected = True
                                self.log(f"Detected {tech_name} via meta tag")
                                break

                if detected:
                    detected_techs.append(tech_name)

            # Report detected technologies
            if detected_techs:
                self.add_finding(
                    title='Technology Stack Detected',
                    severity='INFO',
                    category='Fingerprinting',
                    description='The following technologies were detected on the website.',
                    evidence=f'Detected: {", ".join(detected_techs)}',
                    recommendation='This is informational. However, exposing technology details can help attackers identify known vulnerabilities.',
                    references=['https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/08-Fingerprint_Web_Application_Framework']
                )

            # Check for version information
            self._check_version_disclosure(response, soup)

        except requests.exceptions.RequestException as e:
            self.log(f"Request error during fingerprinting: {str(e)}")

        return self.findings

    def _check_version_disclosure(self, response, soup: BeautifulSoup):
        """Check for version information disclosure"""
        version_disclosures = []

        # Check headers for version info
        version_headers = ['Server', 'X-Powered-By', 'X-AspNet-Version', 'X-AspNetMvc-Version', 'X-Generator']

        for header in version_headers:
            if header in response.headers:
                value = response.headers[header]
                # Check if it contains version numbers
                if re.search(r'\d+\.\d+', value):
                    version_disclosures.append(f'{header}: {value}')

        # Check meta generator tag
        meta_gen = soup.find('meta', attrs={'name': 'generator'})
        if meta_gen:
            content = meta_gen.get('content', '')
            if re.search(r'\d+\.\d+', content):
                version_disclosures.append(f'Meta generator: {content}')

        # Check for version in HTML comments
        comments = soup.find_all(string=lambda text: isinstance(text, str) and 'version' in text.lower())
        for comment in comments[:5]:  # Limit to first 5
            if re.search(r'version\s*[:=]?\s*\d+\.\d+', comment.lower()):
                preview = comment[:80].strip()
                version_disclosures.append(f'Comment: {preview}...')

        if version_disclosures:
            self.add_finding(
                title='Software Version Information Disclosed',
                severity='LOW',
                category='Fingerprinting',
                description='Software version information is exposed.',
                evidence='\n'.join(version_disclosures[:5]),  # Limit evidence
                recommendation='Remove or obfuscate version information from headers, meta tags, and comments.',
                references=['https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/02-Fingerprint_Web_Server']
            )
