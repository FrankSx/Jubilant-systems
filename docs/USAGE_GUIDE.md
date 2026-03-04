# Usage Guide

## Command Line Interface

### Generate Command

Generate synthetic adversarial user profiles:

```bash
python -m adversarial_ml_tester generate [options]
```

Options:
- `--count, -c`: Number of profiles to generate (default: 100)
- `--output, -o`: Output file path (default: output/profiles.json)
- `--seed, -s`: Random seed for reproducibility
- `--attack-prob, -a`: Probability of applying attacks (default: 0.7)
- `--verbose, -v`: Show detailed output

Examples:

```bash
# Generate 1000 profiles with attacks
python -m adversarial_ml_tester generate -c 1000 -o profiles.json

# Generate with specific seed for reproducibility
python -m adversarial_ml_tester generate -c 100 -s 42 --verbose

# Generate clean profiles (no attacks)
python -m adversarial_ml_tester generate -c 50 -a 0.0 -o clean_profiles.json
```

### Test Command

Run adversarial robustness tests against a model:

```bash
python -m adversarial_ml_tester test [options]
```

Options:
- `--model-url, -m`: Model API endpoint URL
- `--test-text, -t`: Text to use for testing (default: "Test input")
- `--output, -o`: Output report file

Examples:

```bash
# Test against local API
python -m adversarial_ml_tester test -m http://localhost:8000/predict

# Test with custom text
python -m adversarial_ml_tester test -m http://api.example.com/predict -t "Hello World"

# Save report
python -m adversarial_ml_tester test -m http://api.example.com/predict -o report.json
```

### Validate Command

Validate model responses for safety issues:

```bash
python -m adversarial_ml_tester validate [options]
```

Options:
- `--input, -i`: Input file containing responses to validate

Examples:

```bash
# Validate responses from file
python -m adversarial_ml_tester validate -i responses.json

# Interactive mode (validate built-in examples)
python -m adversarial_ml_tester validate
```

### Fuzz Command

Continuous fuzzing mode for finding edge cases:

```bash
python -m adversarial_ml_tester fuzz [options]
```

Options:
- `--output, -o`: Output file for findings (default: output/findings.json)
- `--verbose, -v`: Show each finding immediately

Examples:

```bash
# Run fuzzing with verbose output
python -m adversarial_ml_tester fuzz --verbose

# Run and save findings
python -m adversarial_ml_tester fuzz -o my_findings.json
```

Press Ctrl+C to stop fuzzing.

### Report Command

Generate comprehensive test report:

```bash
python -m adversarial_ml_tester report [options]
```

Options:
- `--output, -o`: Output file (default: output/report.json)

## Python API

### Content Generation

```python
from generators.content_generator import ContentGenerator, AttackType

# Initialize generator
gen = ContentGenerator(seed=42)

# Generate single profile
profile = gen.generate_profile()
print(profile.username)
print(profile.description)

# Generate with specific attacks
profile = gen.generate_profile(attack_probability=1.0)
print([a.value for a in profile.attack_vectors])

# Generate specific components
username = gen.generate_username("base_name", attacks=[AttackType.HOMOGLYPH])
first, last = gen.generate_name(attacks=[AttackType.INVISIBLE])
address = gen.generate_address()
desc = gen.generate_description("John", "New York")
```

### Adversarial Testing

```python
from adversarial.robustness_tester import RobustnessTester

# Define your model interface
def my_model(text: str) -> dict:
    # Your model inference here
    return {
        "prediction": predicted_class,
        "confidence": confidence_score,
        "latency": processing_time
    }

# Create tester
tester = RobustnessTester(my_model)

# Run individual tests
result = tester.test_homoglyph_robustness("test text")
result = tester.test_invisible_character_filtering("test text")
result = tester.test_prompt_injection("test text")

# Run full suite
results = tester.run_full_suite("test text")
print(f"Average score: {results['average_score']}")
```

### Response Validation

