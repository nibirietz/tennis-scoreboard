class Response:
    def __init__(self, body: str | bytes, status: str, content_type: str):
        self.body: bytes = body.encode("utf-8") if isinstance(body, str) else body
        self.status: str = status
        self.content_type: str = content_type

class HTMLResponse(Response):
    def __init__(self, body: str | bytes, status: str):
        super().__init__(body, status, "text/html; charset=utf-8")
