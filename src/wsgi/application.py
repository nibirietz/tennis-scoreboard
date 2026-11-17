from collections.abc import Callable, Iterable
from urllib.parse import parse_qs, urlparse

from wsgi.router import Router


class Application:
    def __init__(self, router: Router):
        self.router: Router = router

    def __call__(
        self,
        environ: dict[str, object],
        start_response: Callable[..., Callable[[bytes], None]],
    ) -> Iterable[bytes]:
        path = environ.get("PATH_INFO", "")
        method = environ.get("REQUEST_METHOD", "")
        result = self.router.handle(path, method)
        _ = start_response("200 OK", [("Content-type", "text/plain; charset=utf-8")])
        print(path, self.router.routes)
        yield result


if __name__ == "__main__":
    router = Router()
    app = Application(router)


# TODO:Все функции при создании с декоратором добавляют роуты в список. В __call__ мы вызываем роутер, который получает путь и вызывает нужную функцию.
