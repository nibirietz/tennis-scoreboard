from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import override
from uuid import UUID

from tennis_scoreboard.exceptions import IdenticalPlayers, MatchUnknownPlayer


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


    @override
    def __eq__(self, other: Player) -> bool:
        return self.name == other.name


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

    def _reset_game_points(self):
        self._game_points = [0, 0]

    def _reset_set_games(self):
        self._set_games = [0, 0]

    def _set_game_deuce(self):
        self._game_points = [3, 3]

    def _is_deuce(self) -> bool:
        return self._game_points[Side.FIRST] == self._game_points[Side.SECOND] == 4

    def _is_winning_game(self, side: Side) -> bool:
        return (
            self._game_points[side] == 4 and self._game_points[side.opponent] != 3
        ) or self._game_points[side] == 5

    def _is_tie_break(self) -> bool:
        return self._set_games[Side.FIRST] == self._set_games[Side.SECOND] == 6

    def _is_winning_tie_break(self, side: Side) -> bool:
        return self._game_points[side] == 7

    def add_point(self, side: Side):
        self._game_points[side] += 1
        if self._is_tie_break():
            if self._is_winning_tie_break(side):
                self._reset_game_points()
                self._add_game(side)
        else:
            if self._is_deuce():
                self._set_game_deuce()
            elif self._is_winning_game(side):
                self._reset_game_points()
                self._add_game(side)

    def _is_winning_set(self, side: Side) -> bool:
        return (
            self._set_games[side] == 6 and self._set_games[side.opponent] != 5
        ) or self._set_games[side] == 7

    def _add_game(self, side: Side):
        self._set_games[side] += 1
        if self._is_winning_set(side):
            self._reset_set_games()
            self._add_set(side)

    def _add_set(self, side: Side):
        self._match_sets[side] += 1


@dataclass
class Match:
    uuid: UUID
    player1: Player
    player2: Player
    score: Score

    @classmethod
    def new(cls, uuid: UUID, player1: Player, player2: Player) -> Match:
        if player1 == player2:
            raise IdenticalPlayers
        return cls(uuid=uuid, player1=player1, player2=player2, score=Score.new())

    @property
    def winner(self) -> Player | None:
        if self.score.get_sets(Side.FIRST) == 2:
            return self.player1
        if self.score.get_sets(Side.SECOND) == 2:
            return self.player2

    def add_point(self, player: Player):
        if player.id == self.player1.id:
            side = Side.FIRST
        elif player.id == self.player2.id:
            side = Side.SECOND
        else:
            raise MatchUnknownPlayer("Неизвестный участник матча.")
        if self.winner is None:
            self.score.add_point(side)
