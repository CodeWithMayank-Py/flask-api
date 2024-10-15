# Import modules
from flask import Flask, jsonify, request

app = Flask(__name__)

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

# Get fetch all users using GET method
@app.route('/users', methods=['GET'])
def get_users():
    """
    Retrieves the list of uesrs.
    
    This function fetches and returns a list of users from the data source.
    The data source could be a database, an API or any other data storage system.

    Returns:
        list: A list of users objects or dictionaries containing user information.
    """
    return jsonify(users)

# POST: Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    """
    Create a new task.
    
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

# PUT: Update an existing Task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Updates an existing data with the provided task_id.
    
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

# DELETE: Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            return jsonify({"message": "Task delete successfully"}), 200 # 200: Successfully deleted
    return jsonify({"error": "Task not found"}), 404 # Not Found Error

if __name__ == '__main__':
    app.run(debug=True)