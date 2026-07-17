from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def dashboard():
    user = "John"

    api_keys = [
        "ABC123",
        "XYZ456",
        "TEST789"
    ]

    return render_template(
        "dashboard.html",
        user=user,
        api_keys=api_keys
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
