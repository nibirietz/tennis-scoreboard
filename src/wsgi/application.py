import functools
from collections.abc import Iterable


class Application:
    def __call__(self, environ: dict, start_response: Callable) -> Iterable[byte]:
        yield b"Stub."


if __name__ == "__main__":
    app = Application()


# TODO:Все функции при создании с декоратором добавляют роуты в список. В __call__ мы вызываем роутер, который получает путь и вызывает нужную функцию.
