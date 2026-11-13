from dataclasses import dataclass
from enum import IntEnum
from typing import Self
from uuid import UUID


class Side(IntEnum):
    FIRST = 0
    SECOND = 1


@dataclass(frozen=True, slots=True)
class Player:
    id: int
    name: str


@dataclass
class Score:
    _game_points: list[int]
    _set_games: list[int]
    _match_sets: list[int]

    @classmethod
    def new(cls) -> Self:
        return cls(
            _game_points=[0, 0],
            _set_games=[0, 0],
            _match_sets=[0, 0],
        )

    def get_points(self, side: Side):
        return self._game_points[side]
        

    def add_points(self, side: Side):
        self._game_points[side] += 1



@dataclass
class Match:
    uuid: UUID
    player1: Player
    player2: Player
    winner: Player | None
    score: Score

    @classmethod
    def new(cls, uuid: UUID, player1: Player, player2: Player) -> Self:
        return cls(
            uuid=uuid, player1=player1, player2=player2, winner=None, score=Score.new()
        )
