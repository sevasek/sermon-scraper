# Download - download.py

from uuid import uuid4
from os import makedirs
import requests

import sermons

def download_mp3(sermon):
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