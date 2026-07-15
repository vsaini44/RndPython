
from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)
REAL_API_KEY = "my-secret-key"

STORED_HASH = hashlib.sha256(
    REAL_API_KEY.encode()
).hexdigest()

print("\n========== SERVER START ==========")
print("Original API Key :", REAL_API_KEY)
print("Stored SHA256    :", STORED_HASH)
print("==================================\n")


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Demo 2"
    })


@app.route("/users")
def get_users():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({
            "error": "Authorization header missing"
        }), 401
      
    if not auth_header.startswith("Bearer "):
        return jsonify({
            "error": "Invalid Authorization format"
        }), 401

    received_key = auth_header.split(" ")[1]
    received_hash = hashlib.sha256(
        received_key.encode()
    ).hexdigest()

    print("\nIncoming API Key :", received_key)
    print("Incoming SHA256  :", received_hash)

    if received_hash != STORED_HASH:

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


@app.route("/show-hash")
def show_hash():
    return jsonify({
        "stored_hash": STORED_HASH
    })


@app.route("/python-hash")
def python_hash():
    return jsonify({
        "python_hash": hash(REAL_API_KEY)
    })


if __name__ == "__main__":
    app.run(debug=True)

# curl http://127.0.0.1:5000/
# curl http://127.0.0.1:5000/users
# curl -H "Authorization: Bearer hello" http://127.0.0.1:5000/users
# curl -H "Authorization: Bearer my-secret-key" http://127.0.0.1:5000/users
# curl http://127.0.0.1:5000/show-hash
# curl http://127.0.0.1:5000/python-hash
# 
