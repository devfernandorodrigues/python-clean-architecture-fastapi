import uuid
from typing import Dict, Self

from app.domain.todo import Todo
from app.repositories.base import ItemNotFound, Repository


class TodoInMemoryRepository(Repository):
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
        return list(self.items.items())
