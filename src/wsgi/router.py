from collections.abc import Callable
from typing import ParamSpec, get_origin, get_type_hints

from wsgi.response import Response

F_Spec = ParamSpec("F_Spec")


class APIRoute:
    def __init__(self, path: str, method: str, func: Callable[F_Spec, Response]):
        self.path: str = path
        self.method: str = method
        self.func: Callable[..., Response] = func


class Router:
    def __init__(self):
        self.routes: list[APIRoute] = []

    def add_route(self, func: Callable[F_Spec, Response], method: str, route: str):
        self.routes.append(APIRoute(route, method, func))

    def get(self, route: str):
        def wrapper(func: Callable[F_Spec, Response]) -> Callable[F_Spec, Response]:
            self.add_route(func, "GET", route)
            return func

        return wrapper

    def post(self, route: str):
        def wrapper(func: Callable[F_Spec, Response]) -> Callable[F_Spec, Response]:
            self.add_route(func, "POST", route)
            return func

        return wrapper

    def patch(self, route: str):
        def wrapper(func: Callable[F_Spec, Response]) -> Callable[F_Spec, Response]:
            self.add_route(func, "PATCH", route)
            return func

        return wrapper

    def parse_kwargs(self, func: Callable[F_Spec, object], **kwargs: list) -> dict:
        hints = get_type_hints(func)
        for key, value in kwargs.items():
            key_type = hints.get(key, None)
            if not get_origin(key_type) is list and len(value) == 1:
                kwargs[key] = kwargs[key][0]
        return kwargs

    def handle(self, path: str, method: str, *args, **kwargs) -> Response:
        for route in self.routes:
            if route.path == path and route.method == method:
                params = self.parse_kwargs(route.func, **kwargs)
                return route.func(*args, **params)
        return Response("Not Founded", "404 Not Founded", "text/plain; charset=utf-8")
