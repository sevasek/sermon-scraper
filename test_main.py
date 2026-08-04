# Tests for main.py's CLI argument parsing - test_main.py

import unittest

from main import parse_args
from transcribe import WHISPER_MODEL_SIZES


class ParseArgsTests(unittest.TestCase):
    def test_defaults_to_tiny_model(self):
        args = parse_args(["John 3:16"])
        self.assertEqual(args.bible_passage, "John 3:16")
        self.assertEqual(args.model, "tiny")

    def test_accepts_explicit_model_flag(self):
        args = parse_args(["John 3:16", "--model", "medium"])
        self.assertEqual(args.model, "medium")

    def test_rejects_unknown_model_size(self):
        with self.assertRaises(SystemExit):
            parse_args(["John 3:16", "--model", "huge"])

    def test_requires_bible_passage(self):
        with self.assertRaises(SystemExit):
            parse_args([])

    def test_all_documented_model_sizes_are_valid_choices(self):
        for size in WHISPER_MODEL_SIZES:
            args = parse_args(["John 3:16", "--model", size])
            self.assertEqual(args.model, size)


if __name__ == "__main__":
    unittest.main()
