from collections.abc import Callable
from contextlib import AbstractContextManager
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from tennis_scoreboard.domain.models import Match, Side
from tennis_scoreboard.dto import MatchResponse
from tennis_scoreboard.exceptions import MatchAlreadyExists, MatchNonExists
from tennis_scoreboard.mapper import MatchMapper
from tennis_scoreboard.repository.repository import SQLAlchemyRepository

SessionFactory = Callable[[], AbstractContextManager[Session]]


class MatchService:
    def __init__(self, session_factory: SessionFactory):
        self.session_factory: SessionFactory = session_factory

    def new_match(self, uuid: UUID, player1_name: str, player2_name: str):
        try:
            with self.session_factory() as session:
                repository = SQLAlchemyRepository(session)
                player1 = repository.get_player(player1_name)
                if player1 is None:
                    player1 = repository.create_player(player1_name)
                player2 = repository.get_player(player2_name)
                if player2 is None:
                    player2 = repository.create_player(player2_name)
                match = Match.new(uuid, player1, player2)
                repository.create_match(match)
                session.commit()
        except IntegrityError:
            raise MatchAlreadyExists("Матч уже существует.")

    def get_match(self, uuid: UUID) -> MatchResponse | None:
        with self.session_factory() as session:
            repository = SQLAlchemyRepository(session)
            match = repository.get_match_by_uuid(uuid)
            if match:
                return MatchMapper.match_to_response(match)

    def add_point(self, uuid: UUID, player_side: Side):
        with self.session_factory() as session:
            repository = SQLAlchemyRepository(session)
            match = repository.get_match_by_uuid(uuid)
            if not match:
                raise MatchNonExists("Матч не существует.")
            if player_side == Side.FIRST:
                player = match.player1
            elif player_side == Side.SECOND:
                player = match.player2
            match.add_point(player)
            repository.update_match_score(match)
            session.commit()

    def get_matches(self, page: int, filtered_by: str | None) -> list[MatchResponse]:
        with self.session_factory() as session:
            repository = SQLAlchemyRepository(session)
            matches = repository.get_matches(page, filtered_by)
            return [MatchMapper.match_to_response(match) for match in matches]
