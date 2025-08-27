from enum import Enum
from typing import Annotated

from playwright.sync_api import sync_playwright
from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self


class Coupon(Enum):
    MIDWEEK = 3
    SATURDAY = 1
    SUNDAY = 2


class Team(BaseModel):
    name: Annotated[str, Field(min_length=1)]


class Probability(BaseModel):
    home_win: Annotated[int, Field(ge=0, le=100)]
    tie: Annotated[int, Field(ge=0, le=100)]
    away_win: Annotated[int, Field(ge=0, le=100)]

    @model_validator(mode='after')
    def check_sum(self) -> Self:
        if self.home_win + self.away_win + self.tie != 100:
            raise ValueError('The sum of all probabilities must be 100.')
        return self


class Match(BaseModel):
    home_team: Team
    away_team: Team
    probability: Probability


def scrape_table(coupon: Coupon) -> list[Match]:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_default_timeout(5000)

        url = f"https://www.norsk-tipping.no/sport/tipping/spill?day={coupon.value}"
        page.goto(url)

        try:
            accept_button = page.get_by_role("button", name="Godta alle", exact=True)
            accept_button.click()
            accept_button.wait_for(state="hidden")
            print("Successfully accepted cookies.")
        except:
            print("No cookie pop-up found or already handled.")

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

        browser.close()

        return matches
