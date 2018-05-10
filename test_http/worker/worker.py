import uuid

from celery import Celery
from time import sleep
from test_http.model.task import task_dao, TaskStatus

CELERY_ACCEPT_CONTENT = ['pickle']

app = Celery('tasks',
             broker='amqp://admin:mypass@localhost:5673')


@app.task()
def image_resize(task_id):
    task = task_dao.get_task(uuid.UUID(task_id))
    print(f'Long running operation on task {task.job_definition}')
    sleep(5)
    task.job_result = 'Task successfully finished.'
    print(f'Long running operation finished.')
    print(f'Updating task with id {task.id}...')
    task.update_status(TaskStatus.DONE)
    task_dao.update_task(task)
    print(f'Task updated.')
    return task
