from uuid import uuid4

from tennis_scoreboard.domain.match_service import MatchService


def test_create_new_match(match_service: MatchService):
    uuid = uuid4()
    player1_name = "Alex"
    player2_name = "Michael"
    match_service.new_match(uuid, player1_name, player2_name)
    match = match_service.get_match(uuid)
    assert match.player1_name == player1_name
    assert match.player2_name == player2_name

    
