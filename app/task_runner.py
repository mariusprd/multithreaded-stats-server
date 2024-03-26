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

        self.num_of_threads = int(os.environ['TP_NUM_OF_THREADS']) if 'TP_NUM_OF_THREADS' in os.environ else os.cpu_count()
        print(f"Server using {self.num_of_threads} threads")

        # var to notify that the data was loaded
        self.data_loaded = Event()

        self.task_state = {}
        self.task_queue = Queue()

        self.threads = [TaskRunner(i, self.task_queue, self.task_state, self.data_loaded) for i in range(self.num_of_threads)]
        for i in range(self.num_of_threads):
            self.threads[i].start()

    def add_task(self, task, job_id) -> int:
        '''adds task to queue and task_state'''
        self.task_queue.put((task, job_id))
        self.task_state[f"job_id_{job_id}"] = "running"

        return job_id

    def get_num_jobs(self) -> int:
        '''Returns the number of jobs in the queue'''
        return self.task_queue.qsize()

    def get_jobs(self) -> list:
        '''Returns job states'''
        return list(self.task_state.items())

    def graceful_shutdown(self) -> None:
        '''ThreadPool shutdown'''
        for thread in self.threads:
            self.task_queue.put((None, None))

        for thread in self.threads:
            thread.join()

        print("THREADPOOL SHUTDOWN!!!")

    def is_valid(self, job_id) -> bool:
        '''Checks if job_id is valid'''
        return f"job_id_{job_id}" in self.task_state


class TaskRunner(Thread):
    def __init__(self, thread_id: int, task_queue: Queue, task_state: dict, data_loaded: Event):
        super().__init__()
        self.thread_id = thread_id
        self.task_queue = task_queue
        self.task_state = task_state
        self.data_loaded = data_loaded

    def run(self):
        # wait for data to process
        self.data_loaded.wait()
        print(f"Started TaskRunner num {self.thread_id}")

        while True:
            # TODO
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            job_id, job = self.task_queue.get()
            if job is None: break

            # Execute the job

            # Save the result to disk

            # Update the task state
            self.task_state[f"job_id_{job_id}"] = "done"




