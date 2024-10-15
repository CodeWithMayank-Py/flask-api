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
    return jsonify(users)

# POST: Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    new_task = request.json
    new_task['id'] = len(tasks)+ 1
    tasks.append(new_task)
    return jsonify(new_task), 201 # 201: Task Creation

# PUT: Update an existing Task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    updated_task = request.json
    for task in tasks:
        if task['id'] == task_id:
            task.update(updated_task)
            return jsonify(task), 200 # 200: Successfully Updated
    return jsonify({"error": "Task not found"}), 404 # 404: Not Found ERROR

# DELETE: Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    delete_task = request.json
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            return jsonify({"message": "Task delete successfully"}), 200 # 200: Successfully deleted
    return jsonify({"error": "Task not found"}), 404 # Not Found Error

if __name__ == '__main__':
    app.run(debug=True)