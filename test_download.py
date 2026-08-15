# Tests for download.py's mp3 URL allow-list - test_download.py

import unittest
from unittest.mock import patch

from download import download_mp3, is_allowed_mp3_url
from sermons import Sermon


class IsAllowedMp3UrlTests(unittest.TestCase):
    def test_accepts_https_evchurch_info(self):
        self.assertTrue(is_allowed_mp3_url("https://evchurch.info/sermons/a.mp3"))

    def test_rejects_http_scheme(self):
        self.assertFalse(is_allowed_mp3_url("http://evchurch.info/sermons/a.mp3"))

    def test_rejects_off_domain_host(self):
        self.assertFalse(is_allowed_mp3_url("https://evil.example.com/a.mp3"))

    def test_rejects_lookalike_subdomain(self):
        self.assertFalse(is_allowed_mp3_url("https://evchurch.info.evil.com/a.mp3"))

    def test_rejects_private_metadata_address(self):
        self.assertFalse(is_allowed_mp3_url("https://169.254.169.254/latest/meta-data/"))

    def test_rejects_malformed_url(self):
        self.assertFalse(is_allowed_mp3_url("not a url"))


class DownloadMp3RefusesUntrustedUrlTests(unittest.TestCase):
    @patch("download.requests.get")
    def test_does_not_call_requests_for_untrusted_host(self, mock_get):
        sermon = Sermon(url="https://evchurch.info/a", url_mp3="https://evil.example.com/a.mp3")

        download_mp3(sermon)

        mock_get.assert_not_called()
        self.assertFalse(sermon.download)
        self.assertIn("Refused", sermon.download_status)

    @patch("download.requests.get")
    def test_calls_requests_for_trusted_host(self, mock_get):
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.content = b"fake mp3 bytes"
        sermon = Sermon(url="https://evchurch.info/a", url_mp3="https://evchurch.info/a.mp3")

        with patch("download.open", create=True), patch("download.makedirs"):
            download_mp3(sermon)

        mock_get.assert_called_once()
        self.assertTrue(sermon.download)


if __name__ == "__main__":
    unittest.main()
