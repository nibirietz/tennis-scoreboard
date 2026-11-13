from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Player:
    id: int
    name: str


@dataclass
class Score:
    game: list[int]
    sets: list[int]


@dataclass
class Match:
    uuid: UUID
    player1: Player
    player2: Player
    winner: Player | None
    score: Score
