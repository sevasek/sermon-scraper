# Local Sermon Index - index.py
# Persists scraped Sermon metadata to a local SQLite file so repeat runs can
# skip re-scraping sermon pages that have already been indexed.

import sqlite3
from contextlib import closing

import pythonbible as bible

from sermons import Sermon

DB_PATH = "sermon_index.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS sermons (
    url TEXT PRIMARY KEY,
    url_mp3 TEXT,
    bible_passage TEXT,
    title TEXT,
    speaker TEXT,
    location TEXT,
    date TEXT,
    event TEXT
)
"""

def init_db(db_path: str = DB_PATH):
    with closing(sqlite3.connect(db_path)) as conn:
        conn.execute(SCHEMA)
        conn.commit()

def get_indexed_urls(db_path: str = DB_PATH) -> set:
    with closing(sqlite3.connect(db_path)) as conn:
        rows = conn.execute("SELECT url FROM sermons").fetchall()
    return {row[0] for row in rows}

def save_sermons(sermon_objects, db_path: str = DB_PATH):
    if not sermon_objects:
        return
    with closing(sqlite3.connect(db_path)) as conn:
        for sermon in sermon_objects:
            bible_passage_str = (
                bible.format_scripture_references(sermon.bible_passage)
                if sermon.bible_passage
                else ""
            )
            conn.execute(
                """
                INSERT INTO sermons (url, url_mp3, bible_passage, title, speaker, location, date, event)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(url) DO UPDATE SET
                    url_mp3=excluded.url_mp3,
                    bible_passage=excluded.bible_passage,
                    title=excluded.title,
                    speaker=excluded.speaker,
                    location=excluded.location,
                    date=excluded.date,
                    event=excluded.event
                """,
                (
                    sermon.url,
                    sermon.url_mp3,
                    bible_passage_str,
                    sermon.title,
                    sermon.speaker,
                    sermon.location,
                    sermon.date,
                    sermon.event,
                ),
            )
        conn.commit()

def load_sermons_by_urls(urls, db_path: str = DB_PATH) -> list:
    if not urls:
        return []
    with closing(sqlite3.connect(db_path)) as conn:
        placeholders = ",".join("?" for _ in urls)
        rows = conn.execute(
            f"SELECT url, url_mp3, bible_passage, title, speaker, location, date, event "
            f"FROM sermons WHERE url IN ({placeholders})",
            tuple(urls),
        ).fetchall()

    sermons = []
    for url, url_mp3, bible_passage_str, title, speaker, location, date, event in rows:
        bible_passage = bible.get_references(bible_passage_str) if bible_passage_str else ""
        sermons.append(
            Sermon(
                url=url,
                url_mp3=url_mp3,
                bible_passage=bible_passage,
                title=title,
                speaker=speaker,
                location=location,
                date=date,
                event=event,
            )
        )
    return sermons
