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

    @classmethod
    def new(cls):
        return cls(
            game=[0, 0],
            sets=[0, 0],
        )


@dataclass
class Match:
    uuid: UUID
    player1: Player
    player2: Player
    winner: Player | None
    score: Score

    @classmethod
    def new(cls, uuid: UUID, player1: Player, player2: Player):
        return cls(
            uuid=uuid, player1=player1, player2=player2, winner=None, score=Score.new()
        )
