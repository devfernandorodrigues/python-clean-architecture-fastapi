import pytest
from fastapi.testclient import TestClient

from app.domain.todo import Todo
from app.main import app, repo

client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def delete_all_from_repo():
    repo.items = {}


def test_all(faker):
    todo = repo.create(Todo(title=faker.pystr(), is_done=faker.pybool()))

    resp = client.get("/todos")

    assert resp.json() == [
        {"uuid": todo.uuid, "title": todo.title, "is_done": todo.is_done}
    ]


def test_create(faker):
    data = {"title": faker.pystr(), "is_done": faker.pybool()}

    resp = client.post("/todos", json=data)

    resp_json = resp.json()
    assert resp.status_code == 200
    assert resp_json["title"] == data["title"]
    assert resp_json["is_done"] == data["is_done"]
    assert resp_json["uuid"]
    assert len(repo.all()) == 1


def test_update(faker):
    todo = repo.create(Todo(title=faker.pystr(), is_done=faker.pybool()))
    data = {"title": faker.pystr(), "is_done": faker.pybool()}

    resp = client.put(f"/todos/{todo.uuid}", json=data)

    resp_json = resp.json()
    assert resp.status_code == 200
    assert resp_json["uuid"] == todo.uuid
    assert resp_json["title"] == data["title"]
    assert resp_json["is_done"] == data["is_done"]
    assert len(repo.all()) == 1


def test_read(faker):
    todo = repo.create(Todo(title=faker.pystr(), is_done=faker.pybool()))

    resp = client.get(f"/todos/{todo.uuid}")

    resp_json = resp.json()
    assert resp.status_code == 200
    assert resp_json["title"] == todo.title
    assert resp_json["is_done"] == todo.is_done
    assert resp_json["uuid"] == todo.uuid


def test_read_not_found():
    resp = client.get("/todos/notfound")
    assert resp.status_code == 404


def test_update_not_found(faker):
    data = {"title": faker.pystr(), "is_done": faker.pybool()}
    resp = client.put("/todos/notfound", json=data)
    assert resp.status_code == 404


def test_delete(faker):
    todo = repo.create(
        Todo(
            title=faker.pystr(),
            is_done=faker.pybool(),
        )
    )

    resp = client.delete(f"/todos/{todo.uuid}")

    assert resp.status_code == 200
    assert len(repo.all()) == 0
