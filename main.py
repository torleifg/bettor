import json
import time

from playwright.sync_api import sync_playwright
from prettytable import PrettyTable
from pydantic import TypeAdapter
from pydantic.json import pydantic_encoder

import expected_value
import kelly_criterion
import odds
import probability
from common import Coupon, Match, Bet, Result


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

            if match.odds is not None:
                expected_value.compute(match)

            if match.expected_value is not None:
                kelly_criterion.compute(match)

        filename = f"matches_{matches[0].match_time.strftime('%Y%m%d')}.json"

        with open(filename, "w") as f:
            json.dump(matches, f, default=pydantic_encoder)

        browser.close()


def bet_amounts(filename: str, balance: int):
    with open(filename, "r") as f:
        data = json.load(f)

    match_list_adapter = TypeAdapter(list[Match])

    matches = match_list_adapter.validate_python(data)

    bets = []

    for match in matches:
        if match.bet_fraction is None:
            continue

        if match.expected_value.home_win > 0:
            bets.append(Bet(home_team=match.home_team.name, away_team=match.away_team.name, result=Result.H,
                            expected_value=match.expected_value.home_win, bet_fraction=match.bet_fraction.home_win))
        if match.expected_value.tie > 0:
            bets.append(Bet(home_team=match.home_team.name, away_team=match.away_team.name, result=Result.T,
                            expected_value=match.expected_value.tie, bet_fraction=match.bet_fraction.tie))
        if match.expected_value.away_win > 0:
            bets.append(Bet(home_team=match.home_team.name, away_team=match.away_team.name, result=Result.A,
                            expected_value=match.expected_value.away_win, bet_fraction=match.bet_fraction.away_win))

    bets.sort(key=lambda b: b.expected_value, reverse=True)

    table = PrettyTable()

    table.field_names = ["Home team", "Away team", "Result", "Expected Value", "Bet Fraction", "Balance", "Bet Amount"]

    print(f"Balance: {balance}")

    for bet in bets:
        bet_amount = int(bet.bet_fraction * balance)
        table.add_row(
            [bet.home_team, bet.away_team, bet.result.value, bet.expected_value, bet.bet_fraction, balance, bet_amount])
        balance -= bet_amount

    print(table)

    print(f"Balance: {balance}")


if __name__ == '__main__':
    bet_amounts("matches_20250831.json", 500)
    # run(Coupon.SUNDAY, 500)
