class Response:
    def __init__(
        self,
        body: str | bytes | None,
        status: str,
        content_type: str | None,
        headers: list[tuple[str, str]] | None = None,
    ):
        if isinstance(body, str):
            self.body: bytes = body.encode("utf-8")
        elif isinstance(body, bytes):
            self.body = body
        else:
            self.body = b""
        self.status: str = status
        if headers:
            self.headers: list[tuple[str, str]] = headers
        else:
            self.headers = []
        if content_type:
            self.headers.append(("Content-Type", content_type))


class HTMLResponse(Response):
    def __init__(self, body: str | bytes | None, status: str):
        super().__init__(body, status, "text/html; charset=utf-8")


class RedirectResponse(Response):
    def __init__(self, path: str):
        super().__init__(None, "302 Founded", None, [("Location", path)])
