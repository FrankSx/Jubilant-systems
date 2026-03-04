# Adversarial ML Testing Suite 🦀

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![13th Hour](https://img.shields.io/badge/13th-Hour-red.svg)]()

> **Comprehensive testing framework for ML model robustness against adversarial content attacks**

```
╔══════════════════════════════════════════════════════════════════════════════╗
║     "Testing the boundaries so the boundaries don't break you"              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## 🚀 Quick Start

```bash
# Clone and install
git clone https://github.com/franksx/adversarial-ml-tester.git
cd adversarial-ml-tester
pip install -r requirements.txt

# Generate adversarial test content
python -m adversarial_ml_tester generate -c 1000 --verbose

# Test your model's robustness
python -m adversarial_ml_tester test -m http://your-model-api.com/predict

# Validate responses
python -m adversarial_ml_tester validate -i responses.json
```

## ✨ Features

### 9 Adversarial Attack Types

| Attack | Description | Example |
|--------|-------------|---------|
| **Homoglyph** | Cyrillic/Latin confusion | `аdmin` vs `admin` |
| **Invisible** | Zero-width characters | `user​name` |
| **ZWJ** | Zero-width joiner | `f‍r‍a‍n‍k` |
| **RTL** | Right-to-left override | `‮resu‭` |
| **Case** | Random case | `UsErNaMe` |
| **Leet** | 1337 speak | `4dm1n` |
| **Glitch** | Combining marks | `a̷d̷m̷i̷n̷` |
| **Punycode** | IDN homographs | `xn--admin-wmc` |
| **Emoji** | Emoji injection | `user🦀name` |

### 5 Validation Checks

- ✅ **PII Detection** - Identifies personal information leakage
- ✅ **Injection Detection** - XSS/script injection attempts
- ✅ **Encoding Validation** - Suspicious encoding detection
- ✅ **Prompt Leakage** - System prompt exposure detection
- ✅ **Consistency Check** - Output consistency verification

## 📊 Example Output

### Generated Profile
```json
{
  "username": "аdmin​istrator",
  "first_name": "Jоhn",
  "last_name": "Smіth", 
  "address": "123 Mаin St, New Yоrk",
  "description": "Hi, I'm Jоhn. I love cоding...",
  "attack_vectors": ["homoglyph", "invisible"],
  "byte_hash": "a3f9e2b8c1d4e5f6"
}
```

### Test Results
```
Total: 6 tests
✅ Passed: 4
❌ Failed: 1
⚠️  Warnings: 1
Average Score: 0.82

homoglyph_robustness: pass (score: 0.85)
invisible_character_handling: pass (score: 0.90)
case_sensitivity: warning (score: 0.60)
prompt_injection_resistance: fail (score: 0.45)
length_boundary_handling: pass (score: 0.95)
encoding_robustness: pass (score: 0.88)
```

## 🛠️ Installation

### From Source
```bash
git clone https://github.com/yourusername/adversarial-ml-tester.git
cd adversarial-ml-tester
pip install -r requirements.txt
```

### As Package
```bash
pip install -e .
```

## 📖 Usage

### CLI Commands

```bash
# Generate adversarial profiles
python -m adversarial_ml_tester generate -c 100 -o profiles.json

# Test model robustness
python -m adversarial_ml_tester test -m http://api.example.com/predict

# Validate responses  
python -m adversarial_ml_tester validate -i responses.json

# Fuzzing mode
python -m adversarial_ml_tester fuzz --verbose -o findings.json

# Generate report
python -m adversarial_ml_tester report -o report.json
```

### Python API

```python
from generators.content_generator import ContentGenerator
from adversarial.robustness_tester import RobustnessTester
from validators.response_validator import ContentValidator

# Generate content
gen = ContentGenerator(seed=42)
profile = gen.generate_profile()

# Test robustness
def my_model(text):
    return {"prediction": "class_1", "confidence": 0.95}

tester = RobustnessTester(my_model)
results = tester.run_full_suite("test input")

# Validate responses
validator = ContentValidator()
reports = validator.validate_all(model_output)
```

## 🧪 Testing

```bash
# Run unit tests
python tests/test_suite.py

# Run example demos
python scripts/examples.py

# Generate and test
python -m adversarial_ml_tester generate -c 100
python -m adversarial_ml_tester test
```

## 📁 Project Structure

```
adversarial_ml_tester/
├── generators/              # Content generation
│   └── content_generator.py
├── adversarial/             # Robustness testing  
│   └── robustness_tester.py
├── validators/              # Response validation
│   └── response_validator.py
├── tests/                   # Unit tests
│   └── test_suite.py
├── docs/                    # Documentation
│   ├── USAGE_GUIDE.md
│   └── ATTACK_REFERENCE.md
├── scripts/                 # Examples
│   └── examples.py
├── __main__.py             # CLI entry
├── README.md               # This file
├── requirements.txt        # Dependencies
├── setup.py               # Package setup
└── LICENSE                # MIT License
```

## 🔒 Safety & Ethics

**✅ Appropriate Use:**
- Testing your own ML models
- Security research with permission
- Educational purposes
- Improving model robustness

**❌ Inappropriate Use:**
- Attacking systems without authorization
- Generating harmful content
- Bypassing security controls
- Impersonating real users

## 📚 Documentation

- [Usage Guide](docs/USAGE_GUIDE.md) - Detailed usage instructions
- [Attack Reference](docs/ATTACK_REFERENCE.md) - Complete attack documentation
- [Package Summary](PACKAGE_SUMMARY.md) - Package overview

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 🦀 Acknowledgments

**13th Hour Productions**

> "Testing the boundaries so the boundaries don't break you"

---

**Note**: This tool is designed for defensive security testing. Use responsibly and only on systems you own or have explicit permission to test.
