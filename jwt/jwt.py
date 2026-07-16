# pip install flask 
# pip install PyJWT

from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)
SECRET_KEY = "my-secret-key"

@app.route("/")
def home():
    return "JWT Authentication Demo"

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
  
    if username == "admin" and password == "password":
        token = jwt.encode(
            {
                "username": username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
            },
            SECRET_KEY,
            algorithm="HS256"
        )

        return jsonify({
            "token": token
        })

    return jsonify({
        "message": "Invalid Credentials"
    }), 401

@app.route("/profile")
def profile():

    auth = request.headers.get("Authorization")

    if not auth:
        return jsonify({
            "message": "Token Missing"
        }), 401

    try:

        token = auth.split()[1]

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return jsonify({
            "message": f"Welcome {payload['username']}"
        })

    except jwt.ExpiredSignatureError:

        return jsonify({
            "message": "Token Expired"
        }), 401

    except jwt.InvalidTokenError:

        return jsonify({
            "message": "Invalid Token"
        }), 401

if __name__ == "__main__":
    app.run(debug=True)




# curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"password\"}"
# curl -H "Authorization: Bearer YOUR_TOKEN" http://127.0.0.1:5000/profile
# curl http://127.0.0.1:5000/profile
# curl -H "Authorization: Bearer abc123" http://127.0.0.1:5000/profile
# curl -H "Authorization: Bearer YOUR_TOKEN" http://127.0.0.1:5000/profile
