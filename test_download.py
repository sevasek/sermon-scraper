# Tests for download.py's mp3 URL allow-list and size cap - test_download.py

import unittest
from unittest.mock import patch, MagicMock

from download import MAX_MP3_BYTES, download_mp3, is_allowed_mp3_url
from sermons import Sermon


def _mock_response(headers=None, chunks=(b"fake mp3 bytes",)):
    response = MagicMock()
    response.raise_for_status.return_value = None
    response.headers = headers or {}
    response.iter_content.return_value = list(chunks)
    return response


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
        mock_get.return_value = _mock_response()
        sermon = Sermon(url="https://evchurch.info/a", url_mp3="https://evchurch.info/a.mp3")

        with patch("download.open", create=True), patch("download.makedirs"):
            download_mp3(sermon)

        mock_get.assert_called_once()
        self.assertEqual(mock_get.call_args.kwargs.get("stream"), True)
        self.assertTrue(sermon.download)


class DownloadMp3SizeCapTests(unittest.TestCase):
    @patch("download.remove")
    @patch("download.exists", return_value=True)
    @patch("download.requests.get")
    def test_refuses_when_content_length_exceeds_cap(self, mock_get, mock_exists, mock_remove):
        mock_get.return_value = _mock_response(
            headers={"Content-Length": str(MAX_MP3_BYTES + 1)}
        )
        sermon = Sermon(url="https://evchurch.info/a", url_mp3="https://evchurch.info/a.mp3")

        with patch("download.open", create=True) as mock_open, patch("download.makedirs"):
            download_mp3(sermon)

        # Rejected before any body chunk is written.
        mock_open.return_value.__enter__.return_value.write.assert_not_called()
        self.assertEqual(mock_get.call_count, 3)
        self.assertFalse(sermon.download)
        self.assertEqual(sermon.download_status, "Failed after 3 attempts")
        self.assertEqual(mock_remove.call_count, 3)

    @patch("download.remove")
    @patch("download.exists", return_value=True)
    @patch("download.requests.get")
    def test_aborts_streamed_download_that_exceeds_cap(self, mock_get, mock_exists, mock_remove):
        # No (or an understated) Content-Length, but the streamed body itself
        # exceeds the cap - the oversized chunk must never be written to disk.
        oversized_chunk = b"x" * (MAX_MP3_BYTES + 1)
        mock_get.return_value = _mock_response(headers={}, chunks=(oversized_chunk,))
        sermon = Sermon(url="https://evchurch.info/a", url_mp3="https://evchurch.info/a.mp3")

        with patch("download.open", create=True) as mock_open, patch("download.makedirs"):
            download_mp3(sermon)

        mock_open.return_value.__enter__.return_value.write.assert_not_called()
        self.assertFalse(sermon.download)
        self.assertEqual(sermon.download_status, "Failed after 3 attempts")

    @patch("download.remove")
    @patch("download.exists", return_value=True)
    @patch("download.requests.get")
    def test_allows_download_under_the_cap(self, mock_get, mock_exists, mock_remove):
        mock_get.return_value = _mock_response(
            headers={"Content-Length": "14"}, chunks=(b"fake mp3 bytes",)
        )
        sermon = Sermon(url="https://evchurch.info/a", url_mp3="https://evchurch.info/a.mp3")

        with patch("download.open", create=True) as mock_open, patch("download.makedirs"):
            download_mp3(sermon)

        mock_open.return_value.__enter__.return_value.write.assert_called_once_with(
            b"fake mp3 bytes"
        )
        self.assertTrue(sermon.download)
        mock_remove.assert_not_called()


if __name__ == "__main__":
    unittest.main()
