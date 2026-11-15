from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from uuid import UUID


class Side(IntEnum):
    FIRST = 0
    SECOND = 1

    @property
    def opponent(self) -> Side:
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
    def new(cls) -> Score:
        return cls(
            _game_points=[0, 0],
            _set_games=[0, 0],
            _match_sets=[0, 0],
        )

    def get_points(self, side: Side) -> int:
        return self._game_points[side]

    def get_games(self, side: Side) -> int:
        return self._set_games[side]

    def get_sets(self, side: Side) -> int:
        return self._match_sets[side]

    def reset_game_points(self):
        self._game_points = [0, 0]

    def reset_set_games(self):
        self._set_games = [0, 0]

    def set_game_deuce(self):
        self._game_points = [3, 3]

    def is_deuce(self) -> bool:
        return self._game_points[Side.FIRST] == self._game_points[Side.SECOND] == 4

    def is_winning_game(self, side: Side) -> bool:
        return (
            self._game_points[side] == 4 and self._game_points[side.opponent] != 3
        ) or self._game_points[side] == 5

    def is_tie_break(self) -> bool:
        return self._set_games[Side.FIRST] == self._set_games[Side.SECOND] == 6

    def is_winning_tie_break(self, side: Side) -> bool:
        return (
            self._game_points[side] >= 7
            and self._game_points[side] - self._game_points[side.opponent] >= 2
        )

    def add_points(self, side: Side):
        self._game_points[side] += 1
        if self.is_tie_break():
            if self.is_winning_tie_break(side):
                self.reset_game_points()
                self.add_game(side)
        else:
            if self.is_deuce():
                self.set_game_deuce()
            elif self.is_winning_game(side):
                self.reset_game_points()
                self.add_game(side)

    def is_winning_set(self, side: Side) -> bool:
        return (
            self._set_games[side] == 6 and self._set_games[side.opponent] != 5
        ) or self._set_games[side] == 7

    def add_game(self, side: Side):
        self._set_games[side] += 1
        if self.is_winning_set(side):
            self.reset_set_games()
            self.add_set(side)

    def add_set(self, side: Side):
        self._match_sets[side] += 1


@dataclass
class Match:
    uuid: UUID
    player1: Player
    player2: Player
    winner: Player | None
    score: Score

    @classmethod
    def new(cls, uuid: UUID, player1: Player, player2: Player) -> Match:
        return cls(
            uuid=uuid, player1=player1, player2=player2, winner=None, score=Score.new()
        )
