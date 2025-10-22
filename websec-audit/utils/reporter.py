"""Report generation module"""

import json
from datetime import datetime
from typing import List, Dict, Any
from collections import Counter
from utils.colors import Colors


class Reporter:
    """Generate security scan reports in multiple formats"""

    SEVERITY_ORDER = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']

    def __init__(self, target_url: str, findings: List[Dict], scan_duration: float):
        self.target_url = target_url
        self.findings = sorted(findings, key=lambda x: self.SEVERITY_ORDER.index(x.get('severity', 'INFO')))
        self.scan_duration = scan_duration
        self.severity_counts = Counter(f['severity'] for f in findings)

    def print_summary(self):
        """Print scan summary to console"""
        total_issues = len(self.findings)

        print(f"\n\n{Colors.CYAN}{'='*70}")
        print(f"                      SCAN SUMMARY")
        print(f"{'='*70}{Colors.RESET}\n")

        print(f"{Colors.YELLOW}Target URL:{Colors.RESET}      {self.target_url}")
        print(f"{Colors.YELLOW}Scan Duration:{Colors.RESET}   {self.scan_duration:.2f} seconds")
        print(f"{Colors.YELLOW}Total Issues:{Colors.RESET}    {total_issues}\n")

        print(f"{Colors.YELLOW}Issues by Severity:{Colors.RESET}")
        for severity in self.SEVERITY_ORDER:
            count = self.severity_counts.get(severity, 0)
            if count > 0:
                color = Colors.severity_color(severity)
                print(f"  {color}● {severity:8s}{Colors.RESET} : {count}")

        print(f"\n{Colors.CYAN}{'='*70}{Colors.RESET}")

    def print_detailed_findings(self):
        """Print detailed findings to console"""
        if not self.findings:
            print(f"\n{Colors.GREEN}[✓] No security issues found!{Colors.RESET}")
            return

        print(f"\n\n{Colors.CYAN}{'='*70}")
        print(f"                   DETAILED FINDINGS")
        print(f"{'='*70}{Colors.RESET}\n")

        current_severity = None
        issue_number = 1

        for finding in self.findings:
            severity = finding.get('severity', 'INFO')

            # Print severity header when it changes
            if severity != current_severity:
                current_severity = severity
                color = Colors.severity_color(severity)
                print(f"\n{color}{'─'*70}")
                print(f"  {severity} SEVERITY ISSUES")
                print(f"{'─'*70}{Colors.RESET}\n")

            # Print issue details
            color = Colors.severity_color(severity)
            print(f"{color}[{issue_number}] {finding['title']}{Colors.RESET}")
            print(f"    Category: {finding.get('category', 'Unknown')}")
            print(f"    Severity: {color}{severity}{Colors.RESET}")

            if 'description' in finding:
                print(f"    Description: {finding['description']}")

            if 'evidence' in finding:
                print(f"    Evidence: {finding['evidence']}")

            if 'recommendation' in finding:
                print(f"    {Colors.GREEN}Recommendation:{Colors.RESET} {finding['recommendation']}")

            if 'references' in finding and finding['references']:
                print(f"    References:")
                for ref in finding['references']:
                    print(f"      - {ref}")

            print()
            issue_number += 1

        print(f"{Colors.CYAN}{'='*70}{Colors.RESET}\n")

    def generate_json_report(self, filename: str):
        """Generate JSON report"""
        report_data = {
            'scan_info': {
                'target_url': self.target_url,
                'scan_date': datetime.now().isoformat(),
                'scan_duration_seconds': round(self.scan_duration, 2),
                'total_issues': len(self.findings)
            },
            'summary': {
                'severity_counts': dict(self.severity_counts)
            },
            'findings': self.findings
        }

        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=2)

    def generate_html_report(self, filename: str):
        """Generate HTML report"""
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Scan Report - {self.target_url}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .summary {{
            padding: 30px 40px;
            background: #f8f9fa;
            border-bottom: 3px solid #e9ecef;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .summary-card h3 {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
            text-transform: uppercase;
        }}
        .summary-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #1e3c72;
        }}
        .severity-badges {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin-top: 20px;
        }}
        .severity-badge {{
            padding: 10px 20px;
            border-radius: 20px;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .severity-badge .count {{
            background: rgba(255,255,255,0.3);
            padding: 2px 10px;
            border-radius: 10px;
        }}
        .severity-critical {{ background: #dc3545; color: white; }}
        .severity-high {{ background: #fd7e14; color: white; }}
        .severity-medium {{ background: #ffc107; color: #333; }}
        .severity-low {{ background: #17a2b8; color: white; }}
        .severity-info {{ background: #6c757d; color: white; }}
        .findings {{
            padding: 40px;
        }}
        .finding-section {{
            margin-bottom: 40px;
        }}
        .finding-section h2 {{
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            color: white;
        }}
        .finding-card {{
            background: white;
            border-left: 5px solid;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .finding-card.critical {{ border-left-color: #dc3545; }}
        .finding-card.high {{ border-left-color: #fd7e14; }}
        .finding-card.medium {{ border-left-color: #ffc107; }}
        .finding-card.low {{ border-left-color: #17a2b8; }}
        .finding-card.info {{ border-left-color: #6c757d; }}
        .finding-title {{
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #1e3c72;
        }}
        .finding-meta {{
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
            font-size: 0.9em;
        }}
        .finding-meta span {{
            background: #f8f9fa;
            padding: 5px 12px;
            border-radius: 5px;
        }}
        .finding-description {{
            margin: 15px 0;
            line-height: 1.6;
            color: #555;
        }}
        .finding-evidence {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            border-left: 3px solid #667eea;
        }}
        .finding-recommendation {{
            background: #d4edda;
            border-left: 3px solid #28a745;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }}
        .finding-recommendation strong {{
            color: #155724;
        }}
        .references {{
            margin-top: 15px;
        }}
        .references a {{
            color: #667eea;
            text-decoration: none;
            display: block;
            padding: 5px 0;
        }}
        .references a:hover {{
            text-decoration: underline;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 3px solid #e9ecef;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 WebSecAudit Security Report</h1>
            <p>Comprehensive Security Assessment</p>
        </div>

        <div class="summary">
            <h2 style="color: #1e3c72; margin-bottom: 20px;">Scan Summary</h2>
            <div class="summary-grid">
                <div class="summary-card">
                    <h3>Target URL</h3>
                    <div class="value" style="font-size: 1.2em; word-break: break-all;">{self.target_url}</div>
                </div>
                <div class="summary-card">
                    <h3>Scan Date</h3>
                    <div class="value" style="font-size: 1em;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                </div>
                <div class="summary-card">
                    <h3>Duration</h3>
                    <div class="value">{self.scan_duration:.2f}s</div>
                </div>
                <div class="summary-card">
                    <h3>Total Issues</h3>
                    <div class="value">{len(self.findings)}</div>
                </div>
            </div>

            <div class="severity-badges">
                {self._generate_severity_badges_html()}
            </div>
        </div>

        <div class="findings">
            {self._generate_findings_html()}
        </div>

        <div class="footer">
            <p>Generated by WebSecAudit v1.0 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p style="margin-top: 10px; font-size: 0.9em;">⚠️ This report contains sensitive security information. Handle with care.</p>
        </div>
    </div>
</body>
</html>"""

        with open(filename, 'w') as f:
            f.write(html_content)

    def _generate_severity_badges_html(self) -> str:
        """Generate HTML for severity badges"""
        badges_html = []
        for severity in self.SEVERITY_ORDER:
            count = self.severity_counts.get(severity, 0)
            if count > 0:
                severity_lower = severity.lower()
                badges_html.append(
                    f'<div class="severity-badge severity-{severity_lower}">'
                    f'{severity} <span class="count">{count}</span>'
                    f'</div>'
                )
        return '\n'.join(badges_html)

    def _generate_findings_html(self) -> str:
        """Generate HTML for findings"""
        if not self.findings:
            return '<p style="text-align: center; color: #28a745; font-size: 1.2em;">✓ No security issues found!</p>'

        findings_html = []
        current_severity = None

        for finding in self.findings:
            severity = finding.get('severity', 'INFO')

            # Add section header when severity changes
            if severity != current_severity:
                if current_severity is not None:
                    findings_html.append('</div>')  # Close previous section

                current_severity = severity
                severity_lower = severity.lower()
                bg_colors = {
                    'CRITICAL': '#dc3545',
                    'HIGH': '#fd7e14',
                    'MEDIUM': '#ffc107',
                    'LOW': '#17a2b8',
                    'INFO': '#6c757d'
                }
                findings_html.append(
                    f'<div class="finding-section">'
                    f'<h2 style="background: {bg_colors.get(severity, "#6c757d")};">'
                    f'{severity} SEVERITY ISSUES</h2>'
                )

            # Add finding card
            severity_lower = severity.lower()
            card_html = f'<div class="finding-card {severity_lower}">'
            card_html += f'<div class="finding-title">{finding["title"]}</div>'

            card_html += '<div class="finding-meta">'
            card_html += f'<span><strong>Category:</strong> {finding.get("category", "Unknown")}</span>'
            card_html += f'<span><strong>Severity:</strong> {severity}</span>'
            card_html += '</div>'

            if 'description' in finding:
                card_html += f'<div class="finding-description">{finding["description"]}</div>'

            if 'evidence' in finding:
                card_html += f'<div class="finding-evidence"><strong>Evidence:</strong><br>{finding["evidence"]}</div>'

            if 'recommendation' in finding:
                card_html += f'<div class="finding-recommendation"><strong>Recommendation:</strong><br>{finding["recommendation"]}</div>'

            if 'references' in finding and finding['references']:
                card_html += '<div class="references"><strong>References:</strong><br>'
                for ref in finding['references']:
                    card_html += f'<a href="{ref}" target="_blank">{ref}</a>'
                card_html += '</div>'

            card_html += '</div>'
            findings_html.append(card_html)

        findings_html.append('</div>')  # Close last section
        return '\n'.join(findings_html)
