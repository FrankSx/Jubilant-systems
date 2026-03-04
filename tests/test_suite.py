#!/usr/bin/env python3
"""
Unit tests for Adversarial ML Testing Suite
"""

import unittest
import json
import tempfile
import os
from pathlib import Path

# Add parent to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from generators.content_generator import (
    ContentGenerator, AdversarialStringGenerator, 
    UserProfile, AttackType
)
from adversarial.robustness_tester import RobustnessTester, BiasTester
from validators.response_validator import ContentValidator, ConsistencyTester


class TestAdversarialStringGenerator(unittest.TestCase):
    """Test adversarial string generation."""

    def setUp(self):
        self.gen = AdversarialStringGenerator(seed=13)

    def test_homoglyph_attack(self):
        """Test homoglyph substitution."""
        result = self.gen.homoglyph_attack("admin", probability=1.0)
        self.assertNotEqual(result, "admin")
        self.assertEqual(len(result), len("admin"))

    def test_invisible_attack(self):
        """Test invisible character insertion."""
        result = self.gen.invisible_attack("test", count=3)
        self.assertNotEqual(result, "test")
        self.assertGreater(len(result), len("test"))

    def test_rtl_attack(self):
        """Test RTL override."""
        result = self.gen.rtl_attack("user")
        self.assertIn('\u202e', result)
        self.assertIn('\u202c', result)

    def test_leet_attack(self):
        """Test leet speak conversion."""
        result = self.gen.leet_attack("hello", probability=1.0)
        self.assertIn('3', result)  # e -> 3
        self.assertIn('1', result)  # l -> 1


class TestContentGenerator(unittest.TestCase):
    """Test content generation."""

    def setUp(self):
        self.gen = ContentGenerator(seed=13)

    def test_generate_username(self):
        """Test username generation."""
        username = self.gen.generate_username("testuser")
        self.assertIsInstance(username, str)
        self.assertGreater(len(username), 0)

    def test_generate_profile(self):
        """Test complete profile generation."""
        profile = self.gen.generate_profile()
        self.assertIsInstance(profile, UserProfile)
        self.assertIsNotNone(profile.username)
        self.assertIsNotNone(profile.first_name)
        self.assertIsNotNone(profile.last_name)
        self.assertIsNotNone(profile.address)
        self.assertIsNotNone(profile.description)

    def test_profile_to_dict(self):
        """Test profile serialization."""
        profile = self.gen.generate_profile()
        data = profile.to_dict()
        self.assertIsInstance(data, dict)
        self.assertIn('username', data)
        self.assertIn('attack_vectors', data)


class TestContentValidator(unittest.TestCase):
    """Test content validation."""

    def setUp(self):
        self.validator = ContentValidator()

    def test_pii_detection(self):
        """Test PII detection."""
        report = self.validator.validate_pii("Contact me at test@example.com")
        self.assertEqual(report.check_name, "pii_detection")
        self.assertIn(report.result.value, ['invalid', 'suspicious'])

    def test_injection_detection(self):
        """Test injection detection."""
        report = self.validator.validate_injection("<script>alert(1)</script>")
        self.assertEqual(report.result.value, 'invalid')

    def test_valid_content(self):
        """Test validation of clean content."""
        report = self.validator.validate_pii("Hello world")
        self.assertEqual(report.result.value, 'valid')


class TestRobustnessTester(unittest.TestCase):
    """Test robustness testing framework."""

    def setUp(self):
        def mock_model(text):
            return {
                "prediction": f"class_{hash(text) % 5}",
                "confidence": 0.9
            }

        self.tester = RobustnessTester(mock_model)

    def test_homoglyph_robustness(self):
        """Test homoglyph robustness check."""
        result = self.tester.test_homoglyph_robustness("test", num_variants=5)
        self.assertEqual(result.name, "homoglyph_robustness")
        self.assertGreaterEqual(result.score, 0.0)
        self.assertLessEqual(result.score, 1.0)

    def test_case_sensitivity(self):
        """Test case sensitivity check."""
        result = self.tester.test_case_sensitivity("TestInput")
        self.assertEqual(result.name, "case_sensitivity")


class TestIntegration(unittest.TestCase):
    """Integration tests."""

    def test_end_to_end_generation(self):
        """Test complete generation and validation pipeline."""
        # Generate content
        gen = ContentGenerator(seed=42)
        profile = gen.generate_profile()

        # Validate content
        validator = ContentValidator()
        reports = validator.validate_all(profile.description)

        # Should have reports
        self.assertGreater(len(reports), 0)

        # Check overall status
        status, conf = validator.get_overall_status(reports)
        self.assertIn(status.value, ['valid', 'suspicious', 'invalid'])

    def test_json_serialization(self):
        """Test JSON serialization of all types."""
        gen = ContentGenerator(seed=42)
        profile = gen.generate_profile()

        # Should serialize without errors
        data = profile.to_dict()
        json_str = json.dumps(data)
        self.assertIsInstance(json_str, str)

        # Should deserialize
        restored = json.loads(json_str)
        self.assertEqual(restored['username'], data['username'])


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAdversarialStringGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestContentGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestContentValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestRobustnessTester))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
