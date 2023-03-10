from dataclasses import asdict

from pydantic import BaseModel

from app.domain.todo import Todo


class TodoSchema(BaseModel):
    uuid: str | None = None
    title: str
    is_done: bool

    def to_model(self) -> Todo:
        return Todo(
            uuid=self.uuid,
            title=self.title,
            is_done=self.is_done,
        )

    @staticmethod
    def from_model(todo: Todo):
        return TodoSchema(**asdict(todo))
