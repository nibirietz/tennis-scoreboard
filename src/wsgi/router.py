from collections.abc import Callable
from typing import ParamSpec, TypeVar

F_Spec = ParamSpec("F_Spec")


class APIRoute:
    def __init__(self, path: str, method: str, func: Callable[F_Spec, bytes]):
        self.path: str = path
        self.method: str = method
        self.func: Callable[..., bytes] = func


class Router:
    def __init__(self):
        self.routes: list[APIRoute] = []

    def add_route(self, func: Callable[F_Spec, bytes], method: str, route: str):
        self.routes.append(APIRoute(route, method, func))

    def get(self, route: str):
        def wrapper(func: Callable[F_Spec, bytes]) -> Callable[F_Spec, bytes]:
            self.add_route(func, "GET", route)
            return func

        return wrapper

    def post(self, route: str):
        def wrapper(func: Callable[F_Spec, bytes]) -> Callable[F_Spec, bytes]:
            self.add_route(func, "POST", route)
            return func

        return wrapper

    def patch(self, route: str):
        def wrapper(func: Callable[F_Spec, bytes]) -> Callable[F_Spec, bytes]:
            self.add_route(func, "PATCH", route)
            return func

        return wrapper

    def handle(self, path: str, method: str, *args, **kwargs) -> bytes:
        for route in self.routes:
            if route.path == path and route.method == method:
                return route.func(*args, **kwargs)
        return b"Not founded"
