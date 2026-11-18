from collections.abc import Callable, Iterable
import json
from urllib.parse import parse_qs, urlparse

from wsgi.router import Router


class Application:
    def __init__(self, router: Router):
        self.router: Router = router


    def parse_query(self, environ: dict[str, object]) -> dict[str, list[object]]:
        raw_query_params: dict[str, list[object]] = parse_qs(environ.get("QUERY_STRING", ""))
        return raw_query_params
    

    def __call__(
        self,
        environ: dict[str, object],
        start_response: Callable[..., Callable[[bytes], None]],
    ) -> Iterable[bytes]:
        path: str = environ.get("PATH_INFO", "")
        method: str = environ.get("REQUEST_METHOD", "")
        query_params = self.parse_query(environ)
        result = self.router.handle(path, method, **query_params)
        print(result)
        result = json.dumps(result).encode("utf-8")
        _ = start_response("200 OK", [("Content-type", "text/plain; charset=utf-8")])
        return [result]


if __name__ == "__main__":
    router = Router()
    app = Application(router)
