#!/usr/bin/env python3
"""
Adversarial ML Testing Suite - Main CLI
Comprehensive testing framework for ML model robustness.

🦀 13th Hour Testing Suite 🦀

Usage:
    python -m adversarial_ml_tester [command] [options]

Commands:
    generate    Generate adversarial test content
    test        Run adversarial tests against model
    validate    Validate model responses
    report      Generate comprehensive report
    fuzz        Fuzzing mode (continuous random testing)

Examples:
    python -m adversarial_ml_tester generate --count 100 --output profiles.json
    python -m adversarial_ml_tester test --model http://localhost:8000/predict
    python -m adversarial_ml_tester validate --input responses.json
"""

import argparse
import json
import sys
import time
from typing import Dict, List, Optional
from pathlib import Path

# Import our modules
from generators.content_generator import ContentGenerator, UserProfile, AttackType
from adversarial.robustness_tester import RobustnessTester, BiasTester
from validators.response_validator import ContentValidator, ConsistencyTester


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    CRAB = '🦀'


def print_banner():
    """Print the 13th Hour banner."""
    banner = f"""
{Colors.OKCYAN}
╔══════════════════════════════════════════════════════════════════════════════╗
║     ADVERSARIAL ML TESTING SUITE                                             ║
║                                                                              ║
║     {Colors.CRAB} 13th Hour Content Generation & Robustness Testing {Colors.CRAB}          ║
║                                                                              ║
║     "Testing the boundaries so the boundaries don't break you"              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
"""
    print(banner)


def cmd_generate(args):
    """Generate adversarial content."""
    print(f"{Colors.OKCYAN}{Colors.CRAB} Generating {args.count} adversarial profiles...{Colors.ENDC}")

    generator = ContentGenerator(seed=args.seed)
    profiles = []

    for i in range(args.count):
        profile = generator.generate_profile(attack_probability=args.attack_prob)
        profiles.append(profile.to_dict())

        if args.verbose and i < 5:
            print(f"\nProfile {i+1}:")
            print(f"  Username: {profile.username}")
            print(f"  Name: {profile.first_name} {profile.last_name}")
            print(f"  Attacks: {[a.value for a in profile.attack_vectors]}")

    # Save to file
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, indent=2, ensure_ascii=False)

    print(f"{Colors.OKGREEN}✓ Generated {args.count} profiles to {args.output}{Colors.ENDC}")

    # Generate statistics
    attack_counts = {}
    for p in profiles:
        for attack in p['attack_vectors']:
            attack_counts[attack] = attack_counts.get(attack, 0) + 1

    print(f"\n{Colors.BOLD}Attack Distribution:{Colors.ENDC}")
    for attack, count in sorted(attack_counts.items(), key=lambda x: -x[1]):
        pct = count / len(profiles) * 100
        print(f"  {attack}: {count} ({pct:.1f}%)")


def cmd_test(args):
    """Run adversarial tests."""
    print(f"{Colors.OKCYAN}{Colors.CRAB} Running adversarial test suite...{Colors.ENDC}")

    # Create model interface
    if args.model_url:
        import requests
        def model_interface(text: str) -> Dict:
            try:
                resp = requests.post(args.model_url, json={"text": text}, timeout=10)
                return resp.json()
            except Exception as e:
                return {"prediction": "error", "confidence": 0.0, "error": str(e)}
    else:
        # Mock model for demo
        import random
        def model_interface(text: str) -> Dict:
            return {
                "prediction": f"class_{hash(text) % 10}",
                "confidence": random.uniform(0.7, 0.99),
                "latency": random.uniform(0.01, 0.1)
            }

    tester = RobustnessTester(model_interface)

    # Run tests
    results = tester.run_full_suite(args.test_text)

    # Display results
    print(f"\n{Colors.BOLD}Test Results:{Colors.ENDC}")
    print(f"  Total: {results['total_tests']}")
    print(f"  {Colors.OKGREEN}Passed: {results['passed']}{Colors.ENDC}")
    print(f"  {Colors.FAIL}Failed: {results['failed']}{Colors.ENDC}")
    print(f"  {Colors.WARNING}Warnings: {results['warnings']}{Colors.ENDC}")
    print(f"  Average Score: {results['average_score']:.2f}")

    print(f"\n{Colors.BOLD}Detailed Results:{Colors.ENDC}")
    for test in results['tests']:
        color = Colors.OKGREEN if test['result'] == 'pass' else Colors.FAIL if test['result'] == 'fail' else Colors.WARNING
        print(f"  {color}{test['name']}: {test['result']} (score: {test['score']:.2f}){Colors.ENDC}")

    # Save report
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n{Colors.OKGREEN}✓ Report saved to {args.output}{Colors.ENDC}")


