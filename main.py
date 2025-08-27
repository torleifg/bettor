from playwright.sync_api import sync_playwright

from models import Coupon
from scrape_probabilities import scrape_table

if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_default_timeout(5000)

        url = f"https://www.norsk-tipping.no/sport/tipping/spill?day={Coupon.SUNDAY.value}"
        page.goto(url)

        try:
            accept_button = page.get_by_role("button", name="Godta alle", exact=True)
            accept_button.click()
            accept_button.wait_for(state="hidden")
            print("Successfully accepted cookies.")
        except:
            print("No cookie pop-up found or already handled.")

        matches = scrape_table(page)

        for match in matches:
            print(match)

        browser.close()
