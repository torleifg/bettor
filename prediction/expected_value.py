from common.domain import Match, ExpectedValue


def compute(match: Match):
    home_win = formula(match.odds.home_win, match.probability.home_win)
    tie = formula(match.odds.tie, match.probability.tie)
    away_win = formula(match.odds.away_win, match.probability.away_win)

    match.expected_value = ExpectedValue(
        home_win=home_win,
        tie=tie,
        away_win=away_win
    )


def formula(odds: float, probability: int) -> float:
    return round((odds * (probability / 100)) - 1, 3)
