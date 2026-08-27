# Tests for sermons.py's Sermon.bible_passage type - test_sermons.py
#
# Regression test for the REVIEW.md item flagged in 1ad43a0's review:
# Sermon.bible_passage was annotated `str`, but scraper.py and index.py both
# actually assign it pythonbible.get_references()'s return value (a
# list[NormalizedReference]) whenever a passage is found, only ever using a
# real string for the "no passage found" empty-string case. filter.py's
# get_verses_from_reference() relies on that list shape being iterable.

import typing
import unittest

import pythonbible as bible

from sermons import Sermon
from filter import get_verses_from_reference


class BiblePassageTypeTests(unittest.TestCase):
    def test_annotation_allows_list_of_normalized_reference(self):
        hints = typing.get_type_hints(Sermon)
        bible_passage_hint = hints["bible_passage"]
        args = typing.get_args(bible_passage_hint)

        self.assertIn(str, args)
        self.assertIn(list[bible.NormalizedReference], args)

    def test_populated_passage_round_trips_through_filter(self):
        references = bible.get_references("John 3:16")
        sermon = Sermon(
            url="https://evchurch.info/media/watch/?media=1",
            url_mp3="https://evchurch.info/audio/1.mp3",
            bible_passage=references,
        )

        verse_ids = get_verses_from_reference(sermon.bible_passage)

        self.assertTrue(verse_ids)

    def test_empty_passage_yields_no_verses(self):
        sermon = Sermon(
            url="https://evchurch.info/media/watch/?media=1",
            url_mp3="https://evchurch.info/audio/1.mp3",
            bible_passage="",
        )

        self.assertEqual(get_verses_from_reference(sermon.bible_passage), set())


if __name__ == "__main__":
    unittest.main()
