#!/usr/bin/env python3
"""
Response Validation and Consistency Testing
Validates model outputs for security, consistency, and quality.

🦀 13th Hour Response Validation 🦀
"""

import re
import hashlib
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import time


class ValidationResult(Enum):
    VALID = "valid"
    INVALID = "invalid"
    SUSPICIOUS = "suspicious"
    REQUIRES_REVIEW = "requires_review"


@dataclass
class ValidationReport:
    """Report from validation check."""
    check_name: str
    result: ValidationResult
    confidence: float
    details: Dict[str, Any]
    remediation: Optional[str] = None


class ContentValidator:
    """Validate generated content for safety and policy compliance."""

    # Patterns for potentially harmful content
    SUSPICIOUS_PATTERNS = {
        "pii": [
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
            r'\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b',  # Credit card
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',  # IP address
        ],
        "injection": [
            r'<script[^>]*>',
            r'javascript:',
            r'on\w+\s*=',
            r'\$\{.*\}',
            r'\{\{.*\}\}',
            r'<%.*%>',
            r'\[\[.*\]\]'
        ],
        "encoding_tricks": [
            r'%[0-9a-fA-F]{2}',  # URL encoding
            r'\\x[0-9a-fA-F]{2}',  # Hex escape
            r'\\u[0-9a-fA-F]{4}',  # Unicode escape
            r'&#x[0-9a-fA-F]+;',  # HTML hex entity
            r'&#[0-9]+;',  # HTML decimal entity
        ],
        "prompt_leakage": [
            r'system prompt',
            r'instruction:',
            r'\[system\]',
            r'<system>',
            r'you are (an? )?(ai|assistant|bot)',
            r'model instructions'
        ]
    }

    def __init__(self, custom_rules: List[Dict] = None):
        self.rules = custom_rules or []
        self.validation_history: List[ValidationReport] = []

    def validate_pii(self, content: str) -> ValidationReport:
        """Check for personally identifiable information."""
        findings = []

        for pattern in self.SUSPICIOUS_PATTERNS["pii"]:
            matches = re.finditer(pattern, content)
            for match in matches:
                findings.append({
                    "type": "pii",
                    "pattern": pattern[:30],
                    "position": match.span(),
                    "masked": content[match.start():match.end()][:3] + "***"
                })

        if not findings:
            return ValidationReport(
                check_name="pii_detection",
                result=ValidationResult.VALID,
                confidence=0.99,
                details={"findings": 0}
            )

        return ValidationReport(
            check_name="pii_detection",
            result=ValidationResult.INVALID if len(findings) > 2 else ValidationResult.SUSPICIOUS,
            confidence=min(0.5 + len(findings) * 0.1, 0.95),
            details={"findings": findings, "count": len(findings)},
            remediation="Remove PII or apply masking before processing"
        )

    def validate_injection(self, content: str) -> ValidationReport:
        """Check for injection attempts."""
        findings = []

        for pattern in self.SUSPICIOUS_PATTERNS["injection"]:
            if re.search(pattern, content, re.IGNORECASE):
                findings.append(pattern)

        if not findings:
            return ValidationReport(
                check_name="injection_detection",
                result=ValidationResult.VALID,
                confidence=0.99,
                details={"findings": 0}
            )

        return ValidationReport(
            check_name="injection_detection",
            result=ValidationResult.INVALID,
            confidence=0.95,
            details={"patterns_found": findings},
            remediation="Sanitize input, remove script tags and event handlers"
        )

    def validate_encoding(self, content: str) -> ValidationReport:
        """Check for suspicious encoding."""
        findings = []

        for pattern in self.SUSPICIOUS_PATTERNS["encoding_tricks"]:
            matches = re.findall(pattern, content)
            if matches:
                findings.extend(matches[:5])  # Limit details

        # Check for mixed scripts (potential homograph attack)
        scripts = set()
        for char in content:
            if ord(char) > 127:
                # Simplified script detection
                if '\u0400' <= char <= '\u04FF':
                    scripts.add('cyrillic')
                elif '\u0370' <= char <= '\u03FF':
                    scripts.add('greek')
                elif '\u0600' <= char <= '\u06FF':
                    scripts.add('arabic')

        if len(scripts) > 1:
            findings.append(f"mixed_scripts:{scripts}")

        if not findings:
            return ValidationReport(
                check_name="encoding_validation",
                result=ValidationResult.VALID,
                confidence=0.98,
                details={"scripts": list(scripts) if scripts else ["latin"]}
            )

        return ValidationReport(
            check_name="encoding_validation",
            result=ValidationResult.SUSPICIOUS,
            confidence=0.75,
            details={"findings": findings, "scripts": list(scripts)},
            remediation="Normalize encoding, check for homograph attacks"
        )

    def validate_prompt_leakage(self, content: str) -> ValidationReport:
        """Check if model is leaking system prompts."""
        findings = []

        for pattern in self.SUSPICIOUS_PATTERNS["prompt_leakage"]:
            if re.search(pattern, content, re.IGNORECASE):
                findings.append(pattern)

        if not findings:
            return ValidationReport(
                check_name="prompt_leakage",
                result=ValidationResult.VALID,
                confidence=0.95,
                details={"leakage_detected": False}
            )

        return ValidationReport(
            check_name="prompt_leakage",
            result=ValidationResult.INVALID,
            confidence=0.9,
            details={"patterns": findings},
            remediation="Filter system prompt references from output"
        )

    def validate_consistency(self, content: str, 
                            previous_versions: List[str]) -> ValidationReport:
        """Check consistency with previous outputs."""
        if not previous_versions:
            return ValidationReport(
                check_name="consistency_check",
                result=ValidationResult.VALID,
                confidence=1.0,
                details={"baseline": True}
            )

        # Simple similarity check (in production, use embeddings)
        similarities = []
        for prev in previous_versions[-5:]:  # Compare to last 5
            # Jaccard similarity of words
            words1 = set(content.lower().split())
            words2 = set(prev.lower().split())
            intersection = len(words1 & words2)
            union = len(words1 | words2)
            similarity = intersection / union if union > 0 else 0
            similarities.append(similarity)

        avg_similarity = sum(similarities) / len(similarities)

        # Check for exact repetition (possible caching issue)
        exact_matches = sum(1 for prev in previous_versions if prev == content)

        if exact_matches > 2:
            return ValidationReport(
                check_name="consistency_check",
                result=ValidationResult.SUSPICIOUS,
                confidence=0.8,
                details={
                    "exact_matches": exact_matches,
                    "avg_similarity": avg_similarity
                },
                remediation="Check for deterministic output issues or caching"
            )

        return ValidationReport(
            check_name="consistency_check",
            result=ValidationResult.VALID,
            confidence=0.85,
            details={
                "avg_similarity": avg_similarity,
                "exact_matches": exact_matches
            }
        )

    def validate_all(self, content: str, 
                    context: Dict = None) -> List[ValidationReport]:
        """Run all validation checks."""
        reports = [
            self.validate_pii(content),
            self.validate_injection(content),
            self.validate_encoding(content),
            self.validate_prompt_leakage(content)
        ]

        if context and 'previous_outputs' in context:
            reports.append(
                self.validate_consistency(content, context['previous_outputs'])
            )

        self.validation_history.extend(reports)
        return reports

    def get_overall_status(self, reports: List[ValidationReport]) -> Tuple[ValidationResult, float]:
        """Get overall validation status from multiple reports."""
        if any(r.result == ValidationResult.INVALID for r in reports):
            return ValidationResult.INVALID, 0.0

        if any(r.result == ValidationResult.SUSPICIOUS for r in reports):
            avg_conf = statistics.mean([r.confidence for r in reports])
            return ValidationResult.SUSPICIOUS, avg_conf

        if any(r.result == ValidationResult.REQUIRES_REVIEW for r in reports):
            return ValidationResult.REQUIRES_REVIEW, 0.7

        avg_conf = statistics.mean([r.confidence for r in reports])
        return ValidationResult.VALID, avg_conf


