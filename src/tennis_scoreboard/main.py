import os

from dotenv import load_dotenv
from waitress import serve

from tennis_scoreboard.server import application


def main(application, server_port):
    serve(application, host="0.0.0.0", port=server_port)


if __name__ == "__main__":
    load_dotenv()
    server_port = os.getenv("BACKEND_PORT")
    app = application
    main(app, server_port)
