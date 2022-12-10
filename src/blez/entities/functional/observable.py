from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Generic, TypeVar

if TYPE_CHECKING:
    from .observer import Observer

T = TypeVar("T")

ObserverType = TypeVar("ObserverType", bound="Observer[Any]")


class Observable(Generic[T]):

    __observers__: list[Observer]

    def receive(self, item: T) -> None:
        for observer in self.__observers__:
            try:
                observer.receive(item)
            except Exception:
                pass

    def create_observer(
        self,
        observerT: type[ObserverType[T]],
        filter: Callable[[T], bool] | None = None,
    ) -> ObserverType[T]:
        observer = observerT(self, filter=filter)
        if observer not in self.__observers__:
            self.__observers__.append(observer)
        return observer

    def remove_observer(self, observer: Observer[Any]) -> None:
        try:
            self.__observers__.remove(observer)
        except ValueError:
            pass
