# Boot.dev Personal Project 1

## Purpose
This python script produces a research report on the techniques used in sermons on a particular passage of the Bible at EV Church.

## Background
Sermon preparation requires a lot of time and creative energy. For those who practice the discipline of worldview preaching, whereby the preacher is seeking to persuade the audience to the Bible's view of God, themselves, and the world, it is critical that the sermon connects the message of the passage with the audience. One of the most fruitful avenues for crafting sermon techniques that connect the message with the audience is going back through sermon archives.
Effective sermon techniques include applications, implications, illustrations, metaphors, imagery and rhetorical questions.
EV Church is a growing evangelical church on the outskirts of Sydney, Australia that practices the discipline of worldview preaching. Their sermon archives contain many high-quality examples of worldview preaching.
By automating the search for techniques, and providing full attribution, this system speeds up the creative process and increases the likelihood of a high-quality worldview sermon.

## How to Use
1. Install from GitHub

```bash
git clone https://github.com/sevasek/personal-project.git
cd personal-project
```

2. Install Dependencies
```bash
pip install -r requirements.txt
```

3. Set LLM API key
This script will look for an Ollama API key and model name in the following location:

```bash
echo "OLLAMA_HOST=http://localhost:11434" >> ~/.sermon_tech/.env
echo "OLLAMA_MODEL=llama3.1:8b" >> ~/.sermon_tech/.env
echo "OLLAMA_API_KEY=your-api-key" >> ~/.sermon_tech/.env
```

4. Run locally
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

