from uuid import UUID, uuid4

from jinja2 import Environment

from tennis_scoreboard.domain.match_service import MatchService
from tennis_scoreboard.domain.models import Side
from tennis_scoreboard.exceptions import IdenticalPlayers
from wsgi import Router
from wsgi.response import HTMLResponse, RedirectResponse


def register_routers(router: Router, service: MatchService, templates: Environment):
    def render_template(template_name: str, **kwargs) -> str:
        template = templates.get_template(template_name)
        return template.render(**kwargs)

    @router.get("/")
    def main_page():
        template = templates.get_template("index.html")
        html = template.render()
        response = HTMLResponse(html, "200 OK")
        return response

    @router.get("/new-match")
    def match():
        template = templates.get_template("new-match.html")
        html = template.render()
        response = HTMLResponse(html, "200 OK")
        return response

    @router.post("/new-match")
    def new_match(player1_name: str, player2_name: str):
        uuid = uuid4()
        try:
            service.new_match(uuid, player1_name, player2_name)
        except IdenticalPlayers as e:
            template = templates.get_template("new-match.html")
            html = template.render(error=str(e))
            response = HTMLResponse(html, "409 Conflict")
            return response

        return RedirectResponse(f"/match?uuid={uuid}")

    @router.get("/match")
    def match_score(uuid: str):
        match = service.get_match(UUID(uuid))
        template = templates.get_template("match-score.html")
        html = template.render(match=match, uuid=uuid)
        response = HTMLResponse(html, "200 OK")
        return response

    @router.post("/match")
    def add_point(uuid: str, player_number: int):
        if player_number == 1:
            player_side = Side.FIRST
        elif player_number == 2:
            player_side = Side.SECOND
        else:
            return RedirectResponse(f"/match?uuid={uuid}")
        match = service.add_point(UUID(uuid), player_side)
        html = render_template("match-score.html", match=match, uuid=uuid)
        response = HTMLResponse(html, "201 OK")
        return response

    @router.get("/matches")
    def get_matches(page: int = 1, filter_by_player_name: str | None = None):
        matches = service.get_matches(page, filter_by_player_name)
        html = render_template("matches.html", matches=matches)
        response = HTMLResponse(html, "200 OK")
        return response
