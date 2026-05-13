# Boot.dev Personal Project 1

## Purpose
The purpose of this project is to create a python script that produces a research report on applications, implications, illustrations, metaphors and imagery used in sermons of a particular passage of the Bible.

## How to Use
Install from GitHub
```bash
git clone https://github.com/sevasek/personal-project.git
cd personal-project

```
Run locally
```bash
python main.py "Genesis 1"
```

## Workflow

1. **Main:** The main.py stages and coordinates the processing of the stages below
2. **Passages:** A Bible passage is passed to main.py via an input command.
3. **Scraper:** A playwright scraper uses the Bible passage to find mp3 files of relevant sermons on [EV Church's sermon archive](https://evchurch.info/media/). May download multiple sermons.
4. **Whisper:** [Whisper](https://github.com/openai/whisper) transcribes the mp3 into a text document. Audio files are processed one at a time.
5. **LLM Analysis:** The sermon transcription text document is analysed by an LLM. A markdown file specifies the instructions and formatting of the report. One report per mp3/text. The report is saved as a structured markdown document.
6. **LLM Summary:** Each analysis report is appended to a summary document with a read-to-use note citation in the Chicago Manual of Style 18th Edition format.

