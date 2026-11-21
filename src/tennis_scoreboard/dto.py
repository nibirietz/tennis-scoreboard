from dataclasses import dataclass


@dataclass(frozen=True)
class ScoreDTO:
    player1_points: str
    player2_points: str
    player1_games: str
    player2_games: str
    player1_sets: str
    player2_sets: str


@dataclass(frozen=True)
class MatchResponse:
    player1_name: str
    player2_name: str
    score: ScoreDTO
    winner_name: str | None
