from sqlalchemy import Boolean, Column, String, Table
from sqlalchemy.orm import registry

from app.domain.todo import Todo

mapper_registry = registry()

todos = Table(
    "todo",
    mapper_registry.metadata,
    Column("uuid", String(255), primary_key=True, unique=True),
    Column("title", String(255)),
    Column("is_done", Boolean, nullable=False),
)


def start_mappers():
    mapper_registry.map_imperatively(Todo, todos)
