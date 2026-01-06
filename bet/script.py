import configparser
import json

from prettytable import PrettyTable
from pydantic import TypeAdapter
from pydantic.json import pydantic_encoder

from common.domain import Match, Bet, Result


def run(args):
    filename = args.filename
    balance = args.balance

    config = configparser.ConfigParser()
    config.read('config.ini')

    try:
        min_expected_value = float(config['Betting']['min_expected_value'])
        max_odds = float(config['Betting']['max_odds'])
        kelly_fraction = float(config['Betting']['kelly_fraction'])
    except KeyError as e:
        print(f"Error loading configuration: Missing key {e}")
        return
    except ValueError as e:
        print(f"Error loading configuration: Invalid value {e}")
        return
    except Exception as e:
        print(f"Error loading configuration: {e}")

        min_expected_value = 0.05
        max_odds = 4.0
        kelly_fraction = 0.5
        print(
            f"Using default values: min_expected_value={min_expected_value}, max_odds={max_odds}, kelly_fraction={kelly_fraction}")

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
                            odds=match.odds.home_win,
                            expected_value=match.expected_value.home_win, bet_fraction=match.bet_fraction.home_win))
        if match.expected_value.tie > 0:
            bets.append(Bet(home_team=match.home_team.name, away_team=match.away_team.name, prediction=Result.T,
                            odds=match.odds.tie,
                            expected_value=match.expected_value.tie, bet_fraction=match.bet_fraction.tie))
        if match.expected_value.away_win > 0:
            bets.append(Bet(home_team=match.home_team.name, away_team=match.away_team.name, prediction=Result.A,
                            odds=match.odds.away_win,
                            expected_value=match.expected_value.away_win, bet_fraction=match.bet_fraction.away_win))

    bets.sort(key=lambda b: b.bet_fraction, reverse=True)

    table = PrettyTable()

    table.field_names = ["Home team", "Away team", "Result", "Odds", "Expected Value", "Bet Fraction", "Balance",
                         "Bet Amount", "Prize"]

    for bet in bets:
        if bet.expected_value < min_expected_value or bet.odds > max_odds:
            continue

        bet_amount = int((bet.bet_fraction * kelly_fraction) * balance)
        prize = int(bet.odds * bet_amount)

        table.add_row(
            [bet.home_team, bet.away_team, bet.prediction.value, bet.odds, bet.expected_value, bet.bet_fraction,
             balance, bet_amount, prize])

        balance -= bet_amount

    print(table)
