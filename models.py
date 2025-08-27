from enum import Enum
from typing import Annotated

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
