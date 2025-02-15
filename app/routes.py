'''
    This file contains the definition of the endpoints for the webserver.
'''
import json

from flask import request, jsonify
from app import webserver


def verify_request_decorator(allowed_method):
    '''
        Decorator that verifies the request method
    '''
    def decorator(func):
        def wrapper(*args, **kwargs):
            if request.method == allowed_method:
                return func(*args, **kwargs)
            webserver.logger.error("Method not allowed for %s", request.url)
            return jsonify({"error": "Method not allowed"}), 405
        return wrapper
    return decorator


def post_wrapper(func: callable, state: bool=False):
    '''
        Wrapper function that receives a function and a boolean state
        indicating if the function requires a state parameter.
        It returns a jsonified response with the job_id.
    '''
    data = request.json
    webserver.logger.info("Received request: %s", data)

    try:
        job = func(data['question'], data['state']) if state else func(data['question'])
    except KeyError as e:
        webserver.logger.error("Invalid format of %s", data)
        return jsonify({"status": "error", "reason": f"Invalid format of {data} => {e}"})

    # try to add the task to be executed
    if webserver.tasks_runner.add_task(job, webserver.job_counter) == -1:
        webserver.logger.error("Thread pool is shutting down or already shut down.")
        return jsonify({"status": "error", "reason": "Thread pool was shut down."})

    webserver.job_counter += 1
    webserver.logger.info("Job %s added to the queue", {webserver.job_counter - 1})
    return jsonify({"status": "success", "job_id": webserver.job_counter - 1})


@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    '''
        Example POST endpoint that receives JSON data and returns a JSON response
    '''
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    # Method Not Allowed
    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/get_results/<job_id>', methods=['GET'])
@verify_request_decorator('GET')
def get_response(job_id):
    '''
        Returns the result of a job given a job_id
    '''
    webserver.logger.info("Getting response for job_id: %s", job_id)

    if not webserver.tasks_runner.is_valid(job_id):
        webserver.logger.error("Invalid job_id: %s", job_id)
        return jsonify({'status': 'error', 'reason': 'Invalid job_id'})

    if not webserver.tasks_runner.is_done(job_id):
        webserver.logger.info("Job %s is still running", job_id)
        return jsonify({'status': 'running'})

    with open(f"./results/job_{job_id}", "r", encoding="utf-8") as f:
        res = json.loads(f.read())

    webserver.logger.info("Returning response for job_id: %s", job_id)
    return jsonify({'status': 'done', 'data': res})


@webserver.route('/api/states_mean', methods=['POST'], endpoint='states_mean')
@verify_request_decorator('POST')
def states_mean_request():
    '''
        Submit states_mean job to execution
    '''
    return post_wrapper(webserver.data_ingestor.states_mean)


@webserver.route('/api/state_mean', methods=['POST'], endpoint='state_mean')
@verify_request_decorator('POST')
def state_mean_request():
    '''
        Submit state_mean job to execution
    '''
    return post_wrapper(webserver.data_ingestor.state_mean, state=True)


@webserver.route('/api/best5', methods=['POST'], endpoint='best5')
@verify_request_decorator('POST')
def best5_request():
    '''
        Submit best5 job to execution
    '''
    return post_wrapper(webserver.data_ingestor.best5)


@webserver.route('/api/worst5', methods=['POST'], endpoint='worst5')
@verify_request_decorator('POST')
def worst5_request():
    '''
        Submit worst5 job to execution
    '''
    return post_wrapper(webserver.data_ingestor.worst5)


@webserver.route('/api/global_mean', methods=['POST'], endpoint='global_mean')
@verify_request_decorator('POST')
def global_mean_request():
    '''
        Submit global_mean job to execution
    '''
    return post_wrapper(webserver.data_ingestor.global_mean)


@webserver.route('/api/diff_from_mean', methods=['POST'], endpoint='diff_from_mean')
@verify_request_decorator('POST')
def diff_from_mean_request():
    '''
        Submit diff_from_mean job to execution
    '''
    return post_wrapper(webserver.data_ingestor.diff_from_mean)


@webserver.route('/api/state_diff_from_mean', methods=['POST'], endpoint='state_diff_from_mean')
@verify_request_decorator('POST')
def state_diff_from_mean_request():
    '''
        Submit state_diff_from_mean job to execution
    '''
    return post_wrapper(webserver.data_ingestor.state_diff_from_mean, state=True)


@webserver.route('/api/mean_by_category', methods=['POST'], endpoint='mean_by_category')
@verify_request_decorator('POST')
def mean_by_category_request():
    '''
        Submit mean_by_category job to execution
    '''
    return post_wrapper(webserver.data_ingestor.mean_by_category)


@webserver.route('/api/state_mean_by_category', methods=['POST'], endpoint='state_mean_by_category')
@verify_request_decorator('POST')
def state_mean_by_category_request():
    '''
        Submit state_mean_by_category job to execution
    '''
    return post_wrapper(webserver.data_ingestor.state_mean_by_category, state=True)


@webserver.route('/api/graceful_shutdown', methods=['GET'], endpoint='graceful_shutdown')
@verify_request_decorator('GET')
def graceful_shutdown():
    '''
        Gracefully shuts down the webserver
    '''
    webserver.tasks_runner.graceful_shutdown()
    webserver.logger.info("Webserver shutdown")
    return jsonify({"status": "success"})


@webserver.route('/api/jobs', methods=['GET'], endpoint='jobs')
@verify_request_decorator('GET')
def get_jobs():
    '''
        Returns the current status of all jobs
    '''
    webserver.logger.info("Getting jobs...")
    jobs = webserver.tasks_runner.get_jobs()
    webserver.logger.info("Got jobs status")
    return jsonify({"status": "done", "jobs": jobs})


@webserver.route('/api/num_jobs', methods=['GET'], endpoint='num_jobs')
@verify_request_decorator('GET')
def get_num_jobs():
    '''
        Returns the number of jobs in the queue
    '''
    webserver.logger.info("Getting number of jobs...")
    num_jobs = webserver.tasks_runner.get_num_jobs()
    webserver.logger.info("Got number of jobs")
    return jsonify({"status": "done", "num_jobs": num_jobs})


@webserver.route('/')
@webserver.route('/index')
def index():
    '''
        Default route that displays a welcome message and the defined routes
    '''
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = "".join([f"<p>{route}</p>" for route in routes])

    msg += paragraphs
    return msg

def get_defined_routes():
    '''
        Returns a list of all the defined routes in the webserver
    '''
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
