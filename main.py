import asyncio

from scraper import craft_results_url, scrape_all_sermon_page_urls
from sermons import Sermon
import sys

async def main():
    passage = sys.argv[1]

    # Input: a Bible passage (e.g. "John 3:16")
    # Output: a URL for scraping. Results_url is the URL for the first page of search results for the given passage.
    results_url = craft_results_url(passage)
    
    # Input: results URL
    # Output: a list of Sermon objects with the title, passage, mp3 link, etc. for each sermon (sermons)
    sermons = await scrape_all_sermon_page_urls(results_url)

    # Download the mp3 files for each sermon in the sermons list.
    for sermon in sermons:
        sermon.download()
    return

if __name__ == "__main__":
    asyncio.run(main())