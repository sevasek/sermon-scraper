from constants import base_url, keyword
from uuid import uuid4
from playwright.async_api import async_playwright, Playwright
import asyncio

sermon_urls = set()

# COMPLETED FUNCTIONS
def craft_results_url(passage):
    # Takes a Bible passage and returns a URL for scraping.
    results_url = base_url.replace(keyword, passage.replace(" ", "+"))
    return results_url

# INCOMPLETED FUNCTIONS
async def scrape_one_results_page(page, results_url: str):
    # Takes a Playwright page object and a URL for scraping, scrapes the page, and adds sermon URLs to the sermon_urls set.
    url = ""
    sermon_urls.add(url)
    
    
async def get_all_sermon_urls(start_url: str):
    # Takes a URL for scraping, scrapes first page + all pagination pages, returns a list of sermon URLs.
    # Calls scrape_one_results_page for each page to populate the sermon_urls set.
    async def run(playwright: Playwright):
        chromium = playwright.chromium
        browser = await chromium.launch(headless=True)
        page = await browser.new_page()





    return list(sermon_urls)

async def scrape_all_sermon_urls(sermon_urls: list):
    # Takes a list of sermon URLs, scrapes each page for the mp3 link, and returns a list of Sermon objects.
    return sermons



# ----- # 
# The folllowing functions are scraps.
# ----- # 

pagination_urls = set()



def scrape_results_page(results_url, first_page):
    # This function will scrape the results page and return a list of Sermon objects.

    async def run(playwright: Playwright):
        chromium = playwright.chromium
        browser = await chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(results_url, wait_until="domcontentloaded")
        
        await page.screenshot(path=f"screenshots/{uuid4()}.png")
        
        await page.wait_for_selector('a[href^="/media/"]', timeout=15000)

        sermon_links = await page.query_selector_all('a[href^="/media/"]')

        print(f"Found {len(sermon_links)} sermon links.")
        
        for link in sermon_links:
            sermon_url = "https://evchurch.info" + await link.get_attribute("href")
            sermon_urls.add(sermon_url)
        print("Sermon URLs:")
        print(sermon_urls)

        if first_page:
            pagination_links = await page.query_selector_all('a[href*="display_page="]')
            for link in pagination_links:
                href = await link.get_attribute("href")
                if not href:
                    continue
                pagination_urls.add(href)
        
        await browser.close()

    async def main():
        async with async_playwright() as playwright:
            await run(playwright)
    asyncio.run(main())

def scrape_pagination_pages():
    # This function will scrape the pagination page and return a list of Sermon objects.
    for url in pagination_urls:
        scrape_results_page(url, first_page=False)

scrape_pagination_pages()