```python
from validators.response_validator import ContentValidator

validator = ContentValidator()

# Validate single response
reports = validator.validate_all("Model response text")

# Check overall status
status, confidence = validator.get_overall_status(reports)
print(f"Status: {status.value}, Confidence: {confidence}")

# Individual checks
pii_report = validator.validate_pii("text with email@example.com")
injection_report = validator.validate_injection("<script>alert(1)</script>")
```

## Attack Types Reference

### Homoglyph Attack
Replaces characters with visually similar Unicode characters.

```python
from generators.content_generator import AdversarialStringGenerator

adv = AdversarialStringGenerator()
result = adv.homoglyph_attack("admin", probability=0.5)
# Result might be: "аdmin" (Cyrillic 'а')
```

### Invisible Character Attack
Inserts zero-width characters.

```python
result = adv.invisible_attack("username", count=3)
# Result: "user​name" (with zero-width spaces)
```

### RTL Override Attack
Wraps text in right-to-left override characters.

```python
result = adv.rtl_attack("user")
# Result: "‮resu‭" (displays as reversed)
```

### Glitch Attack
Adds combining diacritical marks.

```python
result = adv.glitch_attack("text", intensity=3)
# Result: "t̷e̷x̷t̷" (with overlay marks)
```

## Integration Examples

### Testing a REST API

```python
import requests
from adversarial.robustness_tester import RobustnessTester

def api_model(text: str) -> dict:
    response = requests.post(
        "http://api.example.com/predict",
        json={"text": text},
        timeout=10
    )
    data = response.json()
    return {
        "prediction": data["class"],
        "confidence": data["confidence"],
        "latency": response.elapsed.total_seconds()
    }

tester = RobustnessTester(api_model)
results = tester.run_full_suite("Test input")
```

### Batch Processing

```python
from generators.content_generator import ContentGenerator
import json

gen = ContentGenerator(seed=13)

# Generate batch
profiles = [gen.generate_profile() for _ in range(100)]

# Process through your model
results = []
for profile in profiles:
    prediction = my_model.predict(profile.description)
    results.append({
        "profile": profile.to_dict(),
        "prediction": prediction
    })

# Save results
with open("batch_results.json", "w") as f:
    json.dump(results, f, indent=2)
```

### CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Adversarial Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -e .

      - name: Run unit tests
        run: python tests/test_suite.py

      - name: Generate test profiles
        run: python -m adversarial_ml_tester generate -c 100 -o test_profiles.json

      - name: Test model robustness
        run: python -m adversarial_ml_tester test -m http://localhost:8000/predict
```

## Troubleshooting

### Issue: UnicodeEncodeError

**Solution**: Ensure your terminal supports UTF-8:

```bash
export PYTHONIOENCODING=utf-8
python -m adversarial_ml_tester generate
```

### Issue: Model API timeouts

**Solution**: Increase timeout in your model interface or use batch processing.

### Issue: Memory errors with large batches

**Solution**: Process in chunks:

```python
for i in range(0, total, chunk_size):
    chunk = profiles[i:i+chunk_size]
    process_chunk(chunk)
```

## Advanced Configuration

### Custom Attack Patterns

```python
from generators.content_generator import AdversarialStringGenerator

class CustomGenerator(AdversarialStringGenerator):
    def custom_attack(self, text: str) -> str:
        # Your custom transformation
        return transformed_text
```

### Custom Validation Rules

```python
from validators.response_validator import ContentValidator

custom_rules = [
    {
        "name": "custom_check",
        "pattern": r"suspicious_pattern",
        "severity": "high"
    }
]

validator = ContentValidator(custom_rules=custom_rules)
```

## Performance Tips

1. **Use seeds for reproducibility**: Always set a seed when debugging
2. **Batch API calls**: Reduce latency by batching requests
3. **Cache results**: Save generated profiles for reuse
4. **Parallel processing**: Use multiprocessing for large batches
5. **Filter early**: Validate before expensive model calls

## Security Considerations

- Never run tests against production systems without approval
- Generated content may bypass filters - use responsibly
- Store test data securely
- Validate all inputs to the testing framework itself
- Monitor resource usage during fuzzing

## Getting Help

- GitHub Issues: Report bugs and feature requests
- Documentation: Check docs/ directory
- Examples: See scripts/ directory for example usage
