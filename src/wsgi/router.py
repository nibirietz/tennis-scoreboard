from collections.abc import Callable
from typing import ParamSpec, TypeVar

F_Spec = ParamSpec("F_Spec")
F_Return = TypeVar("F_Return")


class APIRoute:
    def __init__(self, path: str, func: Callable[F_Spec, F_Return]):
        self.path: str = path
        self.func: Callable[..., object] = func


class Router:
    def __init__(self):
        self.routes: list[APIRoute] = []

    def get(self, route: str):
        def wrapper(func: Callable[F_Spec, F_Return]) -> Callable[F_Spec, F_Return]:
            self.routes.append(APIRoute(route, func))
            return func

        return wrapper
