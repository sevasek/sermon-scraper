import asyncio

from filter import filter_by_bible_passage
from scraper import craft_results_url, scrape_all_sermon_page_urls
from sermons import Sermon
import sys
import pythonbible as bible

async def main():
    # Get the Bible passage(s) from the command line arguments.
    if len(sys.argv) < 2:
        print("Usage: python main.py <bible_passages>")
        return

    # Validate the input is a valid Bible passage
    try:
        bible.get_references(sys.argv[1])
    except Exception as e:
        print(f"Invalid Bible passage: {e}")
        return

    list_of_normalized_references = bible.get_references(sys.argv[1])

    # Prepare normalized and formatted references
    # list_of_normalized_references = bible.get_references(sys.argv[1])
    string_of_formatted_references = bible.format_scripture_references(list_of_normalized_references)
    list_of_formatted_references = string_of_formatted_references.split(";")

    # Create a list of tuples for matching passages
    # Each tuple contains a formatted reference and the associated results URLs
    list_tuples_ref_results_urls = []
    for ref in list_of_formatted_references:
        url = craft_results_url(ref)
        list_tuples_ref_results_urls.append((ref, url))

    # Output: a URL for scraping. Results_url is the URL for the first page of search results for the given passage.    
    # Output: a list of Sermon objects with the title, passage, mp3 link, etc. for each sermon (sermons)
    all_sermons = []

    for tuple in list_tuples_ref_results_urls:
        ref = tuple[0]
        url = tuple[1]
        sermons_subset = await scrape_all_sermon_page_urls(url)
        if sermons_subset is not None and not sermons_subset:
            continue
        else:
            all_sermons += sermons_subset
    
    if all_sermons is not None and not all_sermons:
        print(f"No sermons found for {string_of_formatted_references}.")
        return

    # Input 1: A list of Sermon objects (all_sermons) containing a list of normalized references
    # Input 2: A list of normalized references from the command line input (normalized_references).
    filtered_sermons = filter_by_bible_passage(all_sermons, list_of_normalized_references)

    print("\nFiltered Sermons:")
    for sermon in filtered_sermons:
        print(sermon)
    return

if __name__ == "__main__":
    asyncio.run(main())