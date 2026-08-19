# Tests for scraper.py's scrape_sermon_details() field-reset behavior - test_scraper.py
#
# Regression test for the bug fixed in 1ad43a0 ("fix: reset per-sermon fields
# before each detail scrape"): scrape_sermon_details() loops over a set of
# sermon page URLs, and each per-sermon field used to live only inside
# conditional branches, so a page missing the expected h2/h4 markup could
# silently inherit the previous sermon's title/speaker/date/event/passage
# instead of coming back empty. This mocks Playwright's page so both a
# "good" page and a page with none of that markup can be asserted
# independently of iteration order (the input is a Python set, so which URL
# is visited first is not guaranteed).

import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from scraper import scrape_sermon_details


def _fake_element(text):
    element = AsyncMock()
    element.inner_text = AsyncMock(return_value=text)
    element.text_content = AsyncMock(return_value=text)
    element.get_attribute = AsyncMock(return_value=None)
    return element


class _FakeAsyncPlaywright:
    """Minimal async-context-manager stand-in for playwright.async_api.async_playwright()."""

    def __init__(self, chromium):
        self._chromium = chromium

    async def __aenter__(self):
        return SimpleNamespace(chromium=self._chromium)

    async def __aexit__(self, *exc_info):
        return False


class ScrapeSermonDetailsFieldResetTests(unittest.TestCase):
    GOOD_URL = "https://evchurch.info/media/watch/?media=good"
    BARE_URL = "https://evchurch.info/media/watch/?media=bare"

    PAGES = {
        GOOD_URL: {
            "h2": _fake_element("Good Sermon Title"),
            "h4": [_fake_element("Genesis 1 | Sunday Service | 01/02/2026 | Jane Doe")],
        },
        BARE_URL: {
            "h2": None,
            "h4": [],
        },
    }

    def _build_mock_page(self):
        current = {}

        async def fake_goto(url, wait_until=None):
            current["url"] = url

        async def fake_query_selector(selector):
            if selector == "h2":
                return self.PAGES[current["url"]]["h2"]
            return None

        async def fake_query_selector_all(selector):
            if selector == "h4":
                return self.PAGES[current["url"]]["h4"]
            if selector == 'source[src$=".mp3"]':
                return []
            return []

        page = AsyncMock()
        page.goto = AsyncMock(side_effect=fake_goto)
        page.query_selector = AsyncMock(side_effect=fake_query_selector)
        page.query_selector_all = AsyncMock(side_effect=fake_query_selector_all)
        return page

    def _scrape(self, urls):
        mock_page = self._build_mock_page()

        mock_browser = AsyncMock()
        mock_browser.new_page = AsyncMock(return_value=mock_page)
        mock_browser.close = AsyncMock()

        mock_chromium = AsyncMock()
        mock_chromium.launch = AsyncMock(return_value=mock_browser)

        fake_playwright = lambda: _FakeAsyncPlaywright(mock_chromium)

        with patch("scraper.async_playwright", fake_playwright):
            return asyncio.run(scrape_sermon_details(urls))

    def test_fields_do_not_leak_between_sermons(self):
        sermons = self._scrape({self.GOOD_URL, self.BARE_URL})
        by_url = {sermon.url: sermon for sermon in sermons}

        good = by_url[self.GOOD_URL]
        bare = by_url[self.BARE_URL]

        self.assertEqual(good.title, "Good Sermon Title")
        self.assertEqual(good.event, "Sunday Service")
        self.assertEqual(good.speaker, "Jane Doe")
        self.assertEqual(good.date, "1 February 2026")
        self.assertTrue(good.bible_passage)

        # The bare page has none of the good page's h2/h4 markup - its fields
        # must come back empty regardless of which sermon was visited first,
        # not inherit the other sermon's title/speaker/date/event/passage.
        self.assertEqual(bare.title, "")
        self.assertEqual(bare.event, "")
        self.assertEqual(bare.speaker, "")
        self.assertEqual(bare.date, "")
        self.assertEqual(bare.bible_passage, "")

    def test_empty_input_returns_empty_list(self):
        self.assertEqual(asyncio.run(scrape_sermon_details(set())), [])


if __name__ == "__main__":
    unittest.main()
