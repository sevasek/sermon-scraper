# Transcribe - transcribe.py
# Description

import whisper
from os import makedirs

def transcribe_using_whisper(model, sermon):

    # Safety check
    if not getattr(sermon, 'download_location', None):
        print(f"Skipping transcription for '{sermon.title}' - no download_location")
        return False
    
    try:
        print(f"Transcribing: {sermon.title}")

        # Transcribe the audio file
        result = model.transcribe(
                sermon.download_location,
                fp16=False,           # Force CPU-only
                language="en"         # Force English
            )

        sermon_uuid = sermon.download_location.removeprefix("audio/").removesuffix(".mp3")
        filename = f"text/{sermon_uuid}.txt"
    
        with open(filename, "w", encoding="utf-8") as f:
            f.write(result["text"])

        print(f"Transcription successful for {sermon.title} by {sermon.speaker}")
        sermon.transcript_location = filename

        return True
    
    except Exception as e:
        print(f"Transcription failed for {sermon.title}: {e}")
        return False

def transcribe_all(downloaded_sermons):
    
    model = whisper.load_model("tiny")
    makedirs("text", exist_ok=True)

    print(f"\n=== Before transcription ===")
    print(f"Total sermons: {len(downloaded_sermons)}")
    for i, s in enumerate(downloaded_sermons, 1):
        print(f"{i}. {s.title}")
        print(f"Download success: {getattr(s, 'download', False)}")
        print(f"Location: {getattr(s, 'download_location', 'MISSING')}")
        print("---")

    for s in downloaded_sermons:
        transcribe_using_whisper(model, s)
    return
    