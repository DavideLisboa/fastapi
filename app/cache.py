import redis
import pickle
from .schemas import Task

r = redis.Redis(host='localhost', port=6379, db=0)


def get_task(task_id: int):
    task = r.get(f"task:{task_id}")
    if task:
        return pickle.loads(task)
    return None


def set_task(task_id: int, task: Task):
    r.set(f"task:{task_id}", pickle.dumps(task))


def get_tasks(skip: int, limit: int):
    tasks = r.get(f"tasks:{skip}:{limit}")
    if tasks:
        return pickle.loads(tasks)
    return None


def set_tasks(skip: int, limit: int, tasks: list[Task]):
    r.set(f"tasks:{skip}:{limit}", pickle.dumps(tasks))


def delete_task(task_id: int):
    r.delete(f"task:{task_id}")
