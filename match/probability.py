from typing import List

from playwright.sync_api import Page

from common.domain import Match, Probability, Team


def scrape(page: Page) -> List[Match]:
    page.click('[for=choose-tips-EXPERTS]')

    is_checked = page.get_by_label("Ekspert").is_checked()
    print(f"Expert tips? {is_checked}")

    matches = []
    rows = page.locator("table tbody tr:not([aria-hidden='true'])").all()

    for row in rows:
        teams_locator = row.locator("th button div span").nth(0)
        teams = teams_locator.inner_text().split(' – ')

        probability_locators = row.locator("td div fieldset label span span").all()
        home_win = int(probability_locators[0].inner_text())
        tie = int(probability_locators[1].inner_text())
        away_win = int(probability_locators[2].inner_text())

        probability = Probability(
            home_win=home_win,
            tie=tie,
            away_win=away_win
        )

        home_team = Team(name=teams[0].split(' ', 1)[1])
        away_team = Team(name=teams[1])

        match = Match(
            home_team=home_team,
            away_team=away_team,
            probability=probability
        )

        matches.append(match)

    return matches
