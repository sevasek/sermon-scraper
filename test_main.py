# Tests for main.py's CLI argument parsing - test_main.py

import unittest

from main import _successfully_parsed, parse_args
from sermons import Sermon
from transcribe import WHISPER_MODEL_SIZES


class SuccessfullyParsedTests(unittest.TestCase):
    def test_keeps_sermons_with_a_parsed_date(self):
        sermon = Sermon(url="https://evchurch.info/a", url_mp3="a.mp3", date="1 January 2026")
        self.assertEqual(_successfully_parsed([sermon]), [sermon])

    def test_drops_sermons_with_no_parsed_date(self):
        good = Sermon(url="https://evchurch.info/a", url_mp3="a.mp3", date="1 January 2026")
        failed = Sermon(url="https://evchurch.info/b", url_mp3="b.mp3", date="")
        self.assertEqual(_successfully_parsed([good, failed]), [good])

    def test_empty_input(self):
        self.assertEqual(_successfully_parsed([]), [])


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
