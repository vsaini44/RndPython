from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# -----------------------------
# In-Memory Database
# -----------------------------
servers = {
    1: {
        "servername": "production",
        "ip": "192.168.1.10",
        "protected": True
    }
}

next_id = 2


class ServerHandler(BaseHTTPRequestHandler):

    # -----------------------------
    # GET Methods
    # -----------------------------
    def do_GET(self):

        # GET /servers
        if self.path == "/servers":

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(servers).encode())
            return

        # GET /servers/1
        if self.path.startswith("/servers/"):

            try:
                server_id = int(self.path.split("/")[-1])

                if server_id not in servers:

                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()

                    response = {
                        "error": "Server Not Found"
                    }

                    self.wfile.write(json.dumps(response).encode())
                    return

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                self.wfile.write(json.dumps(servers[server_id]).encode())

            except ValueError:

                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                self.wfile.write(
                    json.dumps({"error": "Invalid Server ID"}).encode()
                )

            return

        self.send_response(404)
        self.end_headers()

    # -----------------------------
    # POST Method
    # -----------------------------
    def do_POST(self):

        global next_id

        if self.path != "/servers":

            self.send_response(404)
            self.end_headers()
            return

        try:

            length = int(self.headers["Content-Length"])

            body = self.rfile.read(length).decode()

            data = json.loads(body)

            servers[next_id] = {
                "servername": data["servername"],
                "ip": data["ip"],
                "protected": False
            }

            response = {
                "message": "Server Created",
                "server_id": next_id
            }

            next_id += 1

            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(response).encode())

        except json.JSONDecodeError:

            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                json.dumps({"error": "Invalid JSON"}).encode()
            )

    # -----------------------------
    # DELETE Method
    # -----------------------------
    def do_DELETE(self):

        if not self.path.startswith("/servers/"):

            self.send_response(404)
            self.end_headers()
            return

        try:

            server_id = int(self.path.split("/")[-1])

            if server_id not in servers:

                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                self.wfile.write(
                    json.dumps({"error": "Server Not Found"}).encode()
                )

                return

            if servers[server_id]["protected"]:

                self.send_response(403)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                self.wfile.write(
                    json.dumps(
                        {"error": "Protected Server. Cannot Delete."}
                    ).encode()
                )

                return

            del servers[server_id]

            self.send_response(204)
            self.end_headers()

        except ValueError:

            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                json.dumps({"error": "Invalid Server ID"}).encode()
            )


server = HTTPServer(("localhost", 8081), ServerHandler)

print("Server running on http://localhost:8081")

server.serve_forever()


#  curl http://localhost:8081/servers | jq
#    curl -X POST http://localhost:8081/servers -H "Content-Type: application/json" -d '{
#    "servername":"web01",
#    "ip":"192.168.1.20"
#}'
#  curl http://localhost:8081/servers | jq
#  curl http://localhost:8081/servers/2 | jq
#  curl http://localhost:8081/servers/3 | jq
#  curl http://localhost:8081/servers/20
#  curl -X POST http://localhost:8081/servers -H "Content-Type: application/json" -d '{"servername":"web01"'
#  curl -X DELETE http://localhost:8081/servers 
#  curl -X DELETE http://localhost:8081/servers/2 
#  curl http://localhost:8081/servers | jq
