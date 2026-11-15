from uuid import uuid4

from tennis_scoreboard.domain.models import Match, Player, Score, Side

player1 = Player(1, "Alex")
player2 = Player(2, "Michael")


def test_add_point():
    match = Match.new(uuid4(), player1, player2)
    match.add_point(player1)
    assert match.score.get_points(Side.FIRST) == 1
    assert match.score.get_points(Side.SECOND) == 0


def test_get_winner_returns_none():
    score = Score([0, 0], [0, 0], [1, 1])
    match = Match(uuid4(), player1, player2, score)
    assert match.winner is None


def test_get_winner():
    score = Score([0, 0], [0, 0], [2, 1])
    match = Match(uuid4(), player1, player2, score)
    assert match.winner == player1

def test_add_point_failed_after_indetefication_winner():
    score = Score([0, 0], [0, 0], [2, 1])
    match = Match(uuid4(), player1, player2, score)
    assert match.winner == player1
    match.add_point(player2)
    assert match.score.get_points(Side.FIRST) == 0
    assert match.score.get_points(Side.SECOND) == 0
