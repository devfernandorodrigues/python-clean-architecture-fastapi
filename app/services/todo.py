from app.domain.todo import Todo
from app.repositories.todo import TodoRepository


class TodoService:
    @staticmethod
    def create(todo: Todo, repo: TodoRepository) -> Todo:
        return repo.create(todo)

    @staticmethod
    def update(todo: Todo, repo: TodoRepository) -> Todo:
        return repo.update(todo)

    @staticmethod
    def read(uuid: str, repo: TodoRepository) -> Todo:
        return repo.read(uuid)

    @staticmethod
    def delete(uuid: str, repo: TodoRepository) -> Todo:
        return repo.delete(uuid)

    @staticmethod
    def all(repo: TodoRepository) -> list[Todo]:
        return repo.all()
