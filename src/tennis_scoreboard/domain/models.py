from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Player:
    id: int
    name: str


@dataclass
class Score:
    game_points: list[int]
    set_games: list[int]
    match_sets: list[int]

    @classmethod
    def new(cls):
        return cls(
            game_points=[0, 0],
            set_games=[0, 0],
            match_sets=[0, 0],
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
