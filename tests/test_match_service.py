from uuid import UUID, uuid4

import pytest

from tennis_scoreboard.domain.match_service import MatchService
from tennis_scoreboard.domain.models import Match, Side
from tennis_scoreboard.exceptions import MatchAlreadyExists
from tennis_scoreboard.repository.repository import SQLAlchemyRepository


@pytest.fixture
def default_match_id(match_service: MatchService) -> UUID:
    uuid = uuid4()
    player1_name = "Alex"
    player2_name = "Michael"
    match_service.new_match(uuid, player1_name, player2_name)
    return uuid


def test_create_match_with_exists_players(match_service: MatchService):
    player1_name = "Alex"
    player2_name = "Michael"
    with match_service.session_factory() as session:
        repository = SQLAlchemyRepository(session)
        repository.create_player(player1_name)
        repository.create_player(player2_name)
    uuid = uuid4()
    match_service.new_match(uuid, player1_name, player2_name)
    match = match_service.get_match(uuid)
    assert match is not None
    assert match.player1_name == player1_name
    assert match.player2_name == player2_name


def test_create_new_match_with_non_exists_player(match_service: MatchService):
    uuid = uuid4()
    player1_name = "Alex"
    player2_name = "Michael"
    match_service.new_match(uuid, player1_name, player2_name)
    match = match_service.get_match(uuid)
    assert match is not None
    assert match.player1_name == player1_name
    assert match.player2_name == player2_name


def test_add_point_first_player(match_service: MatchService, default_match_id: UUID):
    match_service.add_point(default_match_id, Side.FIRST)
    match = match_service.get_match(default_match_id)
    assert match is not None
    assert match.score.player1_points == "15"
    assert match.score.player2_points == "0"


def test_create_exists_match(match_service: MatchService, default_match_id: UUID):
    player1_name = "Leha"
    player2_name = "Miha"
    with pytest.raises(MatchAlreadyExists):
        match_service.new_match(default_match_id, player1_name, player2_name)
    match = match_service.get_match(default_match_id)
    assert match is not None
    assert match.player1_name == "Alex"
    assert match.player2_name == "Michael"
