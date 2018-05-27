import uuid
import test_http.worker.worker as worker
import test_http.model.utils as utils


class JobDefinition:
    IMAGE_RESIZE = "IMAGE_RESIZE"


class Task(object):

    def __init__(
        self,
        id,
        status="CREATED",
        job_definition=JobDefinition.IMAGE_RESIZE,
        job_result=None,
        error=None,
    ):
        self.error = error
        self.job_result = job_result
        self.job_definition = job_definition
        self.task_status = status
        self.id = id

    @staticmethod
    def create_task():
        return Task(id=uuid.uuid4())

    def run_task(self):
        self.task_status = utils.TaskStatus.RUNNING
        return worker.image_resize.delay(self.id)

    @property
    def status(self):
        return self.task_status

    @status.setter
    def status(self, value):
        assert value in utils.TaskStatus.statuses
        self.task_status = value
        return self.task_status

    def __iter__(self):
        yield "Id", str(self.id)
        yield "Status", self.task_status
        yield "Error", self.error
        yield "JobResult", self.job_result
        yield "JobDefinition", self.job_definition

    def __str__(self):
        return str(dict(self))
