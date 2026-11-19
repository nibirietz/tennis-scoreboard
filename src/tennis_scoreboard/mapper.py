from tennis_scoreboard.domain.models import Match, Side
from tennis_scoreboard.dto import MatchResponse, ScoreDTO


class MatchMapper:
    @staticmethod
    def game_points_to_view(point: int) -> int:
        match point:
            case 0:
                return 0
            case 1:
                return 15
            case 2:
                return 30
            case 3:
                return 40
            case _:
                return -1
    
    @staticmethod
    def match_to_response(match: Match) -> MatchResponse:
        score = ScoreDTO(
            MatchMapper.game_points_to_view(match.score.get_points(Side.FIRST)),
            MatchMapper.game_points_to_view(match.score.get_points(Side.SECOND)),
            match.score.get_games(Side.FIRST),
            match.score.get_games(Side.SECOND),
            match.score.get_sets(Side.FIRST),
            match.score.get_sets(Side.SECOND),
        )
        return MatchResponse(
            match.player1.name,
            match.player2.name,
            score,
            match.winner.name if match.winner else None
        )
        
