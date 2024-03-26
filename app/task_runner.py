import os
from queue import Queue
from threading import Thread, Lock, Event
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

        self.num_of_threads = int(os.environ['TP_NUM_OF_THREADS']) if 'TP_NUM_OF_THREADS' in os.environ else os.cpu_count()
        print(f"Server using {self.num_of_threads} threads")

        # var to notify that the data was loaded
        self.data_loaded = Event()

        self.task_state = {}
        self.task_queue = Queue()

        self.current_job_id = 0

        self.threads = []
        for i in range(self.num_of_threads):
            self.threads.append(TaskRunner(i, self.task_queue, self.task_state, self.data_loaded))
            self.threads[i].start()


    def add_task(self, task):
        self.task_queue.put(task)
        self.current_job_id += 1
        job_id = f"job_id_{self.current_job_id}"
        self.task_state[job_id] = "running"

        return self.current_job_id


    def get_num_jobs(self):
        return self.task_queue.qsize()
    

    def get_jobs(self):
        return list(self.task_state.items())


    def graceful_shutdown(self):
        for thread in self.threads:
            self.task_queue.put(None)

        for thread in self.threads:
            thread.join()

class TaskRunner(Thread):
    def __init__(self, thread_id: int, task_queue: Queue, task_state: dict, data_loaded: Event):
        # TODO: init necessary data structures
        super().__init__()
        self.therad_id = thread_id
        self.task_queue = task_queue
        self.task_state = task_state
        self.data_loaded = data_loaded

    def run(self):
        # wait for data to process
        self.data_loaded.wait()
        print(f"Started TaskRunner num {self.therad_id}")

        while True:
            # TODO
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            task = self.task_queue.get()
            if task is None: break

