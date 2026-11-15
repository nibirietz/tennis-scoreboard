from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "players"  # pyright: ignore[reportUnannotatedClassAttribute]

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), index=True)


class Match(DeclarativeBase):
    __tablename__ = "matches"  # pyright: ignore[reportUnannotatedClassAttribute]

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(Uuid, default=uuid4)
    player1_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    player2_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    score: Mapped[dict[str, list[int]]] = mapped_column(JSONB)

    player1: Mapped[Player] = relationship(foreign_keys=[player1_id])
    player2: Mapped[Player] = relationship(foreign_keys=[player2_id])
