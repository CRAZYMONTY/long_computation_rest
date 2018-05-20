from test_http.model.task import Task
from test_http.model.utils import TaskStatus


def test_update_status():
    task = Task(1)

    task.update_status(TaskStatus.RUNNING)

    assert task.status == TaskStatus.RUNNING
