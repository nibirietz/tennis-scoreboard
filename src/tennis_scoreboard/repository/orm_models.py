from uuid import UUID

from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class PlayerORM(Base):
    __tablename__ = "players"  # pyright: ignore[reportUnannotatedClassAttribute]

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, index=True)


class MatchORM(Base):
    __tablename__ = "matches"  # pyright: ignore[reportUnannotatedClassAttribute]

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(Uuid, unique=True)
    player1_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    player2_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    winner_id: Mapped[int | None] = mapped_column(ForeignKey("players.id"))
    score: Mapped[dict[str, list[int]]] = mapped_column(JSONB)

    player1: Mapped[PlayerORM] = relationship(foreign_keys=[player1_id])
    player2: Mapped[PlayerORM] = relationship(foreign_keys=[player2_id])
    winner: Mapped[PlayerORM | None] = relationship(foreign_keys=[winner_id])
