import pytest
from test_http.model.task import Task
from test_http.model.utils import TaskStatus


class TestTask(object):
    def test_update_status_correct(self):
        task = Task(1)

        task.status = TaskStatus.RUNNING

        assert task.status == TaskStatus.RUNNING

    def test_update_status_incorrect(self):
        task = Task(1)

        with pytest.raises(AssertionError) as _:
            task.status = "FOOOO"

        assert task.status == TaskStatus.CREATED
