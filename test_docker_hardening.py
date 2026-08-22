# Static-scan regression tests for Dockerfile/docker-compose.yml hardening
# (REVIEW.md finding 3, 2026-08-14 cybersecurity review) - test_docker_hardening.py
#
# These check the *files*, not a built image, since building one (Playwright
# + Whisper/torch) is too slow/heavy for a unit-test run.

import re
import unittest
from pathlib import Path

DOCKERFILE = Path(__file__).parent / "Dockerfile"
COMPOSE_FILE = Path(__file__).parent / "docker-compose.yml"


class DockerfileRunsAsNonRootTests(unittest.TestCase):
    def setUp(self):
        self.lines = DOCKERFILE.read_text().splitlines()

    def test_has_a_user_instruction(self):
        user_lines = [
            line for line in self.lines if re.match(r"^\s*USER\s+\S+", line)
        ]
        self.assertTrue(user_lines, "Dockerfile has no USER instruction")

    def test_user_instruction_is_not_root(self):
        user_lines = [
            line for line in self.lines if re.match(r"^\s*USER\s+\S+", line)
        ]
        for line in user_lines:
            user = line.split()[1].strip()
            self.assertNotIn(
                user, ("root", "0"), f"Dockerfile switches to root user: {line!r}"
            )

    def test_user_instruction_comes_after_the_last_chown(self):
        user_index = next(
            i for i, line in enumerate(self.lines) if re.match(r"^\s*USER\s+\S+", line)
        )
        chown_indices = [
            i for i, line in enumerate(self.lines) if "chown" in line
        ]
        self.assertTrue(chown_indices, "expected a chown before switching USER")
        self.assertGreater(
            user_index,
            max(chown_indices),
            "USER instruction should come after /app is chown'd to that user",
        )

    def test_caches_are_redirected_off_root_home(self):
        # Whisper/Playwright both cache under $HOME by default; if HOME is
        # never redirected off /root, the non-root user can't read what
        # got downloaded during the (root) build steps.
        content = "\n".join(self.lines)
        self.assertIn("HOME=", content)
        self.assertNotRegex(content, r"HOME=/root\b")


class ComposeDoesNotBindMountFullRepoTests(unittest.TestCase):
    def setUp(self):
        self.content = COMPOSE_FILE.read_text()

    def test_no_full_repo_bind_mount(self):
        # A bare `- .:/app` (or `- ./:/app`) hands the container read-write
        # access to the entire host checkout, not just the data dirs it
        # actually needs.
        pattern = re.compile(r"^\s*-\s*\.\/?:\S*/app\s*$", re.MULTILINE)
        self.assertIsNone(
            pattern.search(self.content),
            "docker-compose.yml still bind-mounts the full repo into the container",
        )

    def test_still_mounts_audio_and_text_dirs(self):
        self.assertIn("./audio:/app/audio", self.content)
        self.assertIn("./text:/app/text", self.content)


if __name__ == "__main__":
    unittest.main()
