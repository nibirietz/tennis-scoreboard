import pytest


class FakeRepository:
    def get_by_id(self, id: int):
        return None


@pytest.fixture
def repository() -> FakeRepository:
    return FakeRepository()
