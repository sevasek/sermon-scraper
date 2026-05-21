# EV Church Sermon Transcriber

**A tool to find, download, and transcribe sermons from EV Church based on a Bible passage.**

This project searches the [EV Church sermon archive](https://evchurch.info/media/), filters sermons by Bible reference (using verse-level overlap), downloads the MP3s, and generates accurate transcriptions using OpenAI's Whisper model.

## Features

- Intelligent Bible passage search with verse-level matching
- Automated MP3 downloading with retry logic
- Audio transcription using Whisper (`tiny` model)
- Docker support for easy, reproducible setup
- Outputs organized into `audio/` and `text/` folders
- SBL citation appended to transcription

## Quick Start (Docker - Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/sevasek/sermon-scraper.git
cd sermon-scraper

# 2. Build the container (first time only)
docker compose build --no-cache

# 3. Run the scraper
docker compose run --rm scraper python main.py "John 1"

### Project Structure after first run
```bash
audio/          # Downloaded MP3 files
text/           # Generated transcripts
```

### Example
docker compose run --rm scraper python main.py "John 3:16"
docker compose run --rm scraper python main.py "Jeremiah 29:11"

## Local Installation
```bash
git clone https://github.com/sevasek/sermon-scraper.git
cd sermon-scraper

# Install dependencies
pip install -r requirements.txt
playwright install

# Run
python main.py "Ezekiel 1"
```

## Project Structure
After running, you will see:
```bash
audio/          # Downloaded sermon MP3 files
text/           # Generated transcriptions (.txt files)
```
**Note:** When using Docker, these folders are automatically mounted from your machine.

## How It Works

1. Input → Bible passage(s) via command line
2. Search → Playwright scrapes EV Church sermon archive
3. Filter → pythonbible finds sermons with overlapping verses
4. Download → MP3 files saved with retry logic
5. Transcribe → Whisper (tiny model) converts audio to text and adds the citation

## Technologies Uses

- Python 3.11
- Playwright 1.45 – Browser automation
- pythonbible – Bible reference parsing and formatting
- OpenAI Whisper – Speech-to-text model
- Docker – Environment

## Development
```bash
# Rebuild container after changes
docker compose build

# Run with any passage
docker compose run --rm scraper python main.py "Your Passage Here"
```
## Afterword
Made during Boot.dev DevOps coursework.