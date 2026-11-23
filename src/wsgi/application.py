import json
import mimetypes
from collections.abc import Callable, Iterable
from pathlib import Path
from urllib.parse import parse_qs

from wsgi.response import Response
from wsgi.router import Router


class Application:
    def __init__(self, router: Router, static_dir: Path, templates_dir: Path):
        self.router: Router = router
        self.static_dir: Path = static_dir
        self.templates_dir: Path = templates_dir

    def parse_query(self, environ: dict[str, object]) -> dict[str, list[object]]:
        raw_query_params: dict[str, list[object]] = parse_qs(
            environ.get("QUERY_STRING", "")
        )
        return raw_query_params

    def send_response(
        self,
        start_response,
        body: bytes,
        headers: list[tuple[str, str]],
        status: str = "200 OK",
    ) -> Iterable[bytes]:
        if body != b"":
            headers.append(("Content-Length", str(len(body))))
        start_response(status, headers)
        return [body]

    def serve_static(self, path: str, start_response) -> Iterable[bytes]:
        relative_path = path.removeprefix("/static/")
        file_path = (self.static_dir / relative_path).resolve()

        if not file_path.is_relative_to(self.static_dir.resolve()):
            start_response("403 Forbidden", [])
            return [b"Forbidden"]

        if not file_path.is_file():
            start_response("404 Not Found", [])
            return [b"Not Found"]

        content = file_path.read_bytes()

        content_type, _ = mimetypes.guess_type(file_path.name)

        start_response(
            "200 OK",
            [
                ("Content-Type", content_type or "application/octet-stream"),
                ("Content-Length", str(len(content))),
            ],
        )

        return [content]

    def __call__(
        self,
        environ: dict[str, object],
        start_response: Callable[..., Callable[[bytes], None]],
    ) -> Iterable[bytes]:
        path: str = environ.get("PATH_INFO", "")
        method: str = environ.get("REQUEST_METHOD", "")
        query_params = self.parse_query(environ)
        if "/static/" in path and method == "GET":
            body = self.serve_static(path, start_response)
            return body

        try:
            if method == "GET":
                result = self.router.handle(path, method, **query_params)
                return self.send_response(
                    start_response, result.body, result.headers, result.status
                )
            if method == "POST":
                content_length = int(environ.get("CONTENT_LENGTH", 0))
                post_body = (
                    environ.get("wsgi.input", "").read(content_length).decode("utf-8")
                )
                form_data = parse_qs(post_body)
                params = query_params | form_data
                result = self.router.handle(path, method, **params)
                return self.send_response(
                    start_response, result.body, result.headers, result.status
                )

        except Exception as e:
            message = {"message": str(e)}
            response = Response(
                json.dumps(message),
                "500 Internal Server Error",
                "application/json; charset=utf-8",
            )
            return self.send_response(
                start_response,
                json.dumps(message).encode("utf-8"),
                response.headers,
                response.status,
            )


if __name__ == "__main__":
    router = Router()
    app = Application(router)
