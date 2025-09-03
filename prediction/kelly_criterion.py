from common.domain import Match, BetFraction


def compute(match: Match):
    home_win = formula(match.expected_value.home_win, match.odds.home_win)
    tie = formula(match.expected_value.tie, match.odds.tie)
    away_win = formula(match.expected_value.away_win, match.odds.away_win)

    match.bet_fraction = BetFraction(
        home_win=home_win,
        tie=tie,
        away_win=away_win
    )


def formula(expected_value: float, odds: float) -> float:
    return round(expected_value / (odds - 1), 3)
