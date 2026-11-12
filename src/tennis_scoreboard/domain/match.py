from dataclasses import dataclass


@dataclass
class Match:
    player1_id: int
    player2_id: int
    score: dict[int, int]
