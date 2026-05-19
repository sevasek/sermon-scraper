# Scraper Functions - scraper.py
# A collection of functions with the goal to scrape sermon URLs of a given Bible passage on the EV Church website.
# Success means a list of sermon dataclass objects are returned for further processing.

from constants import base_url, keyword
from playwright.async_api import async_playwright, Playwright
import asyncio

# Input: A Bible passage in the format "Book Chapter:Verse"
# Output: Returns a URL of the results page to be scraped.
def craft_results_url(passage):

    results_url = base_url.replace(keyword, passage.replace(" ", "+"))
    return results_url

# Input: Takes a the URL of the first results page.
# Adds the URL of the first page to the results_pages set.
# Scrapes the page for the remaining results page URLs and adds them to the results_pages set.
# In a loop, calls scrape_one_results_page with results page URL, until all results pages have been scraped.
# The individual sermon page URLs for each results page are caught and added to the set of individual sermon page URLs.
# Output: Returns a list of Sermon objects with the title, passage, mp3 link, etc. for each sermon (sermons).
async def scrape_all_sermon_page_urls(start_url: str):

    # Initialise the list of Sermon objects to be returned at the end of the function.
    sermons = []
        
    # Starts the Playwright browser and navigates to the start URL to begin scraping.
    async def run(playwright: Playwright):
        chromium = playwright.chromium
        browser = await chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(start_url, wait_until="domcontentloaded")

        # Initialise pagination_links with the start URL and update the links to the remaining results pages.
        pagination_links = set()
        pagination_links.add(start_url)
        elements = await page.query_selector_all('a[href*="display_page="]')
        for elem in elements:
            href = await elem.get_attribute("href")
            if href is not None:
                pagination_links.add(href)

        # Print the pagination links for debugging purposes.
        print(f"Found {len(pagination_links)} pagination links.")
        print("Pagination URLs:")
        for url in pagination_links:
            print(url)
        
        # Initialise sermon_page_urls as an empty set to store the URLs of the individual sermon pages.
        sermon_page_urls = set()

        # Loop through the pagination links and scrape each results page for the individual sermon page URLs.
        for url in pagination_links:
            await page.goto(url, wait_until="domcontentloaded")
            elements = await page.query_selector_all('a[href^="/media/"]')
            for elem in elements:
                href = await elem.get_attribute("href")
                if href is not None:
                    sermon_page_url = "https://evchurch.info" + href
                    sermon_page_urls.add(sermon_page_url)

        # Print the sermon page URLs for debugging purposes.
        print(f"Found {len(sermon_page_urls)} sermon page links.")
        print("Sermon Page URLs:")
        for url in sermon_page_urls:
            print(url)

        # Update the sermon_page_urls to point to the watch page instead of the media page, as the mp3 links are located on the watch page.
        updated_sermon_page_urls = set()

        for url in sermon_page_urls:
            updated_url = url.replace("/media/", "/media/watch/?media=")
            updated_sermon_page_urls.add(updated_url)

        # Print the updated sermon page URLs for debugging purposes.
        print(f"Updated {len(updated_sermon_page_urls)} sermon page links to watch page URLs.")
        print("Updated Sermon Page URLs:")  
        for url in updated_sermon_page_urls:
            print(url)

        # Loop throught the sermon_page_urls and create Sermon objects for each URL.
        # The Sermon objects will be stored in a list and returned at the end of the function.
        for url in updated_sermon_page_urls:
            await page.goto(url, wait_until="domcontentloaded")
            elements = await page.query_selector_all('a[href$=".mp3"]')
            for elem in elements:
                href = await elem.get_attribute("href")
                if href is not None:
                    mp3_url = "https://evchurch.info" + href
                    print(mp3_url)

        await browser.close()

        sermons.append("We got this far!")

        return
    
    # Runs the async function with Playwright
    async def scrape():
        async with async_playwright() as playwright:
            await run(playwright)
    
    # Calls the scrape function to commence the scraping process
    await scrape()

    return list(sermons)