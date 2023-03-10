from fastapi import FastAPI, Response

from app.repositories.todo import ItemNotFound, TodoRepositoryInMemory
from app.schemas.todo import TodoSchema
from app.services.todo import TodoService

app = FastAPI()
repo = TodoRepositoryInMemory()


@app.exception_handler(ItemNotFound)
def todo_not_found(request, exc):
    return Response(status_code=404)


@app.get("/todos")
def todos():
    todos = TodoService.all(repo)
    return [TodoSchema.from_model(todo) for todo in todos]


@app.post("/todos")
def create_todo(todo_schema: TodoSchema):
    todo = todo_schema.to_model()
    created = TodoService.create(todo, repo)
    return TodoSchema.from_model(created)


@app.get("/todos/{todo_uuid}")
def read_todo(todo_uuid):
    todo = repo.read(todo_uuid)
    return TodoSchema.from_model(todo)


@app.put("/todos/{todo_uuid}")
def update_todo(todo_schema: TodoSchema, todo_uuid: str):
    todo = todo_schema.to_model()
    todo.uuid = todo_uuid
    updated = TodoService.update(todo, repo)
    return TodoSchema.from_model(updated)


@app.delete("/todos/{todo_uuid}")
def delete_todo(todo_uuid: str):
    TodoService.delete(todo_uuid, repo)
    return {}
