import os
from queue import Queue
import threading
import time
from . import webserver

class ThreadPool:
    def __init__(self):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task

        if 'TP_NUM_OF_THREADS' in os.environ:
            self.num_of_threads = int(os.environ['TP_NUM_OF_THREADS'])
        else:
            self.num_of_threads = os.cpu_count()

        print(f"Server using {self.num_of_threads} threads")

        self.task_state = {}
        self.task_queue = Queue()
        self.job_id_lock = threading.Lock()

        self.threads = []
        for i in range(self.num_of_threads):
            self.threads.append(TaskRunner())
            self.threads[i].start()

    def add_task(self, task):
        self.task_queue.put(task)
        with self.job_id_lock:
            webserver.job_counter += 1
            job_id = webserver.job_counter
            self.task_state[job_id] = "running"
        return job_id - 1

class TaskRunner(threading.Thread):
    def __init__(self):
        # TODO: init necessary data structures
        pass

    def run(self):
        while True:
            # TODO
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            pass
