from uuid import uuid4

from tennis_scoreboard.domain.models import Match, Player, Score, Side

player1 = Player(1, "Alex")
player2 = Player(2, "Michael")


def test_add_point():
    match = Match.new(uuid4(), player1, player2)
    match.add_point(player1)
    assert match.score.get_points(Side.FIRST) == 1
    assert match.score.get_points(Side.SECOND) == 0
