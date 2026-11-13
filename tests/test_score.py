from tennis_scoreboard.domain.models import Score, Side


def test_add_point_in_new_match():
    score = Score.new()
    score.add_points(Side.FIRST)
    assert score.get_points(Side.FIRST) == 1
    assert score.get_points(Side.SECOND) == 0
