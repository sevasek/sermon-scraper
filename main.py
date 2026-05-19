from scraper import craft_results_url, get_all_sermon_urls, scrape_all_sermon_urls
from sermons import Sermon
import webbrowser, sys

async def main():
    passage = sys.argv[1]

    # Input: a Bible passage (e.g. "John 3:16")
    # Output: a URL for scraping. Results_url is the URL for the first page of search results for the given passage.
    results_url = craft_results_url(passage)
    
    # Input: results URL
    # Output: the list of pages where the sermons are located (sermon_urls)
    sermon_urls = await get_all_sermon_urls(results_url)
    
    # Input: the list of pages where the sermons are located (sermon_urls)
    # Output: a list of Sermon objects with the title, passage, mp3 link, etc. for each sermon (sermons)
    sermons = await scrape_all_sermon_urls(sermon_urls)

    def is_in_passage_range(sermon):
        # This function will take a sermon and return True if the sermon is in the passage range, and False otherwise.
        # The passage range is determined by the bible_passage attribute of the sermon object.
        # The bible_passage attribute is a string that contains the passage range (e.g. "John 3:16-18").
        # The function will need to parse the bible_passage string and determine if the passage is in the range.
        return True

    filtered_sermons = filter(is_in_passage_range(sermon), sermons)

    for sermon in sermons:
        sermon.download()
    return

if __name__ == "__main__":
    main()