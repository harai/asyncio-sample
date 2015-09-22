import asyncio
import time
from asyncio import Queue, Semaphore
from pprint import PrettyPrinter

import aiobotocore

pp = PrettyPrinter(indent=3)

# import logging
# logging.basicConfig(level=logging.DEBUG)


@asyncio.coroutine
def go(loop, task_id):

  print('Start task {}'.format(task_id))
  bucket = 'jharai'
  filename = '{}-{}'.format(time.strftime("%H-%M-%S"), task_id)
  folder = 'aiobotocore'
  key = '{}/{}'.format(folder, filename)

  session = aiobotocore.get_session(loop=loop)
  client = session.create_client(
      's3',
      region_name='ap-northeast-1')

  try:
    # upload object to amazon s3
    data = b'\x01' * 1024
    resp = yield from client.put_object(Bucket=bucket, Key=key, Body=data)
    print('Finish task {}'.format(task_id))
    print(resp)
  finally:
    client.close()


@asyncio.coroutine
def go_producer(loop, q, tasks):
  for t in tasks:
    yield from q.put(t)


@asyncio.coroutine
def go_consumer(loop, q, count):
  for _ in range(0, count):
    task = yield from q.get()
    yield from task


@asyncio.coroutine
def go_queue(loop, tasks, concurrent_num):
  q = Queue(concurrent_num)
  count = len(tasks)
  yield from asyncio.gather(
      go_producer(loop, q, tasks),
      go_consumer(loop, q, count))


@asyncio.coroutine
def go_semaphore_task(loop, sem, task):
  with (yield from sem):
    yield from task


def semaphore(loop, tasks, concurrent_num):
  sem = Semaphore(concurrent_num)
  sem_tasks = [go_semaphore_task(loop, sem, t) for t in tasks]
  return asyncio.gather(*sem_tasks)


def create_tasks(loop, num):
  return [go(loop, i) for i in range(0, num)]


def go_parallel(tasks):
  return asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
# loop.run_until_complete(go(loop))
# loop.run_until_complete(go_parallel(create_tasks(loop, 10)))
loop.run_until_complete(go_queue(loop, create_tasks(loop, 50), 50))
# loop.run_until_complete(semaphore(loop, create_tasks(loop, 100), 2))
