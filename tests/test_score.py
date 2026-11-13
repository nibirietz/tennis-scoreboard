from tennis_scoreboard.domain.models import Score, Side


def test_add_point_in_new_match():
    score = Score.new()
    score.add_points(Side.FIRST)
    assert score.get_points(Side.FIRST) == 1
    assert score.get_points(Side.SECOND) == 0


def test_first_player_wins_game():
    score = Score([3, 2], [0, 0], [0, 0])
    score.add_points(Side.FIRST)
    assert score.get_games(Side.FIRST) == 1
    assert score.get_games(Side.SECOND) == 0
    assert score.get_points(Side.FIRST) == 0
    assert score.get_points(Side.SECOND) == 0


def test_first_player_add_point_in_deuce():
    score = Score([3, 3], [0, 0], [0, 0])
    score.add_points(Side.FIRST)
    assert score.get_points(Side.FIRST) == 4
    assert score.get_points(Side.SECOND) == 3
    assert score.get_games(Side.FIRST) == 0
    assert score.get_games(Side.SECOND) == 0


def test_set_deuce_after_mistake():
    score = Score([4, 3], [0, 0], [0, 0])
    score.add_points(Side.SECOND)
    assert score.get_points(Side.FIRST) == 3
    assert score.get_points(Side.SECOND) == 3
    assert score.get_games(Side.FIRST) == 0
    assert score.get_games(Side.SECOND) == 0
