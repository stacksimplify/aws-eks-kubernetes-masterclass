"""SSL/TLS Security Scanner"""

import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime
from typing import List, Dict, Any

from modules.base_scanner import BaseScanner


class SSLScanner(BaseScanner):
    """Scanner for SSL/TLS configuration issues"""

    # Weak/deprecated protocols
    WEAK_PROTOCOLS = ['SSLv2', 'SSLv3', 'TLSv1', 'TLSv1.1']

    # Weak ciphers (examples)
    WEAK_CIPHERS = [
        'DES', 'RC4', 'MD5', 'NULL', 'anon', 'EXPORT',
        '3DES', 'ADH', 'AECDH'
    ]

    def scan(self) -> List[Dict[str, Any]]:
        """Scan SSL/TLS configuration"""
        parsed_url = urlparse(self.target_url)

        # Skip if not HTTPS
        if parsed_url.scheme != 'https':
            self.add_finding(
                title='HTTPS Not Used',
                severity='HIGH',
                category='SSL/TLS',
                description='The website does not use HTTPS encryption.',
                evidence=f'URL scheme: {parsed_url.scheme}',
                recommendation='Enable HTTPS for all pages to protect data in transit.',
                references=[
                    'https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/09-Testing_for_Weak_Cryptography/01-Testing_for_Weak_Transport_Layer_Security'
                ]
            )
            return self.findings

        hostname = parsed_url.netloc.split(':')[0]
        port = parsed_url.port or 443

        self.log(f"Checking SSL/TLS for {hostname}:{port}")

        try:
            # Check certificate validity
            self._check_certificate(hostname, port)

            # Check protocol versions
            self._check_protocol_versions(hostname, port)

            # Check cipher suites
            self._check_cipher_suites(hostname, port)

        except Exception as e:
            self.log(f"Error during SSL/TLS scan: {str(e)}")
            self.add_finding(
                title='SSL/TLS Connection Error',
                severity='MEDIUM',
                category='SSL/TLS',
                description='Unable to establish SSL/TLS connection for testing.',
                evidence=str(e),
                recommendation='Verify that the server is accessible and properly configured.'
            )

        return self.findings

    def _check_certificate(self, hostname: str, port: int):
        """Check SSL certificate validity"""
        try:
            context = ssl.create_default_context()

            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()

                    # Check certificate expiration
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_until_expiry = (not_after - datetime.now()).days

                    if days_until_expiry < 0:
                        self.add_finding(
                            title='Expired SSL Certificate',
                            severity='CRITICAL',
                            category='SSL/TLS',
                            description='The SSL certificate has expired.',
                            evidence=f'Expiry date: {not_after}',
                            recommendation='Renew the SSL certificate immediately.',
                            references=['https://www.ssl.com/faqs/what-happens-when-your-ssl-certificate-expires/']
                        )
                    elif days_until_expiry < 30:
                        self.add_finding(
                            title='SSL Certificate Expiring Soon',
                            severity='MEDIUM',
                            category='SSL/TLS',
                            description=f'The SSL certificate will expire in {days_until_expiry} days.',
                            evidence=f'Expiry date: {not_after}',
                            recommendation='Renew the SSL certificate soon to avoid service disruption.'
                        )

                    # Check for self-signed certificate
                    issuer = dict(x[0] for x in cert['issuer'])
                    subject = dict(x[0] for x in cert['subject'])

                    if issuer == subject:
                        self.add_finding(
                            title='Self-Signed SSL Certificate',
                            severity='HIGH',
                            category='SSL/TLS',
                            description='The server is using a self-signed certificate.',
                            evidence=f'Issuer: {issuer.get("commonName", "Unknown")}',
                            recommendation='Use a certificate from a trusted Certificate Authority (CA).',
                            references=['https://owasp.org/www-community/vulnerabilities/Using_Self-Signed_Certificate']
                        )

        except ssl.SSLError as e:
            self.add_finding(
                title='SSL Certificate Validation Failed',
                severity='HIGH',
                category='SSL/TLS',
                description='SSL certificate validation failed.',
                evidence=str(e),
                recommendation='Ensure the certificate is valid and properly configured.'
            )
        except Exception as e:
            self.log(f"Certificate check error: {str(e)}")

    def _check_protocol_versions(self, hostname: str, port: int):
        """Check for weak SSL/TLS protocol versions"""
        # Check currently used protocol
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    version = ssock.version()
                    self.log(f"Protocol version in use: {version}")

                    # Check if using outdated TLS version
                    if version in self.WEAK_PROTOCOLS:
                        self.add_finding(
                            title=f'Weak TLS Protocol: {version}',
                            severity='HIGH',
                            category='SSL/TLS',
                            description=f'The server is using the deprecated {version} protocol.',
                            evidence=f'Protocol: {version}',
                            recommendation='Disable SSLv2, SSLv3, TLSv1.0, and TLSv1.1. Use TLS 1.2 or TLS 1.3.',
                            references=['https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/09-Testing_for_Weak_Cryptography/01-Testing_for_Weak_Transport_Layer_Security']
                        )
                    elif version == 'TLSv1.2':
                        self.add_finding(
                            title='TLS 1.3 Not Supported',
                            severity='LOW',
                            category='SSL/TLS',
                            description='The server does not appear to support TLS 1.3.',
                            evidence=f'Current protocol: {version}',
                            recommendation='Consider enabling TLS 1.3 for improved security and performance.'
                        )

        except Exception as e:
            self.log(f"Protocol check error: {str(e)}")

    def _check_cipher_suites(self, hostname: str, port: int):
        """Check for weak cipher suites"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cipher = ssock.cipher()
                    if cipher:
                        cipher_name = cipher[0]
                        self.log(f"Cipher in use: {cipher_name}")

                        # Check for weak ciphers
                        for weak_cipher in self.WEAK_CIPHERS:
                            if weak_cipher.upper() in cipher_name.upper():
                                self.add_finding(
                                    title=f'Weak Cipher Suite Detected',
                                    severity='HIGH',
                                    category='SSL/TLS',
                                    description=f'The server is using a weak cipher suite: {cipher_name}',
                                    evidence=f'Cipher: {cipher_name}',
                                    recommendation='Disable weak cipher suites and use strong ciphers (AES-GCM, ChaCha20).',
                                    references=['https://wiki.mozilla.org/Security/Server_Side_TLS']
                                )
                                break

        except Exception as e:
            self.log(f"Cipher check error: {str(e)}")
