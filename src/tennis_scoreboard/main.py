from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
from waitress import serve

from tennis_scoreboard.server import application
from wsgi import Application, Response, Router
from wsgi.response import HTMLResponse

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

    @router.get("/")
    def main_page():
        template = templates.get_template("index.html")

        html = template.render()
        body = html.encode("utf-8")
        response = HTMLResponse(body, "200 OK")
        return response

    @router.get("/new-match")
    def new_match():
        template = templates.get_template("new-match.html")

        html = template.render()
        body = html.encode("utf-8")
        response = HTMLResponse(body, "200 OK")
        return response

    @router.post("/new-match")
    def new_match(player1_name: str, player2_name: str):
        return Response("", "302 Found", "")

    main(app, server_port)
