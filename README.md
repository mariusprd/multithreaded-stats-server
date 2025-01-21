# Le Stats Sportif

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Testing](#testing)
- [Logging](#logging)

## Introduction

**Le Stats Sportif** is a Python-based multi-threaded server application that provides statistical insights derived from a dataset on nutrition, physical activity, and obesity in the United States from 2011 to 2022. Built using the Flask framework, this project demonstrates efficient use of synchronization mechanisms, multithreading, and modular code organization.

The project processes a CSV dataset and serves data-driven answers to statistical queries via a RESTful API.

## Features

- **Multi-threaded Processing:** Efficiently handles multiple concurrent requests using a thread pool.
- **CSV Data Processing:** Reads, processes, and analyzes a large dataset to extract meaningful statistics.
- **REST API:** Provides a variety of endpoints for retrieving statistical insights.
- **Graceful Shutdown:** Ensures all queued jobs are processed before the server shuts down.
- **Logging:** Comprehensive logging using Python’s `logging` module for debugging and monitoring.

## Project Structure

```
.
├── Makefile
├── README.md
├── api_server.py
├── app
│   ├── __init__.py
│   ├── data_ingestor.py
│   ├── routes.py
│   └── task_runner.py
├── checker
│   ├── checker.py
│   └── pylintrc
├── requirements.txt
├── results
│   └── [job results stored here]
├── tests
│   ├── [unit tests and functional tests organized by endpoint]
├── unittests
│   ├── TestWebserver.py
├── nutrition_activity_obesity_usa_subset.csv
└── webserver.log
```

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/le-stats-sportif.git
   cd le-stats-sportif
   ```

2. **Set Up a Virtual Environment**
   ```bash
   make create_venv
   ```

3. **Install Dependencies**
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   make install
   ```

## Usage

1. **Run the Server**
   ```bash
   make run_server
   ```

2. Interact with the server using the provided endpoints to query statistics. See [Endpoints](#endpoints) for detailed usage.

## Endpoints

### `/api/states_mean`
- **Description:** Calculate the mean value of a given question across all states.
- **Request:**
  ```json
  {
    "question": "Percent of adults who engage in no leisure-time physical activity"
  }
  ```
- **Response:** Sorted list of states with their mean values.

### `/api/state_mean`
- **Description:** Calculate the mean value of a given question for a specific state.
- **Request:**
  ```json
  {
    "question": "Percent of adults who engage in no leisure-time physical activity",
    "state": "California"
  }
  ```

### `/api/best5` and `/api/worst5`
- **Description:** Retrieve the top 5 and bottom 5 states for a given question based on mean values.

### `/api/global_mean`
- **Description:** Calculate the global mean value for a given question across all states.

### `/api/diff_from_mean`
- **Description:** Calculate the difference between global mean and state mean for all states.

### `/api/state_diff_from_mean`
- **Description:** Calculate the difference between global mean and state mean for a specific state.

### `/api/mean_by_category` and `/api/state_mean_by_category`
- **Description:** Retrieve the mean values categorized by `Stratification1` and `StratificationCategory1` globally or for a specific state.

### `/api/jobs`
- **Description:** Get the status of all jobs.

### `/api/num_jobs`
- **Description:** Get the number of jobs remaining in the queue.

### `/api/get_results/<job_id>`
- **Description:** Retrieve the result of a specific job.

### `/api/graceful_shutdown`
- **Description:** Shut down the server gracefully after completing all pending jobs.

## Testing

1. **Run Unit Tests**
   ```bash
   python -m unittest discover unittests
   ```

2. **Run Functional Tests**
   ```bash
   make run_tests
   ```

## Logging

The server logs are stored in `webserver.log` using a rotating file handler. Key log levels include:
- **INFO:** Tracks API requests and responses.
- **ERROR:** Logs exceptions and issues during runtime.
