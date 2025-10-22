"""Base scanner class for all security scanners"""

from typing import List, Dict, Any
from abc import ABC, abstractmethod


class BaseScanner(ABC):
    """Abstract base class for all security scanners"""

    def __init__(self, target_url: str, verbose: bool = False):
        self.target_url = target_url
        self.verbose = verbose
        self.findings = []

    @abstractmethod
    def scan(self) -> List[Dict[str, Any]]:
        """Execute the security scan and return findings"""
        pass

    def add_finding(self, title: str, severity: str, category: str,
                   description: str = None, evidence: str = None,
                   recommendation: str = None, references: List[str] = None):
        """Add a security finding to the results"""
        finding = {
            'title': title,
            'severity': severity.upper(),
            'category': category,
        }

        if description:
            finding['description'] = description
        if evidence:
            finding['evidence'] = evidence
        if recommendation:
            finding['recommendation'] = recommendation
        if references:
            finding['references'] = references

        self.findings.append(finding)

    def log(self, message: str):
        """Log verbose messages"""
        if self.verbose:
            print(f"    [DEBUG] {message}")
