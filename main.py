import json
import time
from typing import List

from playwright.sync_api import sync_playwright

import expected_value
import kelly_criterion
import odds
import probability
from common import Coupon, Match


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

        matches = probability.scrape(page)

        page.goto("https://www.norsk-tipping.no/sport/oddsen")
        page.wait_for_selector("body")

        time.sleep(1)

        for match in matches:
            print("----------------------------------------")
            print(match.teams_string())
            odds.scrape(page, match, day)
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

        for data in loaded_data:
            matches.append(Match.model_validate(data))

        for match in matches:
            expected_value.compute(match)
            print(match)

        print("------------------------")

        bets: List[Match] = []

        for match in matches:
            if match.expected_value is not None and match.expected_value.is_greater_than(0.05):
                bets.append(match)

        bets.sort(key=lambda it: max(it.expected_value.home_win, it.expected_value.tie, it.expected_value.away_win),
                  reverse=True)

        for bet in bets:
            kelly_criterion.compute(bet)
            print(bet)

    except FileNotFoundError:
        print(f"'Could not find {filename}'.")
    except json.JSONDecodeError:
        print(f"Could not decode JSON from '{filename}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    #run_scrape(Coupon.SATURDAY, 30)
    run_expected_value()
