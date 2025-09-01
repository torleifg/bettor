import argparse
import json
import time
from datetime import datetime

from playwright.sync_api import sync_playwright
from pydantic.json import pydantic_encoder

import expected_value
import kelly_criterion
import odds
import probability
from common import Coupon

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='bets')

    parser.add_argument('--coupon', required=True, type=str)
    parser.add_argument('--days', nargs="+", required=True, type=int)

    args = parser.parse_args()

    coupon = Coupon[args.coupon]
    days = set(args.days)

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

            odds.scrape(page, match, days)

            time.sleep(1)

            if match.odds is not None:
                expected_value.compute(match)

            if match.expected_value is not None:
                kelly_criterion.compute(match)

        match_time = datetime.now().isocalendar()

        for match in matches:
            if match.match_time is datetime:
                match_time = match.match_time.isocalendar()

        year = match_time.year
        week = match_time.week

        filename = f"data/matches_{week}_{year}_{coupon.name}.json"

        with open(filename, "w") as f:
            json.dump(matches, f, default=pydantic_encoder)

        browser.close()
