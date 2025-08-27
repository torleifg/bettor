from playwright.sync_api import sync_playwright


def scrape_table():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Navigate to the page
        page.goto("https://www.norsk-tipping.no/sport/tipping/spill?day=3")

        # Wait for the table to appear (adjust the selector as needed)
        page.wait_for_selector("table")

        is_checked = page.get_by_text("Ekspert").is_checked()
        print(f"Expert tips? {is_checked}")

        # Extract data from each row in the table body
        data = []
        rows = page.locator("table tbody tr:not([aria-hidden='true'])").all()

        for row in rows:
            match_cells = row.locator("th button div span")
            match = match_cells.nth(0).inner_text()

            probabilities_cells = row.locator("td div fieldset label span span").all()

            probabilities = []
            for probability in probabilities_cells:
                probabilities.append(probability.inner_text())

            data.append({
                "Match": match,
                "Probabilities": probabilities
            })

        for row in data:
            print(row)

        browser.close()


if __name__ == "__main__":
    scrape_table()
