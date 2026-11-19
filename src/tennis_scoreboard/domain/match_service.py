from collections.abc import Callable
from contextlib import AbstractContextManager
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from tennis_scoreboard.domain.models import Match
from tennis_scoreboard.exceptions import IdenticalPlayers, MatchAlreadyExists
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

    def get_match(self, uuid: UUID):
        with self.session_factory() as session:
            repository = SQLAlchemyRepository(session)
            return repository.get_match_by_uuid(uuid)
