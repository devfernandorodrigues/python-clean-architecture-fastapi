from abc import ABCMeta, abstractmethod
from typing import Self, TypeVar

T = TypeVar("T")


class ItemNotFound(Exception):
    pass


class Repository(metaclass=ABCMeta):
    @abstractmethod
    def create(self: Self, obj: T) -> T:
        raise NotImplementedError()

    @abstractmethod
    def read(self: Self, uuid: str) -> T:
        raise NotImplementedError()

    @abstractmethod
    def update(self: Self, obj: T) -> T:
        raise NotImplementedError()

    @abstractmethod
    def delete(self: Self, uuid: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def all(self: Self) -> list[T]:
        raise NotImplementedError()
