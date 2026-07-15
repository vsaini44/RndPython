# Import the Flask class from the flask package. Flask is the main class used to create a web application.
from flask import Flask

# Create a Flask application object. __name__ tells Flask where the application is located.
#Flask uses this information to locate templates, static files,and other application resources.
app = Flask(__name__)

# @app.route("/") is called a DECORATOR.
# It tells Flask: "Whenever a user visits the URL '/', execute the function below."
# URL: http://localhost:5000/
@app.route("/")
def home():
    # Whatever this function returns becomes the HTTP response, Since this is HTML, the browser renders it as a Heading.
    return "<h1>Welcome to Flask!</h1>"

# Route for "/about" -> URL: http://localhost:5000/about
# Whenever this URL is requested, Flask executes the about() function.
@app.route("/about")
def about():
    # Returning plain text.Flask automatically creates the HTTP Response.
    return "Innovation In Software Flask Training"

# Route for "/trainer" ->  URL: http://localhost:5000/trainer
@app.route("/trainer")
def trainer():
    return "Trainer: Vishal"

# This condition checks whether this file is being executed directly.
# If we run: python app.py  then __name__ becomes "__main__" and the Flask server starts.
# If another Python file imports this file, the server will NOT start automatically.
if __name__ == "__main__":
    app.run(debug=True)
  # app.run(host="0.0.0.0", port=5000)
