# Scraper Functions - scraper.py
# A collection of functions with the goal to scrape sermon URLs of a given Bible passage on the EV Church website.
# Success means a list of sermon dataclass objects are returned for further processing.

from constants import base_url, keyword, geo_location
from playwright.async_api import async_playwright, Playwright
import asyncio
import pythonbible as bible

from sermons import Sermon

# Input: A Bible passage in the format "Book Chapter:Verse"
# Output: Returns a URL of the results page to be scraped.
def craft_results_url(passage):

    results_url = base_url.replace(keyword, passage).replace(" ", "+")
    return results_url

# Input: Takes a the URL of the first results page.
# Adds the URL of the first page to the results_pages set.
# Scrapes the page for the remaining results page URLs and adds them to the results_pages set.
# In a loop, calls scrape_one_results_page with results page URL, until all results pages have been scraped.
# The individual sermon page URLs for each results page are caught and added to the set of individual sermon page URLs.
# Output: Returns a list of Sermon objects with the title, passage, mp3 link, etc. for each sermon (sermons).
async def scrape_all_sermon_page_urls(start_url: str):
        
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
        if sermon_page_urls is not None and not sermon_page_urls:
            return []
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

        # Initialise the list of Sermon objects to be returned at the end of the function.
        sermons = []

        # Loop throught the sermon_page_urls and create Sermon objects for each URL.
        # The Sermon objects will be stored in a list and returned at the end of the function.
        for url in updated_sermon_page_urls:
            await page.goto(url, wait_until="domcontentloaded")

            # Time to extract the relevant information for each sermon and create a Sermon object.
            # URL
            sermon_object_url = url

            # MP3
            sermon_object_mp3_url = ""
            mp3_elements = await page.query_selector_all('source[src$=".mp3"]')
            for elem in mp3_elements:
                src = await elem.get_attribute("src")
                if src is not None:
                    mp3_url = "https://evchurch.info" + src
                    sermon_object_mp3_url = mp3_url
            print(f"MP3 URL: {sermon_object_mp3_url}")

            # TITLE
            title_elements = await page.query_selector('h2')
            if title_elements is not None:
                raw_title = await title_elements.text_content()
                clean_title = "".join(raw_title).replace("\n                    ", "").replace("\xa0\xa0", "")

            sermon_object_title = clean_title

            # LOCATION
            sermon_object_location = geo_location
            
            # BIBLE PASSAGE, SPEAKER, DATE, EVENT
            elements = await page.query_selector_all('h4')
            for elem in elements:
                text = await elem.inner_text()
                if isinstance(text, str):
                    bible_passages = bible.get_references(text)
                    meta_parts = text.split(" | ")
                    if len(meta_parts) == 4:
                        sermon_object_bible_passage = bible_passages
                        sermon_object_event = meta_parts[1]
                        sermon_object_date = meta_parts[2]
                        sermon_object_speaker = meta_parts[3]
                    if len(meta_parts) == 3:
                        sermon_object_bible_passage = ""
                        sermon_object_event = meta_parts[0]
                        sermon_object_date = meta_parts[1]
                        sermon_object_speaker = meta_parts[2]
                
                # Create the Sermon object
                sermon_object = Sermon(
                    url=sermon_object_url, 
                    url_mp3=sermon_object_mp3_url, 
                    bible_passage=sermon_object_bible_passage,
                    title=sermon_object_title,
                    speaker=sermon_object_speaker,
                    location=sermon_object_location,
                    date=sermon_object_date,
                    event=sermon_object_event)
                sermons.append(sermon_object)
        await browser.close()
        return sermons
    
    # Runs the async function with Playwright
    async def scrape():
        async with async_playwright() as playwright:
            object_list = await run(playwright)
            return object_list
    
    # Calls the scrape function to commence the scraping process
    x = await scrape()

    return list(x)