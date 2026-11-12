from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Player:
    id: int
    name: str


@dataclass(slots=True)
class MatchParticipant:
    player: Player
    score: int


@dataclass
class Match:
    uuid: UUID
    player1: MatchParticipant
    player2: MatchParticipant
    winner: Player | None
