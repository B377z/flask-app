
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

# Sample tasks data
tasks = [
    {
        "id": 1,
        "title": "Learn Flask",
        "completed": False,
        "priority": "High",
        "created_at": "2024-12-17T10:00:00Z",
        "due_date": "2024-12-20",
    },
    {
        "id": 2,
        "title": "Build a Web App",
        "completed": False,
        "priority": "Medium",
        "created_at": "2024-12-17T10:30:00Z",
        "due_date": None,
    },
    {
        "id": 3,
        "title": "Deploy App to Cloud",
        "completed": False,
        "priority": "Low",
        "created_at": "2024-12-17T11:00:00Z",
        "due_date": "2024-12-25",
    }
]


@app.route("/")
def home():
    """My Home Page"""
    return "<h1>Welcome to the Task Manager API!</h1>"

@app.route("/tasks")
def get_tasks():
    """
    Retrieves tasks with filtering, sorting, and pagination.
    """
    # Get query parameters
    status = request.args.get("completed")  # Filter by completion status
    priority = request.args.get("priority")  # Filter by priority
    sort_by = request.args.get("sort_by", "id")  # Default sorting field
    order = request.args.get("order", "asc")  # Default sorting order
    page = int(request.args.get("page", 1))  # Default to page 1
    limit = int(request.args.get("limit", 5))  # Default to 5 items per page

    # Start with all tasks
    filtered_tasks = tasks

    # Filter by completion status if provided
    if status is not None:
        completed_status = status.lower() == "true"
        filtered_tasks = [task for task in filtered_tasks if task["completed"] == completed_status]

    # Filter by priority if provided
    if priority:
        if priority not in ["High", "Medium", "Low"]:
            return {"error": f"Invalid priority: {priority}. Must be 'High', 'Medium', or 'Low'."}, 400
        filtered_tasks = [task for task in filtered_tasks if task["priority"] == priority]

    # Validate the sort_by field
    valid_sort_fields = {"id", "title", "due_date", "completed", "priority", "created_at"}
    sort_by_fields = sort_by.split(",")  # Support multiple sorting fields
    for field in sort_by_fields:
        if field not in valid_sort_fields:
            return {"error": f"Invalid sort_by field: {field}. Valid fields are: {', '.join(valid_sort_fields)}"}, 400

    # Sort tasks by multiple fields
    sorted_tasks = sorted(
        filtered_tasks,
        key=lambda x: tuple(x.get(field, "") for field in sort_by_fields),
        reverse=(order == "desc")
    )

    # Implement pagination
    start = (page - 1) * limit
    end = start + limit
    paginated_tasks = sorted_tasks[start:end]

    # Check if the requested page is out of range
    if not paginated_tasks and page > 1:
        return {"error": f"Page {page} is out of range."}, 404

    return {
        "tasks": paginated_tasks,
        "pagination": {
            "page": page,
            "limit": limit,
            "total_tasks": len(filtered_tasks),
            "total_pages": (len(filtered_tasks) + limit - 1) // limit  # Ceiling division
        }
    }


@app.route("/tasks", methods=["POST"])
def add_task():
    """
    Adds a new task to the task list.
    """
    task_data = request.json
    try:
        # Validate due_date if provided
        due_date = task_data.get("due_date")
        if due_date:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").strftime("%Y-%m-%d")

        # Validate priority
        priority = task_data.get("priority", "Medium")  # Default to "Medium"
        if priority not in ["High", "Medium", "Low"]:
            return {"error": "Invalid priority. Must be 'High', 'Medium', or 'Low'."}, 400

        # Generate created_at timestamp
        created_at = datetime.utcnow().isoformat() + "Z"

        # Create the new task
        new_task = {
            "id": len(tasks) + 1,
            "title": task_data["title"],
            "completed": False,
            "priority": priority,
            "created_at": created_at,
            "due_date": due_date,
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

