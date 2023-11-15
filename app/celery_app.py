import os
import time

from celery import Celery

redis_url = os.environ.get("redis_url")
CELERY_BROKER_URL = f"redis://{redis_url}:6379"
CELERY_RESULT_BACKEND = f"redis://{redis_url}:6379"

# Initialize Celery
celery = Celery("worker", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name="tasks.add")
def add(x: int, y: int) -> int:
    time.sleep(5)
    result = x + y
    print("add", x, y, result)
    return result
