from typing import Protocol


class RepositoryProtocol(Protocol):
    def get_by_id(self, id: int):
        pass
