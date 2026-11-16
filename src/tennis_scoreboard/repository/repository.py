from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from tennis_scoreboard.domain.models import Match, Player, Score
from tennis_scoreboard.repository.orm_models import MatchORM, PlayerORM


class SQLAlchemyRepository:
    def __init__(self, session: Session):
        self.session: Session = session

    def player_to_model(self, player: PlayerORM) -> Player:
        return Player(
            id=player.id,
            name=player.name,
        )

    def score_to_model(self, score: dict[str, list[int]]):
        return Score(
            score["game_points"],
            score["set_games"],
            score["match_sets"],
        )

    def match_to_model(self, match: MatchORM) -> Match:
        return Match(
            uuid=match.uuid,
            player1=self.player_to_model(match.player1),
            player2=self.player_to_model(match.player2),
            score=self.score_to_model(match.score),
        )

    def get_match_by_uuid(self, uuid: UUID) -> Match:
        stmt = select(MatchORM).where(MatchORM.uuid == uuid)
        match = self.session.scalars(stmt).one()
        return self.match_to_model(match)
