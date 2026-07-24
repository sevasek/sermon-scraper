import asyncio

from filter import filter_by_bible_passage
from scraper import craft_results_url, discover_sermon_page_urls, scrape_sermon_details
from download import download_mp3_update
from transcribe import transcribe_all
from index import init_db, get_indexed_urls, load_sermons_by_urls, save_sermons
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
    string_of_formatted_references = bible.format_scripture_references(list_of_normalized_references)
    list_of_formatted_references = string_of_formatted_references.split(";")

    list_tuples_ref_results_urls = []
    for ref in list_of_formatted_references:
        url = craft_results_url(ref)
        list_tuples_ref_results_urls.append((ref, url))

    init_db()

    all_sermons = []

    for tuple in list_tuples_ref_results_urls:
        ref = tuple[0] # I thought I would need this later. Turns out pythonbible is very versatile!
        url = tuple[1]
        sermon_page_urls = await discover_sermon_page_urls(url)
        if sermon_page_urls is not None and not sermon_page_urls:
            continue

        # Skip re-scraping sermon pages already present in the local index.
        indexed_urls = get_indexed_urls()
        cached_urls = sermon_page_urls & indexed_urls
        new_urls = sermon_page_urls - indexed_urls

        sermons_subset = load_sermons_by_urls(cached_urls)
        if cached_urls:
            print(f"Loaded {len(cached_urls)} sermon(s) from local index (skipped re-scrape).")

        if new_urls:
            newly_scraped = await scrape_sermon_details(new_urls)
            save_sermons(newly_scraped)
            sermons_subset += newly_scraped

        all_sermons += sermons_subset
    
    if all_sermons is not None and not all_sermons:
        print(f"No sermons found for {string_of_formatted_references}.")
        return

    filtered_sermons = filter_by_bible_passage(all_sermons, list_of_normalized_references)

    downloaded_sermons = download_mp3_update(filtered_sermons)

    transcribe_all(downloaded_sermons)

if __name__ == "__main__":
    asyncio.run(main())