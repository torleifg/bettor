from scrape_probabilities import scrape_table, Coupon

if __name__ == '__main__':
    matches = scrape_table(Coupon.MIDWEEK)

    for match in matches:
        print(match)
