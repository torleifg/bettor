from playwright.sync_api import Page

from models import Match, Probability, Team


def scrape_table(page: Page) -> list[Match]:
    page.click('[for=choose-tips-EXPERTS]')

    is_checked = page.get_by_label("Ekspert").is_checked()
    print(f"Expert tips? {is_checked}")

    # page.screenshot(path="example.png")

    matches = []
    rows = page.locator("table tbody tr:not([aria-hidden='true'])").all()

    for row in rows:
        match_cells = row.locator("th button div span").nth(0)
        teams = match_cells.inner_text().split(' – ')

        probabilities_cells = row.locator("td div fieldset label span span").all()
        probability = Probability(
            home_win=int(probabilities_cells[0].inner_text()),
            tie=int(probabilities_cells[1].inner_text()),
            away_win=int(probabilities_cells[2].inner_text())
        )

        match = Match(
            home_team=Team(name=teams[0].split(' ', 1)[1]),
            away_team=Team(name=teams[1]),
            probability=probability
        )

        matches.append(match)

    return matches
