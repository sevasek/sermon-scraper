# Download - download.py
# A function to download the mp3 files for each sermon in the sermons list. The function will attempt to download the mp3 file from the url_mp3 attribute of the Sermon object and save it to a local directory. 
# The function will also update the download, download_status, and download_location attributes of the Sermon object based on the success or failure of the download attempt. 
# The function will attempt to download the file up to 3 times before giving up and marking the download as failed.

from fileinput import filename
from urllib import response
from uuid import uuid4
import requests

import sermons

def download_mp3(sermon):
    attempt_download = 0
    while attempt_download < 3:
        # Attempt to download the mp3 file from url_mp3 and save it to a local directory.
        try:
            # Code to download the mp3 file from url_mp3 and save it to a local directory goes here.
            filename = f"audio/{uuid4()}.png"
            response = requests.get(sermon.url_mp3)

            # Ensure the request was successful (Status Code 200)
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
                sermon.download = True
                sermon.download_status = "Success"
                print("Download complete!")
            else:
                print(f"Error: Could not download file. Status code: {response.status_code}")
                sermon.download = True
                sermon.download_status = "Failed"
            return
        
        except Exception as e:
            print(f"Download attempt {attempt_download + 1} failed for {sermon.url_mp3}: {e}")
            attempt_download += 1
            
    sermon.download = False
    sermon.download_status = "Failed after 3 attempts"
    return

for sermon in sermons:
    download_mp3(sermon)