from datetime import datetime
from enum import Enum
from typing import Annotated, Optional

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


class Odds(BaseModel):
    home_win: Annotated[float, Field(ge=1.0)]
    tie: Annotated[float, Field(ge=1.0)]
    away_win: Annotated[float, Field(ge=1.0)]


class ExpectedValue(BaseModel):
    home_win: float
    tie: float
    away_win: float

    def is_greater_than(self, baseline: float) -> bool:
        return (self.home_win > baseline) or (self.tie > baseline) or (self.away_win > baseline)


class BetFraction(BaseModel):
    home_win: Optional[float] = None
    tie: Optional[float] = None
    away_win: Optional[float] = None


class Match(BaseModel):
    home_team: Team
    away_team: Team
    match_time: Optional[datetime] = None
    scrape_time: datetime = datetime.now()
    probability: Probability
    odds: Optional[Odds] = None
    expected_value: Optional[ExpectedValue] = None
    bet_fraction: Optional[BetFraction] = None

    def teams_string(self) -> str:
        return f"{self.home_team.name} - {self.away_team.name}"