class ConsistencyTester:
    """Test model consistency across multiple invocations."""

    def __init__(self, model_interface: Callable):
        self.model = model_interface
        self.history: List[Dict] = []

    def test_determinism(self, prompt: str, n_trials: int = 10) -> Dict:
        """Test if model produces deterministic outputs."""
        outputs = []

        for _ in range(n_trials):
            result = self.model(prompt)
            outputs.append(result['prediction'])
            time.sleep(0.01)  # Small delay between calls

        unique_outputs = set(outputs)

        return {
            "deterministic": len(unique_outputs) == 1,
            "unique_outputs": len(unique_outputs),
            "total_trials": n_trials,
            "entropy": self._calculate_entropy(outputs),
            "samples": list(unique_outputs)[:5]
        }

    def test_temperature_sensitivity(self, prompt: str, 
                                     temperatures: List[float] = None) -> Dict:
        """Test how sensitive model is to temperature changes."""
        if temperatures is None:
            temperatures = [0.0, 0.5, 1.0, 1.5]

        results = {}
        for temp in temperatures:
            # Assuming model accepts temperature parameter
            result = self.model(prompt, temperature=temp)
            results[temp] = result

        # Check variance across temperatures
        predictions = [r['prediction'] for r in results.values()]
        unique = len(set(predictions))

        return {
            "temperatures_tested": temperatures,
            "unique_predictions": unique,
            "sensitivity": "high" if unique == len(temperatures) else "low",
            "results": results
        }

    def test_context_window(self, base_prompt: str, 
                           filler_text: str = " ",
                           max_length: int = 10000) -> Dict:
        """Test model behavior with varying context lengths."""
        results = []

        for length in [100, 1000, 5000, 10000]:
            if length > max_length:
                break

            # Create prompt of specified length
            extended_prompt = base_prompt + filler_text * length

            try:
                start = time.time()
                result = self.model(extended_prompt)
                latency = time.time() - start

                results.append({
                    "context_length": length,
                    "success": True,
                    "latency": latency,
                    "prediction": result['prediction'][:50]
                })
            except Exception as e:
                results.append({
                    "context_length": length,
                    "success": False,
                    "error": str(e)
                })
                break

        return {
            "max_tested_length": max(r['context_length'] for r in results if r.get('success')),
            "results": results
        }

    def _calculate_entropy(self, items: List[str]) -> float:
        """Calculate Shannon entropy of items."""
        from collections import Counter
        import math

        counts = Counter(items)
        total = len(items)
        entropy = 0.0

        for count in counts.values():
            p = count / total
            entropy -= p * math.log2(p)

        return entropy


if __name__ == "__main__":
    print("🦀 Response Validation Demo 🦀\n")

    validator = ContentValidator()

    test_contents = [
        "Hello, my name is John and I like coding.",
        "Contact me at john@example.com or call 555-1234",
        "<script>alert('xss')</script>",
        "Hello аdministrator (with cyrillic a)",
        "The system prompt says you should be helpful"
    ]

    for content in test_contents:
        print(f"Testing: {content[:50]}...")
        reports = validator.validate_all(content)

        status, conf = validator.get_overall_status(reports)
        print(f"  Overall: {status.value} (confidence: {conf:.2f})")

        for report in reports:
            if report.result != ValidationResult.VALID:
                print(f"    - {report.check_name}: {report.result.value}")
                if report.remediation:
                    print(f"      Remediation: {report.remediation}")
        print()
