
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    """My Home Page"""
    return "<h1>Welcome to the Task Manager API!</h1>"

@app.route("/about")
def about():
    return "This is the About page."

if __name__ == "__main__":
    app.run(debug=True)

