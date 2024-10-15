# Import modules
from flask import Flask, jsonify, request
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
@app.route('/users', methods=['GET'])
@limiter.limit("5 per 10 seconds", "20 per minute") # Same burst + throttle pattern
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

# Get fetch all the tasks [rate limiting + throttling]
@app.route('/tasks', methods=['GET'])
@limiter.limit("5 per 10 seconds", "20 per minute")
def get_tasks():
    """
    Retrieve the list of tasks.
    
    rate limiting + throttling.

    This function returns the current list of tasks in JSON format.
    
    Returns:
        Response: A JSON response containing the tasks.
    """
    return jsonify(tasks)


# POST: Create a new task [rate limiting + throttling]
@app.route('/tasks', methods=['POST'])
@limiter.limit("5 per 10 seconds", "20 per minute")
def create_task():
    """
    Create a new task.
    
    rate limiting + throttling.
    
    This function creates a new task from the JSON data provided in the request.
    It assigns a unique ID to the task based on the current number of tasks and
    appends the new task to the tasks data source.

    Returns:
        tuple: A tuple containing the JSON representations of the new tasks and
                the HTTP code 201 indicating successfully creation of task.
    """
    new_task = request.json
    new_task['id'] = len(tasks)+ 1
    tasks.append(new_task)
    return jsonify(new_task), 201 # 201: Task Creation

# PUT: Update an existing Task [rate limiting + throttling]
@app.route('/tasks/<int:task_id>', methods=['PUT'])
@limiter.limit("5 per 10 seconds", "20 per minute")
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
            return jsonify(task), 200 # 200: Successfully Updated
    return jsonify({"error": "Task not found"}), 404 # 404: Not Found ERROR

# DELETE: Delete a task [rate limiting + throttling]
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@limiter.limit("5 per 10 seconds", "20 per minute")
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
    app.run(debug=True, port=5001, ssl_context=('cert.pem', 'key.pem'))