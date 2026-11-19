from dataclasses import dataclass


@dataclass(frozen=True)
class ScoreDTO:
    player1_points: int
    player2_points: int
    player1_games: int
    player2_games: int
    player1_sets: int
    player2_sets: int

@dataclass(frozen=True)
class MatchResponse:
    player1_name: str
    player2_name: str
    score: ScoreDTO
    winner_name: str | None

