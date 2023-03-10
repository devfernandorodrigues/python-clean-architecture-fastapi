from dataclasses import dataclass


@dataclass
class Todo:
    title: str
    is_done: bool
    uuid: str | None = None

    def done(self):
        self.is_done = True

    def not_done(self):
        self.is_done = False
