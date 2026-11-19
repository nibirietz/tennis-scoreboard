from os import getenv

from dotenv import load_dotenv
from waitress import serve

from tennis_scoreboard.server import application
from wsgi import Application, Response, Router
from wsgi.response import HTMLResponse


def main(application, server_port):
    serve(application, host="0.0.0.0", port=server_port)


if __name__ == "__main__":
    load_dotenv()
    server_port = getenv("BACKEND_PORT")
    router = Router()
    app = Application(router)

    @router.get("/")
    def home():
        body = "<h1>Hello, World!</h1>"
        response = HTMLResponse(body, "200 OK")
        return response

    @router.get("/test")
    def test(a: str):
        response = Response(a, "200 OK", "json")
        return response

    @router.get("/tests")
    def tests(b: list[str]):
        return Response(b, "200 OK", "json")

    main(app, server_port)
