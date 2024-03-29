import logging
import time
from logging.handlers import RotatingFileHandler

from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool

webserver = Flask(__name__)

# Set up logging
logging.Formatter.converter = time.gmtime

logger = logging.getLogger("webserver_logger")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("webserver.log", maxBytes=20000, backupCount=5)
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S %Z')
handler.setFormatter(formatter)

logger.addHandler(handler)

webserver.logger = logger

webserver.tasks_runner = ThreadPool()

# webserver.task_runner.start()

webserver.data_path = "./nutrition_activity_obesity_usa_subset.csv"
webserver.data_ingestor = DataIngestor(webserver.data_path, webserver.tasks_runner.data_loaded)
webserver.job_counter = 1



from app import routes
