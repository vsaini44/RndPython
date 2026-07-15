
from flask import Flask, jsonify, request

app = Flask(__name__)
servers = {
    1: {"id":1,"servername":"Production","os":"Linux","protected":True},
    2: {"id":2,"servername":"Web01","os":"Windows","protected":False}
}

next_id = 3

@app.get("/servers")
def get_servers():
    os_filter = request.args.get("os")
    result = list(servers.values())

    if os_filter:
        result = [s for s in result if s["os"].lower()==os_filter.lower()]

    return jsonify(result),200

@app.get("/servers/<int:server_id>")
def get_server(server_id):

    if server_id not in servers:
        return jsonify({"error":"Server Not Found"}),404

    return jsonify(servers[server_id]),200

@app.post("/servers")
def create_server():

    global next_id
    data = request.get_json()

    if not data:
        return jsonify({"error":"JSON Body Required"}),400

    servers[next_id]={
        "id":next_id,
        "servername":data["servername"],
        "os":data["os"],
        "protected":False
    }

    next_id += 1

    return jsonify(servers[next_id-1]),201

@app.put("/servers/<int:server_id>")
def update_server(server_id):

    if server_id not in servers:
        return jsonify({"error":"Server Not Found"}),404

    data=request.get_json()

    servers[server_id]["servername"]=data.get("servername",servers[server_id]["servername"])
    servers[server_id]["os"]=data.get("os",servers[server_id]["os"])

    return jsonify(servers[server_id]),200

@app.delete("/servers/<int:server_id>")
def delete_server(server_id):

    if server_id not in servers:
        return jsonify({"error":"Server Not Found"}),404

    # Prevent deleting protected server.
    if servers[server_id]["protected"]:
        return jsonify({"error":"Protected Server"}),403

    del servers[server_id]

    # 204 = Success with no body.
    return "",204

if __name__=="__main__":
    app.run(debug=True)
# curl http://localhost:5000/servers
# curl http://localhost:5000/servers/1
# curl http://localhost:5000/servers/500
# curl http://localhost:5000/servers?os=Linux
# curl http
