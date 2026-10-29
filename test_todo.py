from todo import TodoList

def test_add_task():
    todo = TodoList()
    res = todo.add_task("Buy milk")
    assert "Buy milk" in res
    assert len(todo.tasks) == 1
    print("✅ test_add_task passed")

def test_mark_done():
    todo = TodoList()
    todo.add_task("Buy milk")
    res = todo.mark_done(0)
    assert todo.tasks[0]["done"] == True
    print("✅ test_mark_done passed")

def test_get_all_tasks():
    todo = TodoList()
    todo.add_task("Buy milk")
    todo.add_task("Write code")
    tasks = todo.get_all_tasks()
    assert len(tasks) == 2
    print("✅ test_get_all_tasks passed")

if __name__ == "__main__":
    test_add_task()
    test_mark_done()
    test_get_all_tasks()
    print("\n🎉 All tests passed!")
