# EV Church Sermon Transcriber

**A tool to find, download, and transcribe sermons from EV Church based on a Bible passage.**

This project searches the [EV Church sermon archive](https://evchurch.info/media/), filters sermons by Bible reference (using verse-level overlap), downloads the MP3s, and generates accurate transcriptions using OpenAI's Whisper model.

## Features

- Intelligent Bible passage search with verse-level matching via `pythonbible`
- Playwright-driven scraper handles pagination automatically
- Automated MP3 downloading with 3-attempt retry logic
- Audio transcription using OpenAI Whisper (`tiny` model by default)
- SBL-style citation appended to every transcript
- Docker support for a fully reproducible, dependency-free setup
- Outputs persist in `audio/` and `text/` folders (excluded from git)

## Quick Start (Docker — Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/sevasek/sermon-scraper.git
cd sermon-scraper

# 2. Build the container (first time only — downloads Whisper model)
docker compose build --no-cache

# 3. Run the scraper with any Bible passage
docker compose run --rm scraper python main.py "John 1"
docker compose run --rm scraper python main.py "John 3:16"
docker compose run --rm scraper python main.py "Jeremiah 29:11"
```

After the first run, you will find:
```
audio/          # Downloaded sermon MP3 files (git-ignored)
text/           # Generated transcriptions (.txt, git-ignored)
```

## Local Installation

```bash
git clone https://github.com/sevasek/sermon-scraper.git
cd sermon-scraper

pip install -r requirements.txt
playwright install chromium

python main.py "Ezekiel 1"
```

## How It Works

```
Input  →  Bible passage(s) via command line
Search →  Playwright scrapes EV Church sermon archive (with pagination)
Filter →  pythonbible finds sermons with overlapping verse IDs
Download → MP3 files saved with retry logic
Transcribe → Whisper (tiny model) converts audio to text + SBL citation
```

## Project Structure

```
sermon-scraper/
├── main.py          # Entry point — orchestrates the pipeline
├── scraper.py       # Playwright scraper; returns list of Sermon objects
├── filter.py        # Verse-level overlap filter
├── download.py      # MP3 downloader with retry
├── transcribe.py    # Whisper transcription + SBL citation
├── sermons.py       # Sermon dataclass
├── constants.py     # Base URL and hardcoded geo_location
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Technologies Used

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.11 | Runtime |
| Playwright | 1.45 | Browser automation / scraping |
| pythonbible | latest | Bible reference parsing |
| OpenAI Whisper | latest | Speech-to-text |
| Docker | — | Reproducible environment |

## Limitations

- **EV Church only** — the scraper is hardcoded to `evchurch.info`. The URL structure and HTML selectors are specific to their media archive.
- **Location hardcoded** — `constants.py` sets `geo_location = "Erina, NSW"`. If the church has multiple campuses, update this manually.
- **Tiny Whisper model** — `transcribe.py` uses the `tiny` model for speed. For better accuracy on quiet or accented audio, swap to `base` or `small` by editing `transcribe.py:43`.
- **English only** — Whisper is forced to `language="en"` in `transcribe.py`.

## Development

```bash
# Rebuild container after code changes
docker compose build

# Run with a different passage
docker compose run --rm scraper python main.py "Romans 8"
```

## 🚀 Roadmap & Future Releases

### v1.1 — Whisper model size flag
Add a `--model` CLI argument so users can choose between `tiny`, `base`, `small`, `medium`, or `large` without editing source code. Tiny is fast; larger models are more accurate on quiet or accented recordings.

### v1.2 — Progress bar + run summary
Replace raw `print()` calls with a `tqdm` progress bar for downloads and transcription. On completion, print a summary table of sermons found, downloaded, and transcribed.

### v2.0 — Multi-church adapter pattern
Abstract the scraping logic into a `SermonScraper` base class so the tool can support additional church websites. `EVChurchScraper` would be the first concrete implementation. New churches could be added by extending the base class and updating `constants.py`.

## Afterword

Made during Boot.dev DevOps coursework as a personal project for studying Bible passages from sermon archives.
