import argparse
import os

import bet.script
import match.script
import prediction.script

if __name__ == '__main__':
    os.makedirs("data", exist_ok=True)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    matches = subparsers.add_parser('matches', help="Run matches")
    matches.add_argument('--coupon', required=True, type=str)
    matches.add_argument('--days', nargs="+", required=True, type=int)
    matches.set_defaults(func=match.script.run)

    predictions = subparsers.add_parser('predictions', help="Run predictions")
    predictions.add_argument('--filename', required=True, type=str)
    predictions.set_defaults(func=prediction.script.run)

    bets = subparsers.add_parser('bets', help="Run bets")
    bets.add_argument('--filename', required=True, type=str)
    bets.add_argument('--balance', required=True, type=int)
    bets.set_defaults(func=bet.script.run)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
