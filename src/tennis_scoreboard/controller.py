from uuid import UUID, uuid4

from jinja2 import Environment

from tennis_scoreboard.domain.match_service import MatchService
from tennis_scoreboard.domain.models import Side
from wsgi import Router
from wsgi.response import HTMLResponse, RedirectResponse


def register_routers(router: Router, service: MatchService, templates: Environment):
    def render_template(template_name: str, **kwargs) -> str:
        template = templates.get_template(template_name)
        return template.render(**kwargs)

    @router.get("/")
    def main_page():
        html = render_template("index.html")
        response = HTMLResponse(html, "200 OK")
        return response

    @router.get("/new-match")
    def match():
        html = render_template("new-match.html")
        response = HTMLResponse(html, "200 OK")
        return response

    @router.post("/new-match")
    def new_match(player1_name: str, player2_name: str):
        uuid = uuid4()
        parsed_player1_name = player1_name.strip()
        parsed_player2_name = player2_name.strip()
        for name in (parsed_player1_name, parsed_player2_name):
            if name == "" or len(name) > 30 or len(name) < 2:
                html = render_template(
                    "new-match.html",
                    error="Unavailable name: name must contain 2 to 30 symbols.",
                )
                response = HTMLResponse(html, "400 Bad Request")
                return response
        try:
            service.new_match(uuid, parsed_player1_name, parsed_player2_name)
        except Exception as e:
            html = render_template("new-match.html", error=str(e))
            response = HTMLResponse(html, "409 Conflict")
            return response

        return RedirectResponse(f"/match?uuid={uuid}")

    @router.get("/match")
    def match_score(uuid: str):
        match = service.get_match(UUID(uuid))
        is_active = service.match_is_active(UUID(uuid))
        html = render_template("match-score.html", match=match, uuid=uuid, is_active=is_active)
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
        service.add_point(UUID(uuid), player_side)
        response = RedirectResponse(f"/match?uuid={uuid}")
        return response

    @router.get("/matches")
    def get_matches(page: int = 1, filter_by_player_name: str = ""):
        parsed_filter_by_player_name = (
            None if filter_by_player_name == "" else filter_by_player_name.strip()
        )
        matches = service.get_matches(page, parsed_filter_by_player_name)
        html = render_template(
            "matches.html",
            matches=matches,
            page=page,
            filter_by_player_name=filter_by_player_name,
        )
        response = HTMLResponse(html, "200 OK")
        return response

    @router.post("/matches")
    def post_filter_matches(page: int = 1, filter_by_player_name: str = ""):
        response = RedirectResponse(
            f"/matches?page={page}&filter_by_player_name={filter_by_player_name}"
        )
        return response