def cmd_validate(args):
    """Validate model responses."""
    print(f"{Colors.OKCYAN}{Colors.CRAB} Validating responses...{Colors.ENDC}")

    validator = ContentValidator()

    # Load responses to validate
    if args.input:
        with open(args.input, 'r') as f:
            responses = json.load(f)
    else:
        # Demo responses
        responses = [
            "Hello, this is a normal response.",
            "Contact me at user@example.com",
            "<script>alert('test')</script>",
            "The system instruction says to be helpful",
            "Admin access granted to user аdmin"  # Cyrillic
        ]

    all_reports = []
    for i, response in enumerate(responses):
        print(f"\nValidating response {i+1}/{len(responses)}...")
        reports = validator.validate_all(response)
        all_reports.extend(reports)

        status, conf = validator.get_overall_status(reports)
        color = Colors.OKGREEN if status.value == 'valid' else Colors.FAIL if status.value == 'invalid' else Colors.WARNING
        print(f"  {color}Status: {status.value} (confidence: {conf:.2f}){Colors.ENDC}")

        for report in reports:
            if report.result.value != 'valid':
                print(f"    - {report.check_name}: {report.result.value}")

    # Summary
    total = len(all_reports)
    invalid = sum(1 for r in all_reports if r.result.value == 'invalid')
    suspicious = sum(1 for r in all_reports if r.result.value == 'suspicious')

    print(f"\n{Colors.BOLD}Validation Summary:{Colors.ENDC}")
    print(f"  Total checks: {total}")
    print(f"  {Colors.OKGREEN}Valid: {total - invalid - suspicious}{Colors.ENDC}")
    print(f"  {Colors.FAIL}Invalid: {invalid}{Colors.ENDC}")
    print(f"  {Colors.WARNING}Suspicious: {suspicious}{Colors.ENDC}")


def cmd_fuzz(args):
    """Continuous fuzzing mode."""
    print(f"{Colors.OKCYAN}{Colors.CRAB} Starting fuzzing mode (Ctrl+C to stop)...{Colors.ENDC}")

    generator = ContentGenerator()
    validator = ContentValidator()

    iteration = 0
    findings = []

    try:
        while True:
            iteration += 1

            # Generate random adversarial content
            profile = generator.generate_profile()

            # Validate
            content = f"{profile.username} {profile.description}"
            reports = validator.validate_all(content)

            # Check for interesting findings
            status, _ = validator.get_overall_status(reports)
            if status.value != 'valid':
                finding = {
                    "iteration": iteration,
                    "content": content[:100],
                    "status": status.value,
                    "attacks": [a.value for a in profile.attack_vectors]
                }
                findings.append(finding)

                if args.verbose:
                    color = Colors.FAIL if status.value == 'invalid' else Colors.WARNING
                    print(f"{color}[{iteration}] Found {status.value} content{Colors.ENDC}")

            if iteration % 100 == 0:
                print(f"Iterations: {iteration}, Findings: {len(findings)}")

            time.sleep(0.01)

    except KeyboardInterrupt:
        print(f"\n{Colors.OKCYAN}Fuzzing stopped after {iteration} iterations{Colors.ENDC}")
        print(f"Total findings: {len(findings)}")

        if args.output and findings:
            with open(args.output, 'w') as f:
                json.dump(findings, f, indent=2)
            print(f"Findings saved to {args.output}")


