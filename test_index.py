# Tests for index.py - test_index.py
# Uses a temp SQLite file so it never touches the real sermon_index.db.

import os
import tempfile
import unittest

from index import init_db, get_indexed_urls, save_sermons, load_sermons_by_urls
from sermons import Sermon


class IndexTests(unittest.TestCase):
    def setUp(self):
        fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        init_db(self.db_path)

    def tearDown(self):
        os.remove(self.db_path)

    def test_save_and_load_round_trip(self):
        sermon = Sermon(
            url="https://evchurch.info/media/watch/?media=1",
            url_mp3="https://evchurch.info/audio/1.mp3",
            bible_passage="",
            title="Test Sermon",
            speaker="Jane Doe",
            location="Erina, NSW",
            date="1 January 2026",
            event="Sunday Service",
        )

        save_sermons([sermon], self.db_path)

        self.assertEqual(get_indexed_urls(self.db_path), {sermon.url})

        loaded = load_sermons_by_urls([sermon.url], self.db_path)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].url, sermon.url)
        self.assertEqual(loaded[0].title, sermon.title)
        self.assertEqual(loaded[0].speaker, sermon.speaker)

    def test_save_sermons_upserts_on_conflict(self):
        sermon = Sermon(
            url="https://evchurch.info/media/watch/?media=2",
            url_mp3="https://evchurch.info/audio/2.mp3",
            title="Original Title",
        )
        save_sermons([sermon], self.db_path)

        sermon.title = "Updated Title"
        save_sermons([sermon], self.db_path)

        loaded = load_sermons_by_urls([sermon.url], self.db_path)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].title, "Updated Title")

    def test_get_indexed_urls_empty_by_default(self):
        self.assertEqual(get_indexed_urls(self.db_path), set())

    def test_load_sermons_by_urls_empty_input(self):
        self.assertEqual(load_sermons_by_urls([], self.db_path), [])


if __name__ == "__main__":
    unittest.main()
