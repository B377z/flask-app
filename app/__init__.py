
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
    },
    {
    "id": 3,
    "title": "Submit Report!",
    "completed": False,
    "due_date": "2021-12-20"
    }
    ]


@app.route("/")
def home():
    """My Home Page"""
    return "<h1>Welcome to the Task Manager API!</h1>"

@app.route("/tasks")
def get_tasks():
    """
    Retrieves tasks, optionally filtered by completion status and/or sorted by a field.
    """
    status = request.args.get("completed")  # Get the "completed" filter
    sort_by = request.args.get("sort_by", "id")  # Default sorting field is "id"
    order = request.args.get("order", "asc")  # Default sorting order is ascending

    # Filter tasks by completion status, if provided
    if status is not None:
        completed_status = status.lower() == "true"
        filtered_tasks = [task for task in tasks if task["completed"] == completed_status]
    else:
        filtered_tasks = tasks  # No filtering if "completed" is not specified

    # Validate the sort_by field
    valid_sort_fields = {"id", "title", "due_date", "completed"}  # Add valid fields here
    if sort_by not in valid_sort_fields:
        return {"error": f"Invalid sort_by field: {sort_by}. Valid fields are: {', '.join(valid_sort_fields)}"}, 400

    # Sort tasks by the specified field
    sorted_tasks = sorted(
        filtered_tasks,
        key=lambda x: x.get(sort_by, ""),  # Use the field specified in "sort_by"
        reverse=(order == "desc")  # Reverse the sorting for descending order
    )

    return {"tasks": sorted_tasks}



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

