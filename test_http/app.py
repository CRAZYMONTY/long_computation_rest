import uuid

from flask import Flask, logging, request
from test_http.worker import worker
from test_http.model.task import Task, task_dao

app = Flask(__name__)
log = logging.create_logger(app)
log.setLevel('INFO')


@app.route('/task', methods=['POST'])
def create_task():
    task = Task.create_task()
    task_dao.add_task(task)
    log.info(f'Created task: {task}')
    return str(task.id), 201


@app.route('/task/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def task(task_id):
    try:
        id = uuid.UUID(task_id)
    except ValueError as e:
        log.error(e)
        return 'WrongTaskIdFormat', 400
    task: Task = task_dao.get_task(id)
    if task is None:
        return 'TaskDoesNotExist', 404
    if request.method == 'GET':
        return str(task)
    if request.method == 'PUT':
        task.run_task()
        task_dao.update_task(task)
        return '', 202
    if request.method == 'DELETE':
        latest_status = task.status
        task_dao.delete_task(task.id)
        return latest_status, 200
