# Sermons Class - sermons.py
# A dataclass for sermons is created after the scrape. A Sermon must contain the url of the page where the mp3 link was found, and the url of the mp3.

from dataclasses import dataclass

@dataclass
class Sermon:
    url: str
    url_mp3: str
    bible_passage: str = ""
    title: str = ""
    speaker: str = ""
    location: str = ""
    date: str = ""
    event: str = ""
    download: bool = None
    download_status: str = "Not attempted"
    download_location: str = ""
    transcript_location: str = ""