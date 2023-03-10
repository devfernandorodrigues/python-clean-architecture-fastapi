from app.domain.todo import Todo


def test_done(faker):
    todo = Todo(
        title=faker.pystr(),
        is_done=False,
    )
    todo.done()
    assert todo.is_done is True


def test_not_done(faker):
    todo = Todo(
        title=faker.pystr(),
        is_done=True,
    )
    todo.not_done()
    assert todo.is_done is False
