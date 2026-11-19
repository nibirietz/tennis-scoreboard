
from uuid import uuid4

from jinja2 import Environment

from tennis_scoreboard.domain.match_service import MatchService
from tennis_scoreboard.exceptions import IdenticalPlayers
from wsgi import Router
from wsgi.response import HTMLResponse, RedirectResponse


def register_routers(router: Router, service: MatchService, templates: Environment):
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
        try:
            service.new_match(uuid, player1_name, player2_name)
        except IdenticalPlayers:
            template = templates.get_template("new-match.html")
            html = template.render()
            body = html.encode("utf-8")
            response = HTMLResponse(body, "409 Conflict")
            return response

        return RedirectResponse(f"/match?uuid={uuid}")

    @router.get("/match")
    def match_score(uuid: str):
        template = templates.get_template("match-score.html")
        html = template.render()
        body = html.encode("utf-8")
        response = HTMLResponse(body, "200 OK")
        return response