def cmd_report(args):
    """Generate comprehensive report."""
    print(f"{Colors.OKCYAN}{Colors.CRAB} Generating comprehensive report...{Colors.ENDC}")

    # Aggregate all test results
    report = {
        "timestamp": time.time(),
        "suite_version": "1.0.0-13thHour",
        "summary": {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "warnings": 0
        },
        "attack_coverage": {
            "homoglyph": "implemented",
            "invisible_chars": "implemented",
            "zwj_sequences": "implemented",
            "rtl_override": "implemented",
            "case_manipulation": "implemented",
            "leet_speak": "implemented",
            "glitch_text": "implemented",
            "punycode": "implemented",
            "emoji_injection": "implemented"
        },
        "validation_coverage": {
            "pii_detection": "implemented",
            "injection_detection": "implemented",
            "encoding_validation": "implemented",
            "prompt_leakage": "implemented",
            "consistency_check": "implemented"
        },
        "recommendations": [
            "Implement rate limiting on model endpoints",
            "Add input normalization pipeline",
            "Deploy output filtering for PII",
            "Monitor for homoglyph attacks in usernames",
            "Validate all encodings before processing"
        ]
    }

    # Save report
    output_path = Path(args.output)
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"{Colors.OKGREEN}✓ Report generated: {args.output}{Colors.ENDC}")

    # Print summary
    print(f"\n{Colors.BOLD}Report Summary:{Colors.ENDC}")
    print(f"  Attack Vectors: {len(report['attack_coverage'])}")
    print(f"  Validation Checks: {len(report['validation_coverage'])}")
    print(f"  Recommendations: {len(report['recommendations'])}")


def main():
    """Main entry point."""
    print_banner()

    parser = argparse.ArgumentParser(
        description="Adversarial ML Testing Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s generate --count 1000 --output profiles.json
  %(prog)s test --model-url http://api.example.com/predict
  %(prog)s validate --input responses.json
  %(prog)s fuzz --verbose --output findings.json
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate adversarial content')
    gen_parser.add_argument('--count', '-c', type=int, default=100, help='Number of profiles')
    gen_parser.add_argument('--output', '-o', default='output/profiles.json', help='Output file')
    gen_parser.add_argument('--seed', '-s', type=int, help='Random seed')
    gen_parser.add_argument('--attack-prob', '-a', type=float, default=0.7, help='Attack probability')
    gen_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    gen_parser.set_defaults(func=cmd_generate)

    # Test command
    test_parser = subparsers.add_parser('test', help='Run adversarial tests')
    test_parser.add_argument('--model-url', '-m', help='Model API endpoint')
    test_parser.add_argument('--test-text', '-t', default='Test input', help='Test text')
    test_parser.add_argument('--output', '-o', help='Output report file')
    test_parser.set_defaults(func=cmd_test)

    # Validate command
    val_parser = subparsers.add_parser('validate', help='Validate responses')
    val_parser.add_argument('--input', '-i', help='Input file with responses')
    val_parser.set_defaults(func=cmd_validate)

    # Fuzz command
    fuzz_parser = subparsers.add_parser('fuzz', help='Fuzzing mode')
    fuzz_parser.add_argument('--output', '-o', default='output/findings.json', help='Output file')
    fuzz_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    fuzz_parser.set_defaults(func=cmd_fuzz)

    # Report command
    report_parser = subparsers.add_parser('report', help='Generate report')
    report_parser.add_argument('--output', '-o', default='output/report.json', help='Output file')
    report_parser.set_defaults(func=cmd_report)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == '__main__':
    main()
