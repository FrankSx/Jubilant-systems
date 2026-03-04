#!/usr/bin/env python3
"""
Automated Report Generator
Generates comprehensive HTML/PDF reports from test results.

🦀 13th Hour Reporting Engine 🦀
"""

import json
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import statistics


class ReportGenerator:
    """Generate comprehensive test reports."""

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.data: Dict[str, Any] = {}

    def load_results(self, results_file: str) -> None:
        """Load test results from JSON file."""
        with open(results_file, 'r') as f:
            self.data = json.load(f)

    def generate_html_report(self, filename: str = "report.html") -> str:
        """Generate HTML report with styling."""

        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Adversarial ML Test Report</title>
    <style>
        :root {{
            --primary: #2c3e50;
            --secondary: #e74c3c;
            --success: #27ae60;
            --warning: #f39c12;
            --info: #3498db;
            --bg: #ecf0f1;
            --card: #ffffff;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--primary);
            line-height: 1.6;
        }}

        .header {{
            background: linear-gradient(135deg, var(--primary) 0%, #34495e 100%);
            color: white;
            padding: 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}

        .header::before {{
            content: "🦀";
            position: absolute;
            font-size: 8rem;
            opacity: 0.1;
            right: -1rem;
            top: -1rem;
        }}

        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}

        .header .subtitle {{
            opacity: 0.9;
            font-size: 1.1rem;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}

        .card {{
            background: var(--card);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}

        .card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.15);
        }}

        .card h3 {{
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #7f8c8d;
            margin-bottom: 0.5rem;
        }}

        .card .value {{
            font-size: 2.5rem;
            font-weight: bold;
            color: var(--primary);
        }}

        .card .value.success {{ color: var(--success); }}
        .card .value.warning {{ color: var(--warning); }}
        .card .value.danger {{ color: var(--secondary); }}

        .section {{
            background: var(--card);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .section h2 {{
            font-size: 1.5rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--bg);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }}

        th, td {{
            text-align: left;
            padding: 0.75rem;
            border-bottom: 1px solid #ecf0f1;
        }}

        th {{
            font-weight: 600;
            color: #7f8c8d;
            font-size: 0.85rem;
            text-transform: uppercase;
        }}

        tr:hover {{
            background: #f8f9fa;
        }}

        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }}

        .badge.success {{
            background: #d4edda;
            color: #155724;
        }}

        .badge.warning {{
            background: #fff3cd;
            color: #856404;
        }}

        .badge.danger {{
            background: #f8d7da;
            color: #721c24;
        }}

        .progress-bar {{
            width: 100%;
            height: 8px;
            background: #ecf0f1;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 0.5rem;
        }}

        .progress-fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 0.3s ease;
        }}

        .progress-fill.success {{ background: var(--success); }}
        .progress-fill.warning {{ background: var(--warning); }}
        .progress-fill.danger {{ background: var(--secondary); }}

        .footer {{
            text-align: center;
            padding: 2rem;
            color: #7f8c8d;
            font-size: 0.9rem;
        }}

        .attack-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}

        .attack-item {{
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid var(--info);
        }}

        .attack-item.covered {{
            border-left-color: var(--success);
        }}

        .attack-item.pending {{
            border-left-color: var(--warning);
        }}

        @media print {{
            .header {{ background: var(--primary) !important; -webkit-print-color-adjust: exact; }}
            .card {{ break-inside: avoid; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🦀 Adversarial ML Test Report</h1>
        <p class="subtitle">13th Hour Testing Suite • Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>

    <div class="container">
        <!-- Summary Cards -->
        <div class="summary-cards">
            <div class="card">
                <h3>Total Tests</h3>
                <div class="value">{self.data.get('total_tests', 0)}</div>
            </div>
            <div class="card">
                <h3>Passed</h3>
                <div class="value success">{self.data.get('passed', 0)}</div>
            </div>
            <div class="card">
                <h3>Failed</h3>
                <div class="value danger">{self.data.get('failed', 0)}</div>
            </div>
            <div class="card">
                <h3>Average Score</h3>
                <div class="value {self._score_class(self.data.get('average_score', 0))}">
                    {self.data.get('average_score', 0):.2f}
                </div>
            </div>
        </div>

        <!-- Test Results -->
        <div class="section">
            <h2>Test Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>Test Name</th>
                        <th>Result</th>
                        <th>Score</th>
                        <th>Progress</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_test_rows()}
                </tbody>
            </table>
        </div>

        <!-- Attack Coverage -->
        <div class="section">
            <h2>Attack Coverage</h2>
            <div class="attack-grid">
                {self._generate_attack_coverage()}
            </div>
        </div>

        <!-- Recommendations -->
        <div class="section">
            <h2>Recommendations</h2>
            <ul>
                {self._generate_recommendations()}
            </ul>
        </div>
    </div>

    <div class="footer">
        <p>🦀 13th Hour Productions • Adversarial ML Testing Suite</p>
        <p>"Testing the boundaries so the boundaries don't break you"</p>
    </div>
</body>
</html>
"""

        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        return str(output_path)

    def _score_class(self, score: float) -> str:
        """Determine CSS class for score."""
        if score >= 0.8:
            return "success"
        elif score >= 0.6:
            return "warning"
        else:
            return "danger"

    def _generate_test_rows(self) -> str:
        """Generate HTML table rows for tests."""
        tests = self.data.get('tests', [])
        rows = []

        for test in tests:
            result_class = test.get('result', 'unknown')
            score = test.get('score', 0)

            badge_class = {
                'pass': 'success',
                'fail': 'danger',
                'warning': 'warning'
            }.get(result_class, 'warning')

            progress_class = self._score_class(score)

            row = f"""
            <tr>
                <td>{test.get('name', 'Unknown')}</td>
                <td><span class="badge {badge_class}">{result_class.upper()}</span></td>
                <td>{score:.2f}</td>
                <td>
                    <div class="progress-bar">
                        <div class="progress-fill {progress_class}" style="width: {score*100}%"></div>
                    </div>
                </td>
            </tr>
            """
            rows.append(row)

        return ''.join(rows) if rows else '<tr><td colspan="4">No test data available</td></tr>'

    def _generate_attack_coverage(self) -> str:
        """Generate attack coverage HTML."""
        coverage = self.data.get('attack_coverage', {})
        items = []

        for attack, status in coverage.items():
            status_class = 'covered' if status == 'implemented' else 'pending'
            icon = '✓' if status == 'implemented' else '○'

            item = f"""
            <div class="attack-item {status_class}">
                <strong>{icon} {attack.replace('_', ' ').title()}</strong>
                <br><small>{status}</small>
            </div>
            """
            items.append(item)

        return ''.join(items) if items else '<p>No attack coverage data</p>'

    def _generate_recommendations(self) -> str:
        """Generate recommendations HTML."""
        recommendations = self.data.get('recommendations', [])

        if not recommendations:
            return '<li>No specific recommendations at this time.</li>'

        return ''.join(f'<li>{rec}</li>' for rec in recommendations)

    def generate_json_report(self, filename: str = "report.json") -> str:
        """Generate JSON report."""
        report = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "1.0.0-13thHour",
                "tool": "Adversarial ML Testing Suite"
            },
            "summary": {
                "total_tests": self.data.get('total_tests', 0),
                "passed": self.data.get('passed', 0),
                "failed": self.data.get('failed', 0),
                "warnings": self.data.get('warnings', 0),
                "average_score": self.data.get('average_score', 0.0)
            },
            "tests": self.data.get('tests', []),
            "attack_coverage": self.data.get('attack_coverage', {}),
            "recommendations": self.data.get('recommendations', [])
        }

        output_path = self.output_dir / filename
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        return str(output_path)

    def generate_markdown_report(self, filename: str = "report.md") -> str:
        """Generate Markdown report."""

        md = f"""# Adversarial ML Test Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Tool:** 13th Hour Testing Suite v1.0.0

## Summary

| Metric | Value |
|--------|-------|
| Total Tests | {self.data.get('total_tests', 0)} |
| Passed | {self.data.get('passed', 0)} ✅ |
| Failed | {self.data.get('failed', 0)} ❌ |
| Warnings | {self.data.get('warnings', 0)} ⚠️ |
| Average Score | {self.data.get('average_score', 0):.2f} |

## Test Results

| Test | Result | Score |
|------|--------|-------|
"""

        for test in self.data.get('tests', []):
            icon = '✅' if test.get('result') == 'pass' else '❌' if test.get('result') == 'fail' else '⚠️'
            md += f"| {test.get('name')} | {icon} {test.get('result')} | {test.get('score', 0):.2f} |\n"

        md += "\n## Attack Coverage\n\n"

        for attack, status in self.data.get('attack_coverage', {}).items():
            icon = '✅' if status == 'implemented' else '⏳'
            md += f"- {icon} **{attack.replace('_', ' ').title()}**: {status}\n"

        md += "\n## Recommendations\n\n"

        for i, rec in enumerate(self.data.get('recommendations', []), 1):
            md += f"{i}. {rec}\n"

        md += "\n---\n\n🦀 *13th Hour Productions*"

        output_path = self.output_dir / filename
        with open(output_path, 'w') as f:
            f.write(md)

        return str(output_path)

    def generate_all(self, base_name: str = "report") -> Dict[str, str]:
        """Generate all report formats."""
        return {
            "html": self.generate_html_report(f"{base_name}.html"),
            "json": self.generate_json_report(f"{base_name}.json"),
            "markdown": self.generate_markdown_report(f"{base_name}.md")
        }


if __name__ == "__main__":
    # Demo with sample data
    sample_data = {
        "total_tests": 6,
        "passed": 4,
        "failed": 1,
        "warnings": 1,
        "average_score": 0.82,
        "tests": [
            {"name": "homoglyph_robustness", "result": "pass", "score": 0.85},
            {"name": "invisible_character_handling", "result": "pass", "score": 0.90},
            {"name": "case_sensitivity", "result": "warning", "score": 0.60},
            {"name": "prompt_injection_resistance", "result": "fail", "score": 0.45},
            {"name": "length_boundary_handling", "result": "pass", "score": 0.95},
            {"name": "encoding_robustness", "result": "pass", "score": 0.88}
        ],
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
        "recommendations": [
            "Implement rate limiting on model endpoints",
            "Add input normalization pipeline",
            "Deploy output filtering for PII",
            "Monitor for homoglyph attacks in usernames",
            "Validate all encodings before processing"
        ]
    }

    gen = ReportGenerator()
    gen.data = sample_data

    reports = gen.generate_all("demo_report")

    print("🦀 Report Generation Demo 🦀\n")
    print("Generated reports:")
    for fmt, path in reports.items():
        print(f"  {fmt.upper()}: {path}")
