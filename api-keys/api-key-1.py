
from flask import Flask, request, jsonify


app = Flask(__name__)
API_KEY = "my-secret-key"


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Demo 1"
    })


@app.route("/users")
def get_users():
  
    auth_header = request.headers.get("Authorization")
    api_key_header = request.headers.get("X-API-Key")
    received_key = None

    if auth_header:
        if auth_header.startswith("Bearer "):
            received_key = auth_header.split(" ")[1]
          
    elif api_key_header:
        received_key = api_key_header

    else:

        return jsonify({
            "error": "API Key Missing"
        }), 401

    if received_key != API_KEY:
        return jsonify({
            "error": "Invalid API Key"
        }), 401
    return jsonify([
        {
            "id": 1,
            "name": "Alice"
        },
        {
            "id": 2,
            "name": "Bob"
        }
    ])


# Run Flask server
if __name__ == "__main__":
    app.run(debug=True)


# curl http://127.0.0.1:5000/
# curl http://127.0.0.1:5000/users
# curl -H "Authorization: Bearer wrong-key" http://127.0.0.1:5000/users
# curl -H "Authorization: Bearer my-secret-key" http://127.0.0.1:5000/users
# curl -H "X-API-Key: my-secret-key" http://127.0.0.1:5000/users
