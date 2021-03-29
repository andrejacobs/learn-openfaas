import os
from redis import Redis
import rq
from .utils import load_secret


def task_queue():
    queueName = os.environ.get('queue-name', 'johnny5')
    redisURL = os.environ.get('redis-url', 'redis://10.62.0.1:6379/0')
    queue = rq.Queue(queueName, connection=Redis.from_url(redisURL))
    return queue


def enqueue_task(queue, task, *args):
    job = queue.enqueue(task, *args)


def download_legoset_image(pkID, imageURL):
    print(f'Received task to download image for: pkID: {pkID} | imageURL: {imageURL}')
    print('TODO: implement this :p')
