from flask import Flask, request, jsonify
import psutil
import time

app = Flask(__name__)

# In-memory data
data = {
    "interfaces": {},
    "macs": {},
    "routes": {}
}

# Load interface and MAC information
for name, addrs in psutil.net_if_addrs().items():
    data["interfaces"][name] = {"name": name}

    for addr in addrs:
        if "AF_LINK" in str(addr.family):
            data["macs"][name] = addr.address

# Sample routes
data["routes"] = {
    1: {"destination": "192.168.1.0/24", "gateway": "192.168.1.1"},
    2: {"destination": "10.0.0.0/24", "gateway": "10.0.0.1"}
}


@app.before_request
def before():
    request.start = time.time()
    print(f"Client IP : {request.remote_addr}")
    print(f"User-Agent: {request.headers.get('User-Agent')}")


@app.after_request
def after(response):
    duration = time.time() - request.start
    print(f"{request.method} {request.path} took {duration:.4f} seconds\n")
    return response


# ---------------- Interfaces ----------------

@app.route("/interfaces", methods=["GET"])
def interfaces():
    return jsonify(data["interfaces"])


# ---------------- MAC Addresses ----------------

@app.route("/macs", methods=["GET"])
def macs():
    return jsonify(data["macs"])


# ---------------- Routes ----------------

@app.route("/routes", methods=["GET"])
def get_routes():
    return jsonify(data["routes"])


@app.route("/routes", methods=["POST"])
def add_route():
    body = request.get_json()

    new_id = max(data["routes"].keys(), default=0) + 1
    data["routes"][new_id] = body

    return jsonify({"message": "Route Added", "id": new_id}), 201


@app.route("/routes/<int:id>", methods=["PUT"])
def update_route(id):

    if id not in data["routes"]:
        return jsonify({"error": "Route not found"}), 404

    data["routes"][id] = request.get_json()

    return jsonify({"message": "Route Updated"})


@app.route("/routes/<int:id>", methods=["DELETE"])
def delete_route(id):

    if id not in data["routes"]:
        return jsonify({"error": "Route not found"}), 404

    del data["routes"][id]

    return jsonify({"message": "Route Deleted"})


# ---------------- Search ----------------

@app.route("/search", methods=["GET"])
def search():

    term = request.args.get("q", "").lower()

    result = {}

    for section, values in data.items():

        matches = {}

        for key, value in values.items():

            text = str(key).lower() + str(value).lower()

            if term in text:
                matches[key] = value

        if matches:
            result[section] = matches

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)


# curl http://localhost:5000/interfaces
# curl http://localhost:5000/macs
# curl http://localhost:5000/routes
# curl -X POST http://localhost:5000/routes -H "Content-Type: application/json" -d '{"destination":"172.16.0.0/24","gateway":"172.16.0.1"}'
# curl -X PUT http://localhost:5000/routes/1 -H "Content-Type: application/json" -d '{"destination":"192.168.100.0/24","gateway":"192.168.100.1"}'
# curl -X DELETE http://localhost:5000/routes/2
# curl "http://localhost:5000/search?q=192"
# curl "http://localhost:5000/search?q=eth"
