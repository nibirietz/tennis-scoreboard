from collections.abc import Callable, Iterable


def application(environ: dict, start_response: Callable) -> Iterable[bytes]:
    start_response("200 OK", [("Content-Type", "text-plain; charset=utf-8")])
    yield b"Hello, World!"
