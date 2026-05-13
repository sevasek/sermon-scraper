# Sermons Class - sermons.py
# A dataclass for sermons is created after the scrape. A Sermon must contain the url of the page where the mp3 link was found, and the url of the mp3.

from dataclasses import dataclass


@dataclass
class Sermon:
    url: str
    url_mp3: str
    title: str = ""
    speaker: str = ""
    location: str = ""
    date: str = ""
    download: bool = False
    download_status: str = "Not attempted"
    download_location: str = ""
    
    def download()
        attempt_download = 0
        while attempt < 3:
            # Attempt to download the mp3 file from url_mp3 and save it to a local directory. If successful, set download to True and return. If unsuccessful, increment attempt and try again. If all 3 attempts fail, set download_status to "Failed after 3 attempts" and return.
            if attempt_download == True:
                self.download = True
                return
            else:
                attempt += 1
        self.download_status = "Failed after 3 attempts"
        return
    



        

    
    