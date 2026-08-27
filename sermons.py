# Sermons Class - sermons.py
# A dataclass for sermons is created after the scrape.
# A Sermon must contain the url of the page where the mp3 link was found, and the url of the mp3.

from dataclasses import dataclass

from pythonbible import NormalizedReference

@dataclass
class Sermon:
    url: str
    url_mp3: str
    # "" when no passage was found on the page; otherwise the list of
    # NormalizedReference objects scraper.py/index.py get back from
    # pythonbible.get_references(), consumed by filter.py's
    # get_verses_from_reference(). Never a populated plain str.
    bible_passage: str | list[NormalizedReference] = ""
    title: str = ""
    speaker: str = ""
    location: str = ""
    date: str = ""
    event: str = ""
    download: bool = None
    download_status: str = "Not attempted"
    download_location: str = ""
    transcript_location: str = ""