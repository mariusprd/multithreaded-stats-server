from app import webserver
from flask import request, jsonify

import os
import json

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    print(f"JobID is {job_id}")

    # Check if job_id is valid
    if not webserver.tasks_runner.is_valid(job_id):
        return jsonify({'status': 'error', 'reason': 'Invalid job_id'})
    
    # Check if job_id is done
    if not webserver.tasks_runner.is_done(job_id):
        return jsonify({'status': 'running'})

    with open(f"./results/job_{job_id}", "r") as f:
        res = f.read()

    res = json.loads(res)

    # print(f"Res for job_id {job_id} is {res}")

    return jsonify({'status': 'done', 'data': res})


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    # Get request data
    data = request.json

    # add task to execution
    job = webserver.data_ingestor.states_mean(data['question'])
    webserver.tasks_runner.add_task(job, webserver.job_counter)
    webserver.job_counter += 1
    
    return jsonify({"status": "success", "job_id": webserver.job_counter - 1})


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    # Get request data
    data = request.json

    # add task to execution
    job = webserver.data_ingestor.state_mean(data['question'], data['state'])
    webserver.tasks_runner.add_task(job, webserver.job_counter)
    webserver.job_counter += 1

    return jsonify({"status": "success", "job_id": webserver.job_counter - 1})


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    # Get request data
    data = request.json

    job = webserver.data_ingestor.best5(data['question'])
    webserver.tasks_runner.add_task(job, webserver.job_counter)
    webserver.job_counter += 1
    
    return jsonify({"status": "success", "job_id": webserver.job_counter - 1})


@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    # Get request data
    data = request.json

    job = webserver.data_ingestor.worst5(data['question'])
    webserver.tasks_runner.add_task(job, webserver.job_counter)
    webserver.job_counter += 1
    
    return jsonify({"status": "success", "job_id": webserver.job_counter - 1})


@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    # Get request data
    data = request.json

    job = webserver.data_ingestor.global_mean(data['question'])
    webserver.tasks_runner.add_task(job, webserver.job_counter)
    webserver.job_counter += 1
    
    return jsonify({"status": "success", "job_id": webserver.job_counter - 1})


@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})


@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})


@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})


@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})


@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    # Gracefully shutdown the webserver
    webserver.tasks_runner.graceful_shutdown()
    return jsonify({"status": "success"})


# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
