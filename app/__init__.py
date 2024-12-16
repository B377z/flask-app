
from flask import Flask, request

app = Flask(__name__)

tasks = [{
    "id": 1,
    "title": "Learn Flask",
    "completed": False
    },
    {
    "id": 2,
    "title": "Build a Web App",
    "completed": False
    }]


@app.route("/")
def home():
    """My Home Page"""
    return "<h1>Welcome to the Task Manager API!</h1>"

@app.route("/tasks")
def about():
    """
    Returns a list of tasks

    """
    return {"tasks": tasks}

@app.route("/tasks", methods=["POST"])
def add_task():
    """
    Adds a new task to the task list.
    """
    task_data = request.json  # Get JSON data from the request
    new_task = {
        "id": len(tasks) + 1,  # Auto-generate a unique ID
        "title": task_data["title"],  # Extract title from input data
        "completed": False,  # Default to not completed
    }
    tasks.append(new_task)  # Add the new task to the global list
    return {"message": "Task added successfully!", "task": new_task}, 201

@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    """
    Marks a task as completed by its ID.
    """
    for task in tasks:
        if task["id"] == task_id:  # Find the task with the matching ID
            task["completed"] = True
            return {"message": "Task updated successfully!", "task": task}, 200
    return {"error": "Task not found"}, 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """
    Deletes a task by its ID.
    """
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]  # Remove task with matching ID
    return {"message": "Task deleted successfully!"}, 200

if __name__ == "__main__":
    app.run(debug=True)

