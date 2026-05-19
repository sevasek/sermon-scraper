# Scraper Functions - scraper.py
# A collection of functions with the goal to scrape sermon URLs of a given Bible passage on the EV Church website.
# Success means a list of sermon dataclass objects are returned for further processing.

from constants import base_url, keyword
from playwright.async_api import async_playwright, Playwright
import asyncio

# A set to store the URLs of the sermon pages.
single_sermon_pages = set()

# Input: A Bible passage in the format "Book Chapter:Verse"
# Output: Returns a URL of the results page to be scraped.
def craft_results_url(passage):

    results_url = base_url.replace(keyword, passage.replace(" ", "+"))
    return results_url

# Input: A Playwright page object and the URL of a results page to be scraped. 
# Each results page contains links to the sermon page.
# The function will scrape the page for sermon page URLs and add them to the sermon_urls set.
# Do not worry about the pagination pages.
# Output: None. The sermon_urls set will be updated with the URLs of the sermon pages.
async def scrape_one_results_page(page, results_url: str):
    sermon_page_links = await page.query_selector_all('a[href^="/media/"]')
    for link in sermon_page_links:
        # TODO: Check this produces the correct sermon URL. It should be in format "https://evchurch.info/media/code/"
        sermon_url = "https://evchurch.info" + await link.get_attribute("href")
        single_sermon_pages.add(sermon_url)
    print(f"Found {len(sermon_page_links)} sermon links on {results_url}.")
    print("Sermon URLs:")
    for url in single_sermon_pages:
        print(url)
    return

# Input: Takes a the URL of the first results page.
# Adds the URL of the first page to the results_pages set.
# Scrapes the page for the remaining results page URLs and adds them to the results_pages set.
# In a loop, calls scrape_one_results_page with results page URL, until all results pages have been scraped.
# The individual sermon page URLs for each results page are caught and added to the set of individual sermon page URLs.
# Output: Returns a list of sermon URLs.
async def get_all_sermon_urls(start_url: str):

    # A set for the individual sermon page links.
    # These pages contain the mp3 links and other meta information about the sermons.
    # This set is updated below, and will be processed by the scrape_all_sermon_page_urls function.
    sermon_page_urls = set()
        
    # Starts the Playwright browser and navigates to the start URL to begin scraping.
    async def run(playwright: Playwright):
        chromium = playwright.chromium
        browser = await chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(start_url, wait_until="domcontentloaded")

        # Initialise pagination_links with the start URL and update the links to the remaining results pages.
        pagination_links = set()
        pagination_links.add(start_url)
        pagination_links.update(await page.query_selector_all('a[href*="display_page="]'))

        # Loop through the pagination links and call scrape_one_results_page for each results page URL.
        for link in pagination_links:
            href = await link.get_attribute("href")
            page_url = "https://evchurch.info" + href
            subset_sermon_pages = list(await scrape_one_results_page(page, page_url))
            sermon_page_urls.update(subset_sermon_pages)

        await browser.close()
    
    # Runs the async function with Playwright
    async def scrape():
        async with async_playwright() as playwright:
            await run(playwright)
    
    # Calls the scrape function to commence the scraping process
    asyncio.run(scrape())

    return list(sermon_page_urls)

# Input: The list of sermon_urls to be scraped.
# The scraper must identify various attributes defined in the Sermon dataclass, such as the title, speaker, date, location, bible passage, and mp3 link.
# Output: A list of Sermon objects.
async def scrape_all_sermon_page_urls(sermon_urls: list):

    return None