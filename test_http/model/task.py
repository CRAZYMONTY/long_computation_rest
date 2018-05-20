import uuid

import test_http.worker.worker as worker


class JobDefinition:
    IMAGE_RESIZE = 'IMAGE_RESIZE'


class Task(object):
    def __init__(self,
                 id,
                 status='CREATED',
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
        self.status = 'RUNNING'
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
