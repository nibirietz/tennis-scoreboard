from contextlib import contextmanager
from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session, sessionmaker
from waitress import serve

from tennis_scoreboard.controller import register_routers
from tennis_scoreboard.domain.match_service import MatchService
from wsgi import Application, Router

BASE_DIR = Path(__file__).resolve().parent

templates = Environment(
    loader=FileSystemLoader(BASE_DIR / "templates"),
    autoescape=select_autoescape(["html"]),
)


def main(app, server_port):
    serve(app, host="0.0.0.0", port=server_port)


if __name__ == "__main__":
    _ = load_dotenv()
    server_port = getenv("BACKEND_PORT")
    router = Router()

    db_url = URL.create(
        drivername="postgresql+psycopg",
        username=getenv("DB_USER"),
        password=getenv("DB_PASSWORD"),
        host=getenv("DB_HOST", "localhost"),
        port=int(getenv("DB_PORT", "5432")),
        database=getenv("POSTGRES_DB"),
    )

    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    @contextmanager
    def get_session():
        session: Session = SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    service = MatchService(get_session)
    register_routers(router, service, templates)
    app = Application(router, BASE_DIR / "static", BASE_DIR / "templates")

    main(app, server_port)
