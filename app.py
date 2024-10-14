# Import modules
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory list of tasks
tasks = [
    {"id":1, "title": "Learn Python", "done": False},
    {"id":2, "title": "Learn Flask", "done": False},
]

# Home route
@app.route('/')
def hello_world():
    return "Hello World!"

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# Create the task
@app.route('/tasks', methods=['POST'])
def create_tasks():
    new_task = request.json
    tasks.append(new_task)
    return jsonify(new_task), 201

# Get a single task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_byID(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({"error":"Task Not found"}), 404
    return jsonify(task)

if __name__ == '__main__':
    app.run(debug=True)