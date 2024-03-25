import os
from queue import Queue
from threading import Thread, Event
import time

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

        pass

class TaskRunner(Thread):
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
