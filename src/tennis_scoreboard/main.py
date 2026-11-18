import os

from dotenv import load_dotenv
from waitress import serve

from tennis_scoreboard.server import application
from wsgi import Application, Router


def main(application, server_port):
    serve(application, host="0.0.0.0", port=server_port)


if __name__ == "__main__":
    load_dotenv()
    server_port = os.getenv("BACKEND_PORT")
    router = Router()
    app = Application(router)

    @router.get("/")
    def home():
        return b"Hello, World!"


    @router.get("/test")
    def test(a: str):
        return a.encode()

    @router.get("/tests")
    def tests(b: list[str]):
        return b
    
    main(app, server_port)
