import json
import time
from typing import List

from playwright.sync_api import sync_playwright

import compute_expected_value
from common import Coupon, Match
from scrape_odds import scrape_search
from scrape_probabilities import scrape_table


def run_scrape(coupon: Coupon, day: int):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_default_timeout(5000)

        page.goto(f"https://www.norsk-tipping.no/sport/tipping/spill?day={coupon.value}")
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
            scrape_search(page, match, day)
            time.sleep(1)

        print("----------------------------------------")

        output_data_dicts = [match.model_dump() for match in matches]
        with open("matches.json", "w") as f:
            json.dump(output_data_dicts, f, indent=4)

        browser.close()


def run_expected_value():
    filename = "matches.json"

    matches: List[Match] = []

    try:
        with open(filename, "r") as f:
            loaded_data = json.load(f)

        for item in loaded_data:
            matches.append(Match.model_validate(item))

        for match in matches:
            compute_expected_value.compute(match)
            print(match)

    except FileNotFoundError:
        print(f"'Could not find {filename}'.")
    except json.JSONDecodeError:
        print(f"Could not decode JSON from '{filename}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")




if __name__ == '__main__':
    # run_scrape(Coupon.MIDWEEK, 28)
    run_expected_value()
