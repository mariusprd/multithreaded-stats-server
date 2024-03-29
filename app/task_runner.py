import os
from queue import Queue
from threading import Thread, Event
import time

class ThreadPool:
    def __init__(self):
        # set number of threads
        self.num_of_threads = (
            int(os.environ['TP_NUM_OF_THREADS']) if 'TP_NUM_OF_THREADS' in os.environ
            else os.cpu_count()
        )

        # var to notify that the data was loaded
        self.data_loaded = Event()

        # task management
        self.task_state = {}
        self.task_queue = Queue()

        self.threads = [
            TaskRunner(i, self.task_queue, self.task_state, self.data_loaded)
            for i in range(self.num_of_threads)
        ]
        for i in range(self.num_of_threads):
            self.threads[i].start()

        # create the result directory if it doesn't exist
        if not os.path.exists("./results"):
            os.makedirs("./results")

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

        # remove the results directory
        os.rmdir("./results")

        print("THREADPOOL SHUTDOWN!!!")

    def is_valid(self, job_id) -> bool:
        '''Checks if job_id is valid'''
        return f"job_id_{job_id}" in self.task_state

    def is_done(self, job_id) -> bool:
        '''Checks if job is done'''
        return self.task_state[f"job_id_{job_id}"] == "done"


class TaskRunner(Thread):
    def __init__(
        self,
        thread_id: int,
        task_queue: Queue,
        task_state: dict,
        data_loaded: Event,
    ):
        Thread.__init__(self)
        self.thread_id = thread_id
        self.task_queue = task_queue
        self.task_state = task_state
        self.data_loaded = data_loaded

    def run(self):
        # wait for data to process
        self.data_loaded.wait()

        while True:
            # Get the task
            task, job_id = self.task_queue.get()
            if task is None:
                break

            # Execute the job
            result = task()

            # Save the result to disk
            with open(f"./results/job_{job_id}", "w", encoding="utf-8") as f:
                f.write(result)

            # Update the task state
            self.task_state[f"job_id_{job_id}"] = "done"
