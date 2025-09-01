import argparse
import json

from prettytable import PrettyTable
from pydantic import TypeAdapter
from pydantic.json import pydantic_encoder

from common import Match, Bet, Result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='bets')

    parser.add_argument('--filename', required=True, type=str)
    parser.add_argument('--balance', required=True, type=int)

    args = parser.parse_args()

    filename = args.filename
    balance = args.balance

    with open(filename, "r") as f:
        data = json.load(f)

    match_list_adapter = TypeAdapter(list[Match])

    matches = match_list_adapter.validate_python(data)

    bets = []

    for match in matches:
        if match.bet_fraction is None:
            continue

        if match.expected_value.home_win > 0:
            bets.append(Bet(home_team=match.home_team.name, away_team=match.away_team.name, prediction=Result.H,
                            expected_value=match.expected_value.home_win, bet_fraction=match.bet_fraction.home_win))
        if match.expected_value.tie > 0:
            bets.append(Bet(home_team=match.home_team.name, away_team=match.away_team.name, prediction=Result.T,
                            expected_value=match.expected_value.tie, bet_fraction=match.bet_fraction.tie))
        if match.expected_value.away_win > 0:
            bets.append(Bet(home_team=match.home_team.name, away_team=match.away_team.name, prediction=Result.A,
                            expected_value=match.expected_value.away_win, bet_fraction=match.bet_fraction.away_win))

    bets.sort(key=lambda b: b.expected_value, reverse=True)

    table = PrettyTable()

    table.field_names = ["Home team", "Away team", "Result", "Expected Value", "Bet Fraction", "Balance", "Bet Amount"]

    for bet in bets:
        bet_amount = int(bet.bet_fraction * balance)
        table.add_row(
            [bet.home_team, bet.away_team, bet.prediction.value, bet.expected_value, bet.bet_fraction, balance,
             bet_amount])
        balance -= bet_amount

    print(table)
