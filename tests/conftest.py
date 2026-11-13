from uuid import UUID, uuid4

import pytest

from tennis_scoreboard.domain.models import Match, Player, Score


class FakeRepository:
    def __init__(self):
        self.players: list[Player] = [Player(1, "Alex"), Player(2, "Michael")]
        self.matches: list[Match] = [
            Match(
                uuid=uuid4(),
                player1=Player(1, "Alex"),
                player2=Player(2, "Michael"),
                winner=None,
                score=Score([0, 0], [0, 0]),
            )
        ]

    def get_player_by_name(self, name: str) -> Player | None:
        for player in self.players:
            if player.name == name:
                return player

    def get_match_by_uuid(self, uuid: UUID) -> Match | None: ...

    def add_match(self, match: Match): ...

    def update_match(self, match: Match): ...

    def add_player(self, name: str): ...

    def get_player_by_id(self, id: int) -> Player: ...


@pytest.fixture
def repository() -> FakeRepository:
    return FakeRepository()
