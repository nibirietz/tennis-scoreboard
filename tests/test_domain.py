from tennis_scoreboard.repository.repository_protocol import RepositoryProtocol


def test_get_by_id_match(repository: RepositoryProtocol):
    match = repository.get_match_by_id(1)
    assert match
