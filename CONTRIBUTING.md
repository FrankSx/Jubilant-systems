# Contributing to Adversarial ML Testing Suite

Thank you for your interest in contributing! 🦀

## How to Contribute

### Reporting Bugs

- Check if the bug has already been reported
- Include Python version and OS
- Provide minimal reproduction steps
- Include error messages and stack traces

### Suggesting Features

- Open an issue describing the feature
- Explain the use case
- Discuss implementation approach

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite (`make test`)
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

## Development Setup

```bash
git clone https://github.com/yourusername/adversarial-ml-tester.git
cd adversarial-ml-tester
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

## Code Style

- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions
- Keep functions focused and small
- Maximum line length: 127 characters

## Testing

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_suite.py -v

# Run with coverage
pytest --cov=. --cov-report=html
```

## Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and PRs where appropriate

## Security

- Never commit API keys or credentials
- Report security vulnerabilities privately
- Follow responsible disclosure

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions

## Questions?

- Open an issue for questions
- Join discussions in existing issues
- Check documentation first

🦀 Thank you for contributing to the 13th Hour!
