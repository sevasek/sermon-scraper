# Boot.dev Personal Project 1

## Purpose
This python script produces transcriptions of sermons in the EV Church archive on a particular Bible passage.

## Background
This project is 
EV Church is a growing evangelical church on the outskirts of Sydney, Australia that practices the discipline of worldview preaching. Their sermon archives contain many high-quality examples of worldview preaching.
Many of these excellent resources do not have transcriptions available.
This tool will can be used to automate the process of transcribing this archive for research purposes.

## How to Install & Run
### Install Manually
1. **Install from GitHub**

```bash
git clone https://github.com/sevasek/personal-project.git
cd personal-project
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt

# Install the playwright browsers for scraping
playwright install
```

3. **Run locally**
```bash
python main.py "Genesis 1"
```

### Install using Docker
1. **Install Docker Desktop**
```bash
brew install --cask docker
```
2. **Start Docker Desktop**

3. **Build the container**
```bash
docker compose build --no-cache
```
4. **Run the scraper**
```bash
# Run with a specific Bible passage
docker compose run --rm scraper python main.py "Ezekiel 1"

# Or run interactively (you can enter different passages)
docker compose run --rm scraper
```

### Project Structure after first run
```bash
audio/          # Downloaded MP3 files
text/           # Generated transcripts
```

**Note**: If you are using Docker, then the `audio/` and `text/` folders are automatically mounted from your host machine, so files persist after the container stops.

## Workflow

1. **Main:** The main.py stages and coordinates the processing of the stages below
2. **Passages:** A Bible passage is passed to main.py via an input command.
3. **Scraper:** A playwright scraper uses the Bible passage to find mp3 files of relevant sermons on [EV Church's sermon archive](https://evchurch.info/media/). May download multiple sermons.
4. **Whisper:** [Whisper](https://github.com/openai/whisper) transcribes the mp3 into a text document. Audio files are processed one at a time.
5. **LLM Analysis:** The sermon transcription text document is analysed by an LLM. A markdown file specifies the instructions and formatting of the report. One report per mp3/text. The report is saved as a structured markdown document.
6. **LLM Summary:** Each analysis report is appended to a summary document with a read-to-use note citation in the Chicago Manual of Style 18th Edition format.

