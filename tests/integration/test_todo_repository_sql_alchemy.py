import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import clear_mappers, sessionmaker

from app.adapters.orm import mapper_registry, start_mappers
from app.domain.todo import Todo
from app.repositories.todo import ItemNotFound, TodoRepositorySqlAlchemy


@pytest.fixture
def session():
    clear_mappers()
    engine = create_engine("sqlite:///:memory:")
    mapper_registry.metadata.create_all(engine)
    start_mappers()
    yield sessionmaker(engine)
    clear_mappers()


@pytest.fixture
def todo(faker, session):
    return Todo(
        title=faker.pystr(),
        is_done=faker.pybool(),
    )


def test_create(todo, session):
    repo = TodoRepositorySqlAlchemy(session)

    repo.create(todo)

    with session() as s:
        result = s.scalars(select(Todo)).all()
    created = result[0]
    assert len(result) == 1
    assert created.title == todo.title
    assert created.uuid
    assert created.is_done == todo.is_done


def test_read(todo, session):
    repo = TodoRepositorySqlAlchemy(session)
    created = repo.create(todo)
    readed = repo.read(created.uuid)
    assert readed.title == created.title
    assert readed.is_done == created.is_done
    assert readed.uuid == created.uuid


def test_read_not_found(session):
    repo = TodoRepositorySqlAlchemy(session)

    with pytest.raises(ItemNotFound):
        repo.read("1")


def test_update(todo, session):
    repo = TodoRepositorySqlAlchemy(session)
    todo = repo.create(todo)
    todo.title = "newtitle"
    todo.done()

    repo.update(todo)

    with session() as s:
        updated = s.scalars(select(Todo).where(Todo.uuid == todo.uuid)).first()
    assert updated.title == "newtitle"
    assert updated.is_done is True


def test_update_not_found(session, todo, faker):
    repo = TodoRepositorySqlAlchemy(session)
    todo.uuid = faker.uuid4()

    with pytest.raises(ItemNotFound):
        repo.update(todo)


def test_delete(session, todo):
    repo = TodoRepositorySqlAlchemy(session)
    created = repo.create(todo)

    repo.delete(created.uuid)

    with session() as s:
        result = s.scalars(select(Todo)).all()
    assert len(result) == 0


def test_all(session, faker):
    repo = TodoRepositorySqlAlchemy(session)
    todo1 = Todo(title=faker.pystr(), is_done=faker.pybool())
    todo2 = Todo(title=faker.pystr(), is_done=faker.pybool())

    repo.create(todo1)
    repo.create(todo2)

    assert len(repo.all()) == 2
