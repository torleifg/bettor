from playwright.sync_api import Page, TimeoutError

from common import Match, Odds


def scrape(page: Page, match: Match, day: int):
    iframe_locator = page.locator("#sportsbookid")
    iframe_locator.wait_for()

    iframe = iframe_locator.content_frame

    search_input_locator = iframe.locator("#searchText")
    search_input_locator.wait_for()

    try:
        search_input_locator.fill(match.home_team.name)
        iframe.locator("#search-event-list-container").wait_for()

        print(f"Search results found for home team: {match.home_team.name}")
    except TimeoutError:
        print(f"No search results found for home team: {match.home_team.name}")

        try:
            search_input_locator.clear()
            search_input_locator.fill(match.away_team.name)
            iframe.locator("#search-event-list-container").wait_for()
            print(f"Search results found for away team: {match.away_team.name}")
        except TimeoutError:
            print(f"No search results found for away team: {match.teams_string()}")
            return None

    search_results_locator = iframe.locator('div[role="listitem"]')
    search_results = search_results_locator.all()

    print(f"Found {len(search_results)} search results.")

    target_locator = None

    for search_result in search_results:
        info_locator = search_result.locator("span span")
        info = info_locator.all()

        teams = info[1].inner_text()
        date = info[2].inner_text()

        if str(day) in date:
            match.date_time = date.rstrip(".")
            target_locator = iframe.locator(f'div[role="listitem"]:has-text("{teams}")')

    if not target_locator:
        print(f"No match found with {day} in the date.")
        search_input_locator.clear()
        return None

    target_locator.click()

    iframe.locator("h1").wait_for()

    odds_locator = iframe.locator('div[data-tip="tooltip"] span')

    home_win = float(odds_locator.nth(1).inner_text())
    tie = float(odds_locator.nth(3).inner_text())
    away_win = float(odds_locator.nth(5).inner_text())

    match.odds = Odds(
        home_win=home_win,
        tie=tie,
        away_win=away_win
    )

    return None
