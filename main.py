import json
import time

from playwright.sync_api import sync_playwright
from pydantic.json import pydantic_encoder

import expected_value
import kelly_criterion
import odds
import probability
from common import Coupon


def run(coupon: Coupon, day: int):
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

        for match in matches:
            expected_value.compute(match)
            kelly_criterion.compute(match)

        matches.sort(key=sort_key, reverse=True)

        filename = f"matches_{matches[0].match_time.strftime('%Y%m%d')}_{matches[0].scrape_time.strftime('%Y%m%d')}.json"

        with open(filename, "w") as f:
            json.dump(matches, f, default=pydantic_encoder)

        browser.close()


def sort_key(match):
    if match.expected_value:
        return max(match.expected_value.home_win, match.expected_value.tie, match.expected_value.away_win)
    return -1


if __name__ == '__main__':
    run(Coupon.SATURDAY, 30)
