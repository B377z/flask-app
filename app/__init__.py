
from flask import Flask, request
from datetime import datetime

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
def get_tasks():
    """
    Retrieves tasks, optionally filtered by completion status.

    """
    status = request.args.get("completed")  # Get the status query parameter
    if status is not None:
        completed_status = status.lower() == "true"  # Check if status is "true"
        filtered_tasks = [task for task in tasks if task["completed"] == completed_status]
        return {"tasks": filtered_tasks}
    return {"tasks": tasks}

@app.route("/tasks", methods=["POST"])
def add_task():
    """
    Adds a new task to the task list.
    """
    task_data = request.json
    try:
        due_date = task_data.get("due_date")  # Optional due date
        if due_date:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        new_task = {
            "id": len(tasks) + 1,
            "title": task_data["title"],
            "completed": False,
            "due_date": due_date,  # Include the due date
        }
        tasks.append(new_task)
        return {"message": "Task added successfully!", "task": new_task}, 201
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD."}, 400

@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    """
    Marks a task as completed by its ID.
    """
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return {"message": "Task updated successfully!", "task": task}, 200
    return {"error": f"Task with ID {task_id} not found."}, 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """
    Deletes a task by its ID.
    """
    global tasks
    filtered_tasks = [task for task in tasks if task["id"] != task_id]
    if len(filtered_tasks) == len(tasks):  # No task was deleted
        return {"error": f"Task with ID {task_id} not found."}, 404
    tasks = filtered_tasks
    return {"message": "Task deleted successfully!"}, 200

@app.route("/tasks/complete_all", methods=["PATCH"])
def complete_all_tasks():
    """
    Marks all tasks as completed.
    """
    for task in tasks:
        task["completed"] = True
    return {"message": "All tasks marked as completed!"}, 200


if __name__ == "__main__":
    app.run(debug=True)

