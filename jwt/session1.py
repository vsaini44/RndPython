from flask import Flask, request, session, jsonify
app = Flask(__name__)

# Secret key used to sign session cookies
app.secret_key = "my-secret-key"

@app.route("/")
def home():
    return "Session Authentication Demo"

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "password":
        session["user"] = username

        return jsonify({
            "message": "Login Successful"
        }), 200

    return jsonify({
        "message": "Invalid Credentials"
    }), 401


@app.route("/profile")
def profile():
    if "user" not in session:
        return jsonify({
            "message": "Unauthorized"
        }), 401

    return jsonify({
        "message": f"Welcome {session['user']}"
    })

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({
        "message": "Logged Out"
    })

if __name__ == "__main__":
    app.run(debug=True)


# curl -c cookie.txt -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"password\"}"
# curl -b cookie.txt http://127.0.0.1:5000/profile
# curl http://127.0.0.1:5000/profile
# curl -b cookie.txt -X POST http://127.0.0.1:5000/logout
# curl -b cookie.txt http://127.0.0.1:5000/profile
