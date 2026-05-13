from scraper import craft_results_url, scrape_results_page
import webbrowser, sys

def main():
    passage = sys.argv[1]

    # Craft the URL for the search results page based on the passage provided as a command-line argument.
    results_url = craft_results_url(passage)
    # print(f"Crafted URL: {results_url}")
    
    # Open the crafted URL in the default web browser.
    # webbrowser.open(results_url)

    # Scrape the results page and return a list of Sermon objects
    scrape_results_page(results_url, first_page=True)
    return

if __name__ == "__main__":
    main()