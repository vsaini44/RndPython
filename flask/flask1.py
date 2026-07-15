from flask import Flask

app = Flask(__name__)
@app.route("/")
def home():
    return "<h1>Welcome to Flask!</h1>"

@app.route("/about")
def about():
    return "Innovation In Software Flask Training"

@app.route("/trainer")
def trainer():
    return "Trainer: Vishal"

if __name__ == "__main__":
    app.run(debug=True)
  
