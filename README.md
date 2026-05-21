# Boot.dev Personal Project 1

## Purpose
This python script produces transcriptions of sermons in the EV Church archive on a particular Bible passage.

## Background
- This project was started as a part of the Boot.dev DevOps Path course. The goal was to simply to get used to the process of building something from scratch.
- EV Church is a growing evangelical church on the outskirts of Sydney, Australia that practices the discipline of worldview preaching. Their sermon archives contain many high-quality examples of worldview preaching. Many of these excellent resources do not have transcriptions available.
- This tool will can be used to automate the process of transcribing this archive for research purposes.

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
# Run with a specific Bible passage(s)
python main.py "<Bible references>"
# Example
python main.py "Ezekiel 1:7; 1 Thessalonians 2:3"
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
# Run with a specific Bible passage(s)
docker compose run --rm scraper python main.py "<Bible references>"
# Example
docker compose run --rm scraper python main.py "Ezekiel 1:7; 1 Thessalonians 2:3"
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
2. **Passages:** A Bible passage is passed to main.py via an input command. We use pythonbible to standardize and format the reference for later uses.
3. **Scraper:** A playwright scraper uses the Bible passage to find the corresponding pages on the [EV Church sermon archive](https://evchurch.info/media/), and stores the metadata in an object. 
4. **Filter & Download:** The sermon objects are filtered to find only the sermons whose Bible passages intersect with the references provided. The mp3 file for these filtered sermons is then downloaded to the `audio/` folder. 
5. **Whisper:** [Whisper](https://github.com/openai/whisper) transcribes the mp3 into a text document. Audio files are processed one at a time, and the text file is stored in the `text/` folder.
6. A simple citation reference for the sermon is added to the end of the text file.
