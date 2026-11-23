from collections.abc import Generator
from contextlib import contextmanager

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.community.postgres import PostgresContainer

from tennis_scoreboard.domain.match_service import MatchService, SessionFactory
from tennis_scoreboard.repository.orm_models import Base


@pytest.fixture(scope="session")
def test_engine() -> Generator[Engine]:
    with PostgresContainer("postgres:18-alpine", driver="psycopg") as postgres:
        engine: Engine = create_engine(postgres.get_connection_url())
        Base.metadata.create_all(engine)
        yield engine
        engine.dispose()


@pytest.fixture(scope="function")
def db_session(test_engine: Engine) -> Generator[Session]:
    connection = test_engine.connect()
    transaction = connection.begin()
    TestSessionLocal = sessionmaker(
        bind=connection,
        autoflush=False,
        autocommit=False,
        join_transaction_mode="create_savepoint",
        expire_on_commit=False,
    )
    session: Session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def get_session(db_session: Session) -> SessionFactory:
    @contextmanager
    def _factory() -> Generator[Session]:
        with db_session.begin_nested():
            yield db_session

    return _factory


@pytest.fixture(scope="function")
def match_service(get_session: SessionFactory) -> MatchService:
    return MatchService(get_session)
