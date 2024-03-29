from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

# webserver.task_runner.start()

webserver.data_path = "./nutrition_activity_obesity_usa_subset.csv"
webserver.data_ingestor = DataIngestor(webserver.data_path, webserver.tasks_runner.data_loaded)
webserver.job_counter = 1

from app import routes
