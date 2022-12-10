from __future__ import annotations

from typing import Callable, Generic, Protocol, TypeVar

T = TypeVar("T")


class Observable(Protocol):
    __observers__: list[Observer]


class Observer(Generic[T]):
    def __init__(
        self,
        observable: Observable,
        filter: Callable[[T], bool] | None = None,
    ) -> None:
        self.observable = observable
        self.filter = filter

    def callback(self, item: T) -> None:
        ...

    def receive(self, item: T) -> None:
        if self.filter:
            if self.filter(item):
                self.callback(item)
        else:
            self.callback(item)

    def remove(self) -> None:
        try:
            self.observable.__observers__.remove(self)
        except ValueError:
            pass
