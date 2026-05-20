import asyncio

from filter import filter_by_bible_passage
from scraper import craft_results_url, scrape_all_sermon_page_urls
from sermons import Sermon
import sys
import pythonbible as bible


async def main():
    # Get the Bible passage from the command line arguments.
    if len(sys.argv) < 2:
        print("Usage: python main.py <bible_passage>")
        return

    # Validate the Bible passage
    try:
        bible.get_references(sys.argv[1])
    except Exception as e:
        print(f"Invalid Bible passage: {e}")
        return
    
    passage = bible.get_references(sys.argv[1])

    # Input: a Bible passage (e.g. "John 3:16")
    # Output: a URL for scraping. Results_url is the URL for the first page of search results for the given passage.
    results_url = craft_results_url(passage)
    
    # Input: results URL
    # Output: a list of Sermon objects with the title, passage, mp3 link, etc. for each sermon (sermons)
    sermons = await scrape_all_sermon_page_urls(results_url)

    # Print all sermons before filtering
    print("\nAll Sermons:")
    for sermon in sermons:
        print(sermon)
    
    filtered_sermons = filter_by_bible_passage(sermons, passage)

    print("\nFiltered Sermons:")
    for sermon in filtered_sermons:
        print(sermon)

    return

if __name__ == "__main__":
    asyncio.run(main())