from common import Match, ExpectedValue


def compute(match: Match):
    if match.odds is None:
        return None

    home_win = round((match.odds.home_win * (match.probability.home_win / 100)) - 1, 3)
    tie = round((match.odds.tie * (match.probability.away_win / 100)) - 1, 3)
    away_win = round((match.odds.away_win * (match.probability.away_win / 100)) - 1, 3)

    match.expected_value = ExpectedValue(
        home_win=home_win,
        tie=tie,
        away_win=away_win
    )

    return None
