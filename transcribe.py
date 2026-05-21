# Transcribe - transcribe.py
# Description

import whisper
from os import makedirs

def transcribe_using_whisper(model, sermon):

    # Transcribe the audio file
    result = model.transcribe(
            sermon.download_location,
            fp16=False,           # Force CPU-only
            language="en"         # Force English
        )

    result = model.transcribe(sermon.download_location)

    if not getattr(sermon, 'download_location', None):
        uuid = sermon.download_location.removeprefix("audio/").removesuffix(".mp3")
        filename = f"text/{uuid}.txt"
    
        with open(filename, "w") as f:
            f.write(result["text"])
        print(f"Transcription successful for {sermon.title} by {sermon.speaker}")
        self.transcript_location = filename

        return
    else:
        print("Transcription failed: download_location missing.")
        return

def transcribe(downloaded_sermons):
    
    model = whisper.load_model("tiny")
    makedirs("text", exist_ok=True)

    print("Time to transcribe...")

    for s in downloaded_sermons:
        transcribe_using_whisper(model, s)
    return
    