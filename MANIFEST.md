# Adversarial ML Testing Suite - File Manifest

## Package Contents

### Core Python Modules (18 files)

| File | Lines | Purpose |
|------|-------|---------|
| `__init__.py` | 7 | Package initialization |
| `__main__.py` | 350 | CLI entry point |
| `generators/__init__.py` | 7 | Generators package init |
| `generators/content_generator.py` | 450 | Main content generation engine |
| `adversarial/__init__.py` | 7 | Adversarial package init |
| `adversarial/robustness_tester.py` | 420 | Model robustness testing |
| `adversarial/multimodal_tester.py` | 380 | Multi-modal (text+image) testing |
| `adversarial/fuzzing_engine.py` | 580 | Advanced fuzzing engine |
| `validators/__init__.py` | 7 | Validators package init |
| `validators/response_validator.py` | 380 | Response validation |
| `tests/__init__.py` | 7 | Tests package init |
| `tests/test_suite.py` | 280 | Unit tests |
| `reports/__init__.py` | 7 | Reports package init |
| `reports/report_generator.py` | 420 | HTML/JSON/Markdown report generation |
| `scripts/__init__.py` | 7 | Scripts package init |
| `scripts/examples.py` | 280 | Usage examples and demos |
| `data/__init__.py` | 7 | Data package init |

**Total Python Code: ~3,500 lines**

### Documentation (5 files)

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation |
| `PACKAGE_SUMMARY.md` | Package overview and quick start |
| `docs/USAGE_GUIDE.md` | Detailed usage instructions |
| `docs/ATTACK_REFERENCE.md` | Complete attack documentation |
| `CONTRIBUTING.md` | Contribution guidelines |

### Configuration (6 files)

| File | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | GitHub Actions CI/CD |
| `.pre-commit-config.yaml` | Pre-commit hooks |
| `Dockerfile` | Docker container definition |
| `docker-compose.yml` | Docker Compose services |
| `Makefile` | Build automation |
| `data/config.json` | Suite configuration |

### Data & Assets (2 files)

| File | Purpose |
|------|---------|
| `data/seed_corpus.txt` | Fuzzing seed corpus |
| `requirements.txt` | Python dependencies |

### Project Files (3 files)

| File | Purpose |
|------|---------|
| `setup.py` | Package installation |
| `LICENSE` | MIT License |
| `.gitignore` | Git ignore patterns |

## Architecture Overview

```
adversarial_ml_tester/
├── Core Package
│   ├── __init__.py
│   ├── __main__.py (CLI)
│   └── generators/
│       └── content_generator.py
├── Testing Modules
│   ├── adversarial/
│   │   ├── robustness_tester.py
│   │   ├── multimodal_tester.py
│   │   └── fuzzing_engine.py
│   └── validators/
│       └── response_validator.py
├── Quality Assurance
│   ├── tests/
│   │   └── test_suite.py
│   └── reports/
│       └── report_generator.py
├── Documentation
│   ├── README.md
│   ├── docs/
│   │   ├── USAGE_GUIDE.md
│   │   └── ATTACK_REFERENCE.md
│   └── CONTRIBUTING.md
├── Deployment
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── .github/workflows/ci.yml
│   └── Makefile
└── Configuration
    ├── setup.py
    ├── requirements.txt
    └── data/
        ├── config.json
        └── seed_corpus.txt
```

## Attack Coverage

### Implemented Attacks (9)

1. **Homoglyph** - Cyrillic/Latin confusion
2. **Invisible** - Zero-width characters
3. **ZWJ** - Zero-width joiner
4. **RTL** - Right-to-left override
5. **Case** - Random case variation
6. **Leet** - 1337 speak
7. **Glitch** - Combining diacriticals
8. **Punycode** - IDN homographs
9. **Emoji** - Emoji injection

### Mutation Strategies (6)

1. **Bit Flip** - Bit-level mutations
2. **Byte Insertion** - Insert problematic bytes
3. **Unicode** - Problematic Unicode chars
4. **Format String** - Format specifiers
5. **Length** - Length boundary testing
6. **Grammar** - Structure corruption

## Testing Capabilities

### Content Generation
- ✅ User profiles (username, name, address, description)
- ✅ Profile picture prompts
- ✅ Deterministic generation with seeds
- ✅ Batch generation (up to 100K profiles)

### Robustness Testing
- ✅ Homoglyph resistance
- ✅ Invisible character handling
- ✅ Case sensitivity
- ✅ Length boundaries
- ✅ Prompt injection
- ✅ Encoding robustness

### Validation
- ✅ PII detection
- ✅ Injection detection
- ✅ Encoding validation
- ✅ Prompt leakage
- ✅ Consistency checking

### Multi-Modal
- ✅ Text + image testing
- ✅ Cross-modal attacks
- ✅ Modality confusion

### Fuzzing
- ✅ Coverage-guided fuzzing
- ✅ Multiple mutation strategies
- ✅ Crash detection
- ✅ Corpus management

## CI/CD Integration

### GitHub Actions
- Python 3.8, 3.9, 3.10, 3.11 testing
- Automated linting (flake8)
- Security scanning (bandit)
- Coverage reporting (codecov)
- Docker image building

### Docker
- Multi-stage builds
- Docker Compose services
- Volume mounting for outputs
- Health checks

### Local Development
- Makefile for common tasks
- Pre-commit hooks
- Virtual environment support
- Live reloading

## Usage Statistics

- **Generation Speed**: ~1,000 profiles/second
- **Testing Speed**: ~10 tests/second (with API)
- **Validation Speed**: ~1,000 responses/second
- **Fuzzing Speed**: Configurable (default: max)

## Version Information

- **Version**: 1.0.0-13thHour
- **Python**: 3.8+
- **License**: MIT
- **Author**: frankSx / 13th Hour Productions

## Security Considerations

This tool is designed for:
- Defensive security testing
- Authorized penetration testing
- Educational purposes
- Model robustness improvement

Not for:
- Unauthorized system access
- Harmful content generation
- Bypassing security controls
- Production data manipulation

## Support

- Documentation: `docs/` directory
- Examples: `scripts/examples.py`
- Tests: `tests/test_suite.py`
- Issues: GitHub Issues

---

🦀 **13th Hour Productions**

"Testing the boundaries so the boundaries don't break you"
