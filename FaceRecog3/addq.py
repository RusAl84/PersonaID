from redis import Redis
from rq import Queue, Worker

# Returns all workers registered in this connection
redis = Redis(host='localhost', port=6379)
workers = Worker.all(connection=redis)

# Returns all workers in this queue (new in version 0.10.0)
queue = Queue('queue_name')
workers = Worker.all(queue=queue)
worker = workers[0]
print(worker.nam