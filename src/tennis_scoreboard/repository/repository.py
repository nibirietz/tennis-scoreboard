from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import or_

from tennis_scoreboard.domain.models import Match, Player, Score, Side
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

    def score_to_dict(self, score: Score) -> dict[str, list[int]]:
        return {
            "game_points": [
                score.get_points(Side.FIRST),
                score.get_points(Side.SECOND),
            ],
            "set_games": [score.get_games(Side.FIRST), score.get_games(Side.SECOND)],
            "match_sets": [score.get_sets(Side.FIRST), score.get_sets(Side.SECOND)],
        }

    def match_to_orm(self, match: Match):
        return MatchORM(
            uuid=match.uuid,
            player1_id=match.player1.id,
            player2_id=match.player2.id,
            winner_id=match.winner.id if match.winner is not None else None,
            score=self.score_to_dict(match.score),
        )

    def get_match_by_uuid(self, uuid: UUID) -> Match | None:
        stmt = (
            select(MatchORM)
            .options(joinedload(MatchORM.player1), joinedload(MatchORM.player2))
            .where(MatchORM.uuid == uuid)
        )
        match = self.session.scalar(stmt)
        if match:
            return self.match_to_model(match)


    def get_player(self, name: str) -> Player | None:
        stmt = select(PlayerORM).where(PlayerORM.name == name)
        player = self.session.scalars(stmt).one_or_none()
        if player:
            return self.player_to_model(player)

    def create_player(self, name: str):
        player_orm = PlayerORM(name=name)
        self.session.add(player_orm)
        self.session.flush()
        return self.player_to_model(player_orm)

    def create_match(self, match: Match):
        match_orm = self.match_to_orm(match)
        self.session.add(match_orm)
        self.session.flush()
        return match

    def update_match_score(self, match: Match) -> Match:
        stmt = (
            update(MatchORM)
            .where(MatchORM.uuid == match.uuid)
            .values(
                score=self.score_to_dict(match.score),
                winner_id=match.winner.id if match.winner is not None else None,
            )
        )
        _ = self.session.execute(stmt)
        self.session.flush()
        return match

    def get_matches(self, page: int, filtered_by: str | None) -> list[Match]:
        stmt = (
            select(MatchORM)
            .order_by(MatchORM.id)
            .where(MatchORM.winner_id.is_not(None))
            .options(
                joinedload(MatchORM.player1),
                joinedload(MatchORM.player2),
            )
        )
        if filtered_by:
            stmt = stmt.where(
                or_(
                    MatchORM.player1.has(PlayerORM.name == filtered_by),
                    MatchORM.player2.has(PlayerORM.name == filtered_by),
                )
            )
        stmt = stmt.limit(5).offset((page - 1) * 5)
        matches_orm = self.session.scalars(stmt).all()
        matches = [self.match_to_model(match) for match in matches_orm]
        return matches
