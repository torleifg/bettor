import json
import time

from playwright.sync_api import sync_playwright

from common import Coupon
from scrape_odds import scrape_search
from scrape_probabilities import scrape_table

if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_default_timeout(5000)

        page.goto(f"https://www.norsk-tipping.no/sport/tipping/spill?day={Coupon.MIDWEEK.value}")
        page.wait_for_selector("body")

        time.sleep(1)

        cookies = page.get_by_role("button", name="Godta alle", exact=True)
        cookies.click()
        cookies.wait_for(state="hidden")

        time.sleep(1)

        matches = scrape_table(page)

        page.goto("https://www.norsk-tipping.no/sport/oddsen")
        page.wait_for_selector("body")

        time.sleep(1)

        for match in matches:
            print("----------------------------------------")
            print(match.teams_string())
            scrape_search(page, match)
            time.sleep(1)

        print("----------------------------------------")

        output_data_dicts = [match.model_dump() for match in matches]
        with open("matches.json", "w") as f:
            json.dump(output_data_dicts, f, indent=4)

        browser.close()
