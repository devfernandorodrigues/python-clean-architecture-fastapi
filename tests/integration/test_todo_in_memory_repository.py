import pytest

from app.domain.todo import Todo
from app.repositories.base import ItemNotFound
from app.repositories.in_memory import TodoInMemoryRepository


@pytest.fixture
def repo():
    return TodoInMemoryRepository()


def test_create(faker, repo):
    todo = Todo(
        title=faker.pystr(),
        is_done=False,
    )
    created = repo.create(todo)
    assert len(repo.items) == 1
    assert created.uuid
    assert created.title == todo.title
    assert created.is_done == todo.is_done


def test_read(faker, repo):
    todo = Todo(
        title=faker.pystr(),
        is_done=False,
    )
    created = repo.create(todo)

    todo_repo = repo.read(created.uuid)

    assert todo == todo_repo


def test_read_not_found(repo):
    with pytest.raises(ItemNotFound):
        repo.read("notexists")


def test_update(faker, repo):
    todo = Todo(title=faker.pystr(), is_done=False)
    created = repo.create(todo)
    created.title = "mynewtitle"

    updated = repo.update(created)

    assert updated.title == "mynewtitle"


def test_update_not_found(faker, repo):
    todo = Todo(title=faker.pystr(), is_done=False, uuid=faker.uuid4())

    with pytest.raises(ItemNotFound):
        repo.update(todo)


def test_delete(faker, repo):
    todo = Todo(title=faker.pystr(), is_done=False)
    created = repo.create(todo)

    assert len(repo.items) == 1

    repo.delete(created.uuid)
    assert len(repo.items) == 0


def test_delete_correct(faker, repo):
    todo = Todo(title=faker.pystr(), is_done=False)
    other_todo = Todo(title=faker.pystr(), is_done=False)
    created = repo.create(todo)
    other_todo = repo.create(other_todo)

    assert len(repo.items) == 2

    repo.delete(created.uuid)
    assert len(repo.items) == 1
    assert repo.read(other_todo.uuid) == other_todo


def test_all(faker, repo):
    todo = Todo(title=faker.pystr(), is_done=False)
    other_todo = Todo(title=faker.pystr(), is_done=False)
    repo.create(todo)
    repo.create(other_todo)

    all_todos = repo.all()

    assert len(all_todos) == 2
