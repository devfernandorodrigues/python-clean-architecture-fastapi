import uuid
from abc import ABCMeta, abstractmethod
from typing import Dict, Self, TypeVar

from app.domain.todo import Todo

T = TypeVar("T")


class ItemNotFound(Exception):
    pass


class TodoRepository(metaclass=ABCMeta):
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


class TodoRepositoryInMemory(TodoRepository):
    def __init__(self) -> None:
        self.items: Dict[str, Todo] = {}
        super().__init__()

    def create(self: Self, obj: Todo) -> Todo:
        obj.uuid = str(uuid.uuid4())
        self.items[obj.uuid] = obj
        return obj

    def read(self: Self, uuid: str) -> Todo:
        try:
            return self.items[uuid]
        except KeyError:
            raise ItemNotFound(uuid)

    def update(self: Self, obj: Todo) -> Todo:
        self.read(obj.uuid)
        self.items[obj.uuid] = obj
        return obj

    def delete(self: Self, uuid: str) -> None:
        del self.items[uuid]

    def all(self: Self) -> list[Todo]:
        return list(self.items.values())
