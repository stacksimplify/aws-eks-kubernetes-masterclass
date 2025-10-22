#!/usr/bin/env python3
"""
WebSecAudit - Comprehensive Website Security Scanner
A state-of-the-art security scanning tool for web applications
"""

import argparse
import json
import sys
import time
from datetime import datetime
from urllib.parse import urlparse
from typing import List, Dict, Any

from modules.ssl_scanner import SSLScanner
from modules.headers_scanner import HeadersScanner
from modules.xss_scanner import XSSScanner
from modules.injection_scanner import InjectionScanner
from modules.info_disclosure import InfoDisclosureScanner
from modules.cors_scanner import CORSScanner
from modules.auth_scanner import AuthScanner
from modules.tech_fingerprint import TechFingerprint
from utils.reporter import Reporter
from utils.colors import Colors


class WebSecAudit:
    """Main security scanner orchestrator"""

    def __init__(self, target_url: str, verbose: bool = False):
        self.target_url = self._normalize_url(target_url)
        self.verbose = verbose
        self.findings = []
        self.scan_start_time = None
        self.scan_end_time = None

        # Initialize all scanners
        self.scanners = [
            TechFingerprint(self.target_url, verbose),
            SSLScanner(self.target_url, verbose),
            HeadersScanner(self.target_url, verbose),
            CORSScanner(self.target_url, verbose),
            XSSScanner(self.target_url, verbose),
            InjectionScanner(self.target_url, verbose),
            InfoDisclosureScanner(self.target_url, verbose),
            AuthScanner(self.target_url, verbose),
        ]

    def _normalize_url(self, url: str) -> str:
        """Normalize URL to include protocol"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url.rstrip('/')

    def print_banner(self):
        """Print tool banner"""
        banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              WebSecAudit - Security Scanner v1.0             ║
║          Comprehensive Website Vulnerability Scanner         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.YELLOW}Target:{Colors.RESET} {self.target_url}
{Colors.YELLOW}Scan Started:{Colors.RESET} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{Colors.GREEN}[*] Initializing security scanners...{Colors.RESET}
"""
        print(banner)

    def run_scan(self):
        """Execute all security scans"""
        self.scan_start_time = time.time()
        self.print_banner()

        # Run each scanner
        for scanner in self.scanners:
            scanner_name = scanner.__class__.__name__
            print(f"\n{Colors.BLUE}[+] Running {scanner_name}...{Colors.RESET}")

            try:
                results = scanner.scan()
                if results:
                    self.findings.extend(results)
                    print(f"{Colors.GREEN}    ✓ {scanner_name} completed - Found {len(results)} issues{Colors.RESET}")
                else:
                    print(f"{Colors.GREEN}    ✓ {scanner_name} completed - No issues found{Colors.RESET}")
            except Exception as e:
                error_msg = f"Error running {scanner_name}: {str(e)}"
                print(f"{Colors.RED}    ✗ {error_msg}{Colors.RESET}")
                if self.verbose:
                    import traceback
                    traceback.print_exc()

        self.scan_end_time = time.time()

        # Generate report
        self._generate_report()

    def _generate_report(self):
        """Generate and display the security report"""
        scan_duration = self.scan_end_time - self.scan_start_time

        reporter = Reporter(
            target_url=self.target_url,
            findings=self.findings,
            scan_duration=scan_duration
        )

        # Display console report
        reporter.print_summary()
        reporter.print_detailed_findings()

        # Save reports
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        parsed_url = urlparse(self.target_url)
        hostname = parsed_url.netloc.replace(':', '_')

        # HTML Report
        html_file = f"report_{hostname}_{timestamp}.html"
        reporter.generate_html_report(html_file)
        print(f"\n{Colors.GREEN}[✓] HTML Report saved: {html_file}{Colors.RESET}")

        # JSON Report
        json_file = f"report_{hostname}_{timestamp}.json"
        reporter.generate_json_report(json_file)
        print(f"{Colors.GREEN}[✓] JSON Report saved: {json_file}{Colors.RESET}")


def main():
    parser = argparse.ArgumentParser(
        description='WebSecAudit - Comprehensive Website Security Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scanner.py https://example.com
  python scanner.py https://2rbc-ai.com -v
  python scanner.py example.com (automatically adds https://)

Security Categories Tested:
  ✓ SSL/TLS Configuration
  ✓ HTTP Security Headers
  ✓ Cross-Site Scripting (XSS)
  ✓ SQL Injection
  ✓ Information Disclosure
  ✓ CORS Misconfiguration
  ✓ CSRF Protection
  ✓ Authentication & Session Security
  ✓ Technology Fingerprinting
  ✓ Common Vulnerabilities (OWASP Top 10)

Note: Only scan websites you own or have permission to test!
        """
    )

    parser.add_argument('url', help='Target URL to scan (e.g., https://example.com)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--version', action='version', version='WebSecAudit 1.0')

    args = parser.parse_args()

    try:
        scanner = WebSecAudit(args.url, args.verbose)
        scanner.run_scan()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Scan interrupted by user{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[!] Fatal error: {str(e)}{Colors.RESET}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
