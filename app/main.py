from fastapi import FastAPI, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker
from sqlalchemy.pool import StaticPool

from app.adapters.orm import mapper_registry, start_mappers
from app.repositories.todo import ItemNotFound, TodoRepositorySqlAlchemy
from app.schemas.todo import TodoSchema
from app.services.todo import TodoService


def create_app():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    mapper_registry.metadata.create_all(engine)
    start_mappers()
    session = sessionmaker(engine)
    app = FastAPI()
    return app, session


app, session = create_app()


@app.on_event("shutdown")
def shutdown():
    clear_mappers()


@app.exception_handler(ItemNotFound)
def todo_not_found(request, exc):
    return Response(status_code=404)


@app.get("/todos")
def todos():
    repo = TodoRepositorySqlAlchemy(session)
    todos = TodoService.all(repo)
    return [TodoSchema.from_model(todo) for todo in todos]


@app.post("/todos")
def create_todo(todo_schema: TodoSchema):
    repo = TodoRepositorySqlAlchemy(session)
    todo = todo_schema.to_model()
    created = TodoService.create(todo, repo)
    return TodoSchema.from_model(created)


@app.get("/todos/{todo_uuid}")
def read_todo(todo_uuid):
    repo = TodoRepositorySqlAlchemy(session)
    todo = repo.read(todo_uuid)
    return TodoSchema.from_model(todo)


@app.put("/todos/{todo_uuid}")
def update_todo(todo_schema: TodoSchema, todo_uuid: str):
    repo = TodoRepositorySqlAlchemy(session)
    todo = todo_schema.to_model()
    todo.uuid = todo_uuid
    updated = TodoService.update(todo, repo)
    return TodoSchema.from_model(updated)


@app.delete("/todos/{todo_uuid}")
def delete_todo(todo_uuid: str):
    repo = TodoRepositorySqlAlchemy(session)
    repo.read(todo_uuid)
    TodoService.delete(todo_uuid, repo)
    return {}
