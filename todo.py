# 简单的待办列表业务代码
class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task_name):
        self.tasks.append({"name": task_name, "done": False})
        return f"Added task: {task_name}"

    def get_all_tasks(self):
        return [f"[{'x' if t['done'] else ' '}] {t['name']}" for t in self.tasks]

    def mark_done(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index]["done"] = True
            return f"Marked task {task_index} as done"
        return "Invalid task index"
