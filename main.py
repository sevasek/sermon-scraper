from scraper import craft_results_url, get_all_sermon_urls, scrape_all_sermon_urls

import webbrowser, sys

async def main():
    passage = sys.argv[1]

    # Craft the URL for the search results page based on the passage provided as a command-line argument.
    results_url = craft_results_url(passage)
    
    # Get all sermon URLs from the search results page and pagination pages.
    sermon_urls = await get_all_sermon_urls(results_url)
    
    # Scrape the results page and return a list of Sermon objects
    sermons = await scrape_all_sermon_urls(sermon_urls)

    for sermon in sermons:
        sermon.download()

    return

if __name__ == "__main__":
    main()