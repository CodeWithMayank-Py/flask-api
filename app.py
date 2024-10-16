# Import modules
from flask import Flask, jsonify, request, url_for
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initializes Flask App
app = Flask(__name__)

# Enabl CORS for all routes
CORS(app)

# Initialize Flask-Limiter with multiple rate limits (rate limiting + throttling)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute", "100 per hour"]    # Limiting to 10 requests per minute and 100 per hour
)

# Dummy data to simulate resources
users = [
    {"id":1, "name": "John Smith"},
    {"id":2, "name": "Pirate Jacky"},
]

tasks = [
    {"id":1, "title": "Working on Daily Reports", "description": "Day 1"},
    {"id":2, "title": "Sailing the ship", "description": "Roaming around the world"},
]

# Helper function to add HATEOAS links
def add_hateoas_links(task):
    task_id = task['id']
    task['links']= [
        {"rel": "self", "href": url_for('get_task', task_id=task_id, _external=True)},
        {"rel": "delete", "href": url_for('delete_task', task_id=task_id, _external=True), "method": "DELETE"},
        {"rel": "update", "href": url_for('update_task', task_id=task_id, _external=True), "method": "PUT"},
        {"rel": "list", "href": url_for('get_tasks', _external=True), "method": "GET"}
    ]
    return task

# Standardized error response format
def error_response(status_code, error, message):
    response = jsonify({"error": error, "message": message})
    response.status_code = status_code
    return response

# Custom Handlers
@app.errorhandler(404)
def not_found(error):
    return error_response(404, "Not Found", "The requested resource does not exist")

@app.errorhandler(400)
def bad_request(error):
    return error_response(400, "Bad Request", "The request could not be understood or was missing required parameters")

@app.errorhandler(401)
def unauthorized(error):
    return error_response(401, "Unauthorized", "Authentication is required to access this resource")

@app.errorhandler(429)
def too_many_request(error):
    return error_response(429, "Too Many Requests", "You have exceeded the request limit. Please try again later.")


# Homepage
@app.route('/')
def homepage():
    """
    Display the message on / route

    Returns:
        message: Hello Developers Message on / route as a sign of homepage.
    """
    return "Hello, Developers! Welcome to simple flask APIs."

# Get fetch all users using GET method [Rate limiting + throttling]
@app.route('/api/v1/users', methods=['GET'])
@limiter.limit("5 per 10 seconds")  # Burst limit
@limiter.limit("20 per minute")     # Throttle limit
def get_users():
    """
    Retrieves the list of uesrs.
    
    rate limiting + throttling.
    
    This function fetches and returns a list of users from the data source.
    The data source could be a database, an API or any other data storage system.

    Returns:
        list: A list of users objects or dictionaries containing user information.
    """
    return jsonify(users)


# GET: Fetch a single task [rate limiting + throttling], HATEOAS-enabled
@app.route('/api/v1/tasks/<int:task_id>', methods=['GET'])
@limiter.limit("5 per 10 seconds")  # Burst Limit
@limiter.limit("20 per minute")     # Throttle Limit
def get_task(task_id):
    """
    Retrieve a task by its ID and return it with HATEOAS links if found.

    Args:
        task_id (int): The unique identifier of the task to retrieve.

    Returns:
        Response: A JSON] response containing the task with HATEOAS links if found,
                  or an error message with a 404 status code if not found.
    """
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        return jsonify(add_hateoas_links(task))
    return jsonify({"error": "Task not found"}), 404


# Get fetch all the tasks [rate limiting + throttling], HATEOAS-enabld
@app.route('/api/v1/tasks', methods=['GET'])
@limiter.limit("5 per 10 seconds")  # Burst limit
@limiter.limit("20 per minute")     # Throttle limit
def get_tasks():
    """
    Retrieve the list of tasks.
    
    rate limiting + throttling.

    This function returns the current list of tasks in JSON format.
    
    Returns:
        Response: A JSON response containing the tasks.
    """
    tasks_with_link = [add_hateoas_links(task) for task in tasks]
    return jsonify(tasks_with_link)


# POST: Create a new task [rate limiting + throttling]
@app.route('/api/v1/tasks', methods=['POST'])
@limiter.limit("5 per 10 seconds")  # Burst limit
@limiter.limit("20 per minute")     # Throttle limit
def create_task():
    """
    Create a new task.
    
    A
    
    rate limiting + throttling.
    
    This function creates a new task from the JSON data provided in the request.
    It assigns a unique ID to the task based on the current number of tasks and
    appends the new task to the tasks data source.

    Returns:
        tuple: A tuple containing the JSON representations of the new tasks and
                the HTTP code 201 indicating successfully creation of task.
    """
    new_task = request.json
    if not new_task or "title" not in new_task:
        return bad_request("Missing 'title' field in request body")
    
    new_task['id'] = len(tasks)+ 1
    tasks.append(new_task)
    return jsonify(add_hateoas_links(new_task)), 201 # 201: Task Creation

# PUT: Update an existing Task [rate limiting + throttling], [Idempotent]
@app.route('/api/v1/tasks/<int:task_id>', methods=['PUT'])
@limiter.limit("5 per 10 seconds")  # Burst limit
@limiter.limit("20 per minute")     # Throttle limit
def update_task(task_id):
    """
    Updates an existing data with the provided task_id.
    
    rate limiting + throttling.
    
    This function retrieves the updated task data from the request's JSON payload
    and updates the corresponding task in the tasks list if it exists.
    
    Args:
        task_id (int): The unique identifier of the task to be updated.

    Returns:
        Response: A JSON response containing the updated task and the status code 200
        if the task is successfully updated.
        A JSON response with an error message and a status code of 404 if the
        task with the given task_id is not found.
    """
    updated_task = request.json
    for task in tasks:
        if task['id'] == task_id:
            task.update(updated_task)
            return jsonify(add_hateoas_links(task)), 200 # 200: Successfully Updated
    
    # If the task does not exist, you should create it (optional based on API design)
    new_task = updated_task
    new_task['id'] = task_id
    tasks.append(new_task)
    return jsonify(add_hateoas_links(new_task)), 201   # Returns 201 created if new task is added

# DELETE: Delete a task [rate limiting + throttling], [Idempotent]
@app.route('/api/v1/tasks/<int:task_id>', methods=['DELETE'])
@limiter.limit("5 per 10 seconds")  # Burst limit
@limiter.limit("20 per minute")     # Throttle limit
def delete_task(task_id):
    """
    Delete an existing data with the given task_id.
    
    rate limiting + throttling.
    
    This function retrieves the deleted task data from the request's JSON payload
    and deletes the corresponding task in the tasks list if it exist.

    Args:
        task_id (int): The unique identfier of task to be deleted.

    Returns:
        Response: A JSON containing the deleted tasks and status code of 200
        if the task deleted successfully.
        A JSON response with the error message and status code of 404
        if the taskwith the given task_id is not found.
    """
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            return jsonify({"message": "Task delete successfully"}), 200 # 200: Successfully deleted
    return jsonify({"error": "Task not found"}), 404 # Not Found Error

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True, port=5001, ssl_context=('cert.pem', 'key.pem')) 
    # SSl included in above, Self-signed ceritficte