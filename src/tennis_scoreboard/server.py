from collections.abc import Callable, Iterator


def application(environ: dict, start_response: Callable) -> Iterator:
    start_response("200 OK", [("Content-Type", "text-plain")])
    yield b"Hello, World!"
