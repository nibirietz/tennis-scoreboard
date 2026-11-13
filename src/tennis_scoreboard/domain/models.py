from dataclasses import dataclass
from enum import IntEnum
from typing import Self
from uuid import UUID


class Side(IntEnum):
    FIRST = 0
    SECOND = 1

    @property
    def opponent(self):
        return Side(1 - self.value)


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

    def get_points(self, side: Side) -> int:
        return self._game_points[side]
        

    def get_games(self, side: Side) -> int:
        return self._set_games[side]

    def reset_game_points(self):
        self._game_points = [0, 0]
    
    def set_game_deuce(self):
        self._game_points = [3, 3]
    

    def add_points(self, side: Side):
        self._game_points[side] += 1
        if self._game_points[side] == 4 and self._game_points[side.opponent] == 4:
            self.set_game_deuce()
        elif self._game_points[side] == 4 and self._game_points[side.opponent] != 3:
            self.reset_game_points()
            self.add_game(side)

    def add_game(self, side: Side):
        self._set_games[side] += 1



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
