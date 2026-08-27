# Tests that requirements.txt pins every dependency to an exact version - test_requirements.py

import re
import unittest
from pathlib import Path

REQUIREMENTS_PATH = Path(__file__).parent / "requirements.txt"


def _dependency_lines():
    lines = []
    for raw_line in REQUIREMENTS_PATH.read_text().splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if line:
            lines.append(line)
    return lines


class RequirementsArePinnedTests(unittest.TestCase):
    def test_every_dependency_has_an_exact_version_pin(self):
        unpinned = [line for line in _dependency_lines() if not re.search(r"==\d", line)]
        self.assertEqual(
            unpinned,
            [],
            f"requirements.txt has unpinned dependencies: {unpinned}",
        )

    def test_requirements_file_is_not_empty(self):
        self.assertTrue(_dependency_lines())


if __name__ == "__main__":
    unittest.main()
