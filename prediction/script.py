import json

from pydantic import TypeAdapter
from pydantic.json import pydantic_encoder

from common.domain import Match
from prediction import expected_value, kelly_criterion


def run(args):
    filename = args.filename

    with open(filename, "r") as f:
        data = json.load(f)

    match_list_adapter = TypeAdapter(list[Match])

    matches = match_list_adapter.validate_python(data)

    for match in matches:
        if match.odds is not None:
            expected_value.compute(match)

        if match.expected_value is not None:
            kelly_criterion.compute(match)

    with open(filename, "w") as f:
        json.dump(matches, f, default=pydantic_encoder)
