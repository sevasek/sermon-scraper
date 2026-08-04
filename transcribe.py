# Transcribe - transcribe.py
# Description

from os import makedirs

# Supported OpenAI Whisper model sizes, smallest/fastest to largest/most accurate.
WHISPER_MODEL_SIZES = {"tiny", "base", "small", "medium", "large"}

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
        citation = f'\n{sermon.speaker}, "{sermon.title}", (sermon: EV Church, {sermon.location}, {sermon.date}), {sermon.url}.'

        with open(filename, "w", encoding="utf-8") as f:
            f.write(result["text"])
            f.write(citation)

        print(f"Transcription successful for {sermon.title} by {sermon.speaker}")
        sermon.transcript_location = filename

        return True
    
    except Exception as e:
        print(f"Transcription failed for {sermon.title}: {e}")
        return False

def transcribe_all(downloaded_sermons, model_size="tiny"):

    if model_size not in WHISPER_MODEL_SIZES:
        raise ValueError(f"Unknown Whisper model size '{model_size}'. Choose from: {sorted(WHISPER_MODEL_SIZES)}")

    import whisper  # Imported lazily - openai-whisper pulls in torch and is only needed here.

    print(f"Loading Whisper model: {model_size}")
    model = whisper.load_model(model_size)
    makedirs("text", exist_ok=True)

    print(f"Total sermons: {len(downloaded_sermons)}")
    for i, s in enumerate(downloaded_sermons, 1):
        print(f"{i}. {s.title}")
        print(f"Download success: {getattr(s, 'download', False)}")
        print(f"Location: {getattr(s, 'download_location', 'MISSING')}")
        print("---")

    for s in downloaded_sermons:
        transcribe_using_whisper(model, s)
    return
    