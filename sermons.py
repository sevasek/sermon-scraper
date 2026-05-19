# Sermons Class - sermons.py
# A dataclass for sermons is created after the scrape. A Sermon must contain the url of the page where the mp3 link was found, and the url of the mp3.

from dataclasses import dataclass
from fileinput import filename
from urllib import response
from uuid import uuid4
import requests


@dataclass
class Sermon:
    url: str
    url_mp3: str
    bible_passage: str = ""
    title: str = ""
    speaker: str = ""
    location: str = ""
    date: str = ""
    download: bool = None
    download_status: str = "Not attempted"
    download_location: str = ""
    
    def download(self):
        attempt_download = 0
        while attempt_download < 3:
            # Attempt to download the mp3 file from url_mp3 and save it to a local directory.
            try:
                # Code to download the mp3 file from url_mp3 and save it to a local directory goes here.
                filename = f"audio/{uuid4()}.png"
                response = requests.get(self.url_mp3)

                # Ensure the request was successful (Status Code 200)
                if response.status_code == 200:
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    self.download = True
                    self.download_status = "Success"
                    print("Download complete!")
                else:
                    print(f"Error: Could not download file. Status code: {response.status_code}")
                    self.download = True
                    self.download_status = "Failed"
                return
            
            except Exception as e:
                print(f"Download attempt {attempt_download + 1} failed for {self.url_mp3}: {e}")
                attempt_download += 1
                
        self.download = False
        self.download_status = "Failed after 3 attempts"
        return
    



        

    
    