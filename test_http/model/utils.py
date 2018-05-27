from contextlib import contextmanager

import pickle


@contextmanager
def persist(self, filename="db.json"):
    with open(filename, "rb+") as f:
        self.data = pickle.load(f)
        yield
        f.seek(0)
        pickle.dump(self.data, file=f)


class TaskStatus(object):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    DELETED = "DELETED"
    DONE = "DONE"
    statuses = [CREATED, RUNNING, FAILED, DELETED, DONE]


class TaskDao:

    def __init__(self):
        self.data = {}

    def get_task(self, id):
        with persist(self):
            return self.data.get(id)

    def add_task(self, task):
        with persist(self):
            self.data[task.id] = task

    def delete_task(self, id):
        with persist(self):
            if id not in self.data.keys():
                return None
            self.data.pop(id)
            return id

    def update_task(self, task):
        with persist(self):
            self.data[task.id] = task


task_dao = TaskDao()
