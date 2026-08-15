# Download - download.py

from uuid import uuid4
from os import makedirs
from urllib.parse import urlparse
import requests

import sermons

ALLOWED_MP3_HOST = "evchurch.info"

def is_allowed_mp3_url(url):
    # Only fetch mp3s from the trusted source host over https, so a
    # compromised/MITM'd/off-domain <source src=...> scraped from the page
    # can't turn this into an attacker-directed outbound fetch.
    parsed = urlparse(url)
    return parsed.scheme == "https" and parsed.hostname == ALLOWED_MP3_HOST

def download_mp3(sermon):
    if not is_allowed_mp3_url(sermon.url_mp3):
        print(f"Refusing to download from untrusted URL: {sermon.url_mp3}")
        sermon.download = False
        sermon.download_status = f"Refused: URL is not https://{ALLOWED_MP3_HOST}/..."
        return

    attempt_download = 0
    while attempt_download < 3:
        # Attempt to download the mp3 file from url_mp3 and save it to a local directory.
        try:
            # Download the mp3 file from url_mp3 and save it to a local directory goes here.
            makedirs("audio", exist_ok=True)
            filename = f"audio/{uuid4()}.mp3"
            response = requests.get(sermon.url_mp3, timeout=30)
            print(f"Starting download of {sermon.url_mp3}.")
            response.raise_for_status()

            # Success!
            with open(filename, "wb") as f:
                f.write(response.content)
            
            sermon.download = True
            sermon.download_status = "Success"
            sermon.download_location = filename
            print("Download complete!")
            return
        
        # Something went wrong, but I don't know what
        except Exception as e:
            print(f"Download attempt {attempt_download + 1} failed for {sermon.url_mp3}: {e}")
            attempt_download += 1
            
    sermon.download = False
    sermon.download_status = "Failed after 3 attempts"
    return

def download_mp3_update(sermon_objects):
    for sermon in sermon_objects:
        download_mp3(sermon)
    return sermon_objects