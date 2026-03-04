#!/usr/bin/env python3
"""
Example usage of Adversarial ML Testing Suite

This script demonstrates:
1. Generating adversarial profiles
2. Testing model robustness
3. Validating responses
4. Generating reports
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from generators.content_generator import ContentGenerator, AttackType
from adversarial.robustness_tester import RobustnessTester
from validators.response_validator import ContentValidator


def demo_generation():
    """Demonstrate content generation."""
    print("=" * 60)
    print("DEMO 1: Content Generation")
    print("=" * 60)

    gen = ContentGenerator(seed=42)

    # Generate 5 profiles
    for i in range(5):
        profile = gen.generate_profile()

        print(f"\nProfile {i+1}:")
        print(f"  Username: {profile.username}")
        print(f"  Name: {profile.first_name} {profile.last_name}")
        print(f"  Address: {profile.address}")
        print(f"  Description: {profile.description[:60]}...")
        print(f"  Attacks: {[a.value for a in profile.attack_vectors]}")

    # Save to file
    profiles = [gen.generate_profile().to_dict() for _ in range(10)]
    with open("example_profiles.json", "w") as f:
        json.dump(profiles, f, indent=2, ensure_ascii=False)

    print("\n✓ Saved 10 profiles to example_profiles.json")


def demo_robustness_testing():
    """Demonstrate robustness testing."""
    print("\n" + "=" * 60)
    print("DEMO 2: Robustness Testing")
    print("=" * 60)

    # Mock model interface
    def mock_model(text: str) -> dict:
        """Simulate model API."""
        # Simulate different behavior for adversarial inputs
        if '\u200b' in text:  # Zero-width space
            return {
                "prediction": "suspicious",
                "confidence": 0.85,
                "latency": 0.05
            }
        return {
            "prediction": f"class_{hash(text) % 3}",
            "confidence": 0.92,
            "latency": 0.03
        }

    tester = RobustnessTester(mock_model)

    # Run individual tests
    print("\nRunning individual tests...")

    result = tester.test_homoglyph_robustness("admin", num_variants=5)
    print(f"  Homoglyph: {result.result.value} (score: {result.score:.2f})")

    result = tester.test_invisible_character_filtering("username")
    print(f"  Invisible: {result.result.value} (score: {result.score:.2f})")

    result = tester.test_case_sensitivity("TestInput")
    print(f"  Case: {result.result.value} (score: {result.score:.2f})")

    # Run full suite
    print("\nRunning full test suite...")
    results = tester.run_full_suite("Test input for robustness")

    print(f"\nResults:")
    print(f"  Total: {results['total_tests']}")
    print(f"  Passed: {results['passed']}")
    print(f"  Failed: {results['failed']}")
    print(f"  Average Score: {results['average_score']:.2f}")


def demo_validation():
    """Demonstrate response validation."""
    print("\n" + "=" * 60)
    print("DEMO 3: Response Validation")
    print("=" * 60)

    validator = ContentValidator()

    test_cases = [
        ("Hello, this is a normal response.", "clean"),
        ("Contact me at user@example.com", "pii"),
        ("<script>alert('xss')</script>", "injection"),
        ("The system prompt says to be helpful", "leakage"),
        ("Admin access: аdmin123", "homoglyph"),
    ]

    for content, expected in test_cases:
        print(f"\nTesting: {content[:50]}...")
        reports = validator.validate_all(content)

        status, conf = validator.get_overall_status(reports)
        print(f"  Status: {status.value} (confidence: {conf:.2f})")

        # Show any issues
        issues = [r for r in reports if r.result.value != 'valid']
        for issue in issues:
            print(f"    - {issue.check_name}: {issue.result.value}")


def demo_attack_examples():
    """Show examples of each attack type."""
    print("\n" + "=" * 60)
    print("DEMO 4: Attack Type Examples")
    print("=" * 60)

    from generators.content_generator import AdversarialStringGenerator

    adv = AdversarialStringGenerator(seed=13)
    base = "admin"

    attacks = [
        ("Original", lambda x: x),
        ("Homoglyph", lambda x: adv.homoglyph_attack(x, 1.0)),
        ("Invisible", lambda x: adv.invisible_attack(x, 3)),
        ("RTL", adv.rtl_attack),
        ("Case", lambda x: adv.case_attack(x, 'alternate')),
        ("Leet", lambda x: adv.leet_attack(x, 1.0)),
        ("Glitch", lambda x: adv.glitch_attack(x, 2)),
        ("Punycode", adv.punycode_attack),
        ("Emoji", lambda x: adv.emoji_attack(x, 0.5)),
    ]

    print(f"\nBase text: '{base}'")
    print("\nAttack variations:")

    for name, func in attacks:
        result = func(base)
        print(f"  {name:12}: {result}")
        print(f"               Length: {len(result)}, Bytes: {len(result.encode('utf-8'))}")


def main():
    """Run all demos."""
    print("🦀 Adversarial ML Testing Suite - Examples 🦀\n")

    demo_generation()
    demo_robustness_testing()
    demo_validation()
    demo_attack_examples()

    print("\n" + "=" * 60)
    print("All demos completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
