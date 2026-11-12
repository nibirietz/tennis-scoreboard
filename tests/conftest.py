import uuid

import pytest

from tennis_scoreboard.domain.models import Match, MatchParticipant, Player


class FakeRepository:
    def __init__(self):
        self.matches: list[dict] = [
            {
                "id": 1,
                "uuid": uuid.uuid4(),
                "player1_id": 1,
                "player2_id": 2,
                "winner": None,
                "score": {
                    ...
                },
            },
            {
                "id": 2,
                "uuid": uuid.uuid4(),
                "player1_id": 2,
                "player2_id": 1,
                "winner": 2,
                "score": {
                    ...
                },
            },
        ]
        self.players: list[dict] = [
            {"id": 1, "name": "Alex"},
            {"id": 2, "name": "Michael"},
        ]

    def to_domain_player(self, player: dict) -> Player:
        return Player(player["id"], player["name"])

    def get_player_by_name(self, name: str) -> Player | None:
        for player in self.players:
            if player["name"] == name:
                return self.to_domain_player(player)

    def to_domain_match(self, match: dict) -> Match:
        match_uuid = match["uuid"]
        player1 = self.get_player_by_id(match["player1_id"])
        participant1 = MatchParticipant(player, match["score"][...])
        player2 = self.get_player_by_id(match["player2_id"])
        participant2 = MatchParticipant(player, match["score"][...])
        winner = self.get_player_by_id(match["winner"])
        return Match(match_uuid, player1, player2, winner)

    def get_match_by_id(self, id: int) -> Match | None:
        for match in self.matches:
            if match["id"] == id:
                return self.to_domain_match(match)

    def get_match_by_uuid(self, uuid: uuid.UUID) -> Match | None: ...

    def add_match(self, match: Match): ...

    def update_match(self, match: Match): ...

    def add_player(self, name: str): ...

    def get_player_by_id(self, id: int) -> Player: ...


@pytest.fixture
def repository() -> FakeRepository:
    return FakeRepository()
