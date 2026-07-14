from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class ABCHandler(BaseHTTPRequestHandler):

    def do_POST(self):

        # Read request body
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length).decode("utf-8")

        # Convert JSON into Python dictionary
        data = json.loads(body)

        # Write JSON to a file
        with open("servers.json", "w") as f:
            json.dump(data, f, indent=4)

        # Send response
        response = {
            "message": "Server details saved successfully."
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())


server = HTTPServer(("localhost", 8081), ABCHandler)

print("Server started on http://localhost:8081")

server.serve_forever()


#curl -X POST http://localhost:8081 -H "Content-Type: application/json" \
#-d '{
#   "servername":"web01",
#    "ip":"192.168.1.10",
#   "os":"Linux"
#}'
