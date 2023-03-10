import uuid
from abc import ABCMeta, abstractmethod
from typing import Dict, Self

from sqlalchemy import delete, select, update

from app.domain.todo import Todo


class ItemNotFound(Exception):
    pass


class TodoRepository(metaclass=ABCMeta):
    @abstractmethod
    def create(self: Self, todo: Todo) -> Todo:
        raise NotImplementedError()

    @abstractmethod
    def read(self: Self, uuid: str) -> Todo:
        raise NotImplementedError()

    @abstractmethod
    def update(self: Self, todo: Todo) -> Todo:
        raise NotImplementedError()

    @abstractmethod
    def delete(self: Self, uuid: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def all(self: Self) -> list[Todo]:
        raise NotImplementedError()


class TodoRepositoryInMemory(TodoRepository):
    def __init__(self) -> None:
        self.items: Dict[str, Todo] = {}

    def create(self: Self, todo: Todo) -> Todo:
        todo.uuid = str(uuid.uuid4())
        self.items[todo.uuid] = todo
        return todo

    def read(self: Self, uuid: str) -> Todo:
        try:
            return self.items[uuid]
        except KeyError:
            raise ItemNotFound(uuid)

    def update(self: Self, todo: Todo) -> Todo:
        self.read(todo.uuid)
        self.items[todo.uuid] = todo
        return todo

    def delete(self: Self, uuid: str) -> None:
        del self.items[uuid]

    def all(self: Self) -> list[Todo]:
        return list(self.items.values())


class TodoRepositorySqlAlchemy(TodoRepository):
    def __init__(self, session):
        self.session = session

    def create(self: Self, todo: Todo) -> Todo:
        with self.session() as session:
            with session.begin():
                todo.uuid = str(uuid.uuid4())
                session.add(todo)
            session.refresh(todo)
            return todo

    def read(self: Self, uuid: str) -> Todo:
        stmt = select(Todo).where(Todo.uuid == uuid)
        result = self.session().scalars(stmt).first()
        if not result:
            raise ItemNotFound()
        return result

    def update(self: Self, todo: Todo) -> Todo:
        self.read(todo.uuid)
        with self.session() as session:
            with session.begin():
                stmt = (
                    update(Todo)
                    .where(
                        Todo.uuid == todo.uuid,
                    )
                    .values(title=todo.title, is_done=todo.is_done)
                )
                session.execute(stmt)
                return todo

    def delete(self: Self, uuid: str) -> None:
        with self.session() as session:
            with session.begin():
                stmt = delete(Todo).where(Todo.uuid == uuid)
                session.execute(stmt)

    def all(self: Self) -> list[Todo]:
        with self.session() as session:
            stmt = select(Todo)
            return session.scalars(stmt).all()
