from contextlib import contextmanager
from os import getenv
from pathlib import Path
from uuid import UUID, uuid4

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session, sessionmaker
from waitress import serve

from tennis_scoreboard.domain.match_service import MatchService
from tennis_scoreboard.repository.repository import SQLAlchemyRepository
from tennis_scoreboard.server import application
from wsgi import Application, Response, Router
from wsgi.response import HTMLResponse, RedirectResponse

BASE_DIR = Path(__file__).resolve().parent

templates = Environment(
    loader=FileSystemLoader(BASE_DIR / "templates"),
    autoescape=select_autoescape(["html"]),
)


def main(application, server_port):
    serve(application, host="0.0.0.0", port=server_port)


if __name__ == "__main__":
    load_dotenv()
    server_port = getenv("BACKEND_PORT")
    router = Router()
    app = Application(router, BASE_DIR / "static", BASE_DIR / "templates")
    

    db_url = URL.create(
        drivername="postgresql+psycopg",
        username=getenv("DB_USER"),
        password=getenv("DB_PASSWORD"),
        host=getenv("DB_HOST", "localhost"),
        port=int(getenv("DB_PORT", 5432)),
        database=getenv("POSTGRES_DB"),
    )
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    @contextmanager
    def get_session():
        session: Session = SessionLocal()
        try:
            yield session
        finally:
            session.close()


    service = MatchService(get_session)


    @router.get("/")
    def main_page():
        template = templates.get_template("index.html")

        html = template.render()
        body = html.encode("utf-8")
        response = HTMLResponse(body, "200 OK")
        return response

    @router.get("/new-match")
    def match():
        template = templates.get_template("new-match.html")

        html = template.render()
        body = html.encode("utf-8")
        response = HTMLResponse(body, "200 OK")
        return response

    @router.post("/new-match")
    def new_match(player1_name: str, player2_name: str):
        uuid = uuid4()
        service.new_match(player1_name, player2_name, uuid)
        return RedirectResponse(f"/match?uuid={uuid}")

    @router.get("/match")
    def match_score(uuid: str):
        template = templates.get_template("match-score.html")

        print(service.get_match(UUID(uuid)))

        html = template.render()
        body = html.encode("utf-8")
        response = HTMLResponse(body, "200 OK")
        return response

    main(app, server_port)
