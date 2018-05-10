import uuid
import pickle
from test_http.worker import worker
from contextlib import contextmanager


@contextmanager
def persist(self, filename='db.json'):
    with open(filename, 'rb+') as f:
        self.data = pickle.load(f)
        yield
        f.seek(0)
        pickle.dump(self.data, file=f)


class TaskStatus:
    CREATED = 'CREATED'
    RUNNING = 'RUNNING'
    FAILED = 'FAILED'
    DELETED = 'DELETED'
    DONE = 'DONE'


class JobDefinition:
    IMAGE_RESIZE = 'IMAGE_RESIZE'


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


class Task(object):
    def __init__(self,
                 id,
                 status=TaskStatus.CREATED,
                 job_definition=JobDefinition.IMAGE_RESIZE,
                 job_result=None,
                 error=None):
        self.error = error
        self.job_result = job_result
        self.job_definition = job_definition
        self.status = status
        self.id = id

    @staticmethod
    def create_task():
        return Task(id=uuid.uuid4())

    def run_task(self):
        self.status = TaskStatus.RUNNING
        return worker.image_resize.delay(self.id)

    def update_status(self, status):
        self.status = status

    @property
    def task_status(self):
        return self.status

    def __iter__(self):
        yield 'Id', str(self.id)
        yield 'Status', self.status
        yield 'Error', self.error
        yield 'JobResult', self.job_result
        yield 'JobDefinition', self.job_definition

    def __str__(self):
        return str(dict(self))