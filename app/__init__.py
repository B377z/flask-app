
from flask import Flask

app = Flask(__name__)

tasks = [{
    "id": 1,
    "title": "Learn Flask",
    "Completed": False
    },
    {
    "id": 2,
    "title": "Build a Web App",
    "Completed": False
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

if __name__ == "__main__":
    app.run(debug=True)

