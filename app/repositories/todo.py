import uuid
from abc import ABCMeta, abstractmethod
from typing import Dict, Self, TypeVar

from sqlalchemy import delete, select, update

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


class TodoRepositorySqlAlchemy(TodoRepository):
    def __init__(self, session):
        self.session = session

    def create(self: Self, obj: Todo) -> Todo:
        with self.session() as session:
            obj.uuid = str(uuid.uuid4())
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def read(self: Self, uuid: str) -> Todo:
        stmt = select(Todo).where(Todo.uuid == uuid)
        result = self.session().scalars(stmt).first()
        if not result:
            raise ItemNotFound()
        return result

    def update(self: Self, obj: Todo) -> Todo:
        self.read(obj.uuid)
        with self.session() as session:
            with session.begin():
                stmt = (
                    update(Todo)
                    .where(
                        Todo.uuid == obj.uuid,
                    )
                    .values(title=obj.title, is_done=obj.is_done)
                )
                session.execute(stmt)
                return obj

    def delete(self: Self, uuid: str) -> None:
        with self.session() as session:
            with session.begin():
                stmt = delete(Todo).where(Todo.uuid == uuid)
                session.execute(stmt)
                session.commit()

    def all(self: Self) -> list[Todo]:
        with self.session() as session:
            stmt = select(Todo)
            return session.scalars(stmt).all()
