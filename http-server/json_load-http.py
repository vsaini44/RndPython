from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class ABCHandler(BaseHTTPRequestHandler):

    def do_POST(self):

        try:
            # Read request body
            length = int(self.headers["Content-Length"])
            body = self.rfile.read(length).decode("utf-8")

            # Parse JSON
            data = json.loads(body)

            # Validate required field
            if "servername" not in data:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                response = {
                    "error": "Missing required field: servername"
                }

                self.wfile.write(json.dumps(response).encode())
                return

            # Success response
            response = {
                "message": f"Hello {data['servername']}"
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(response).encode())

        except json.JSONDecodeError:
            # Invalid JSON
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response = {
                "error": "Invalid JSON format"
            }

            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            # Unexpected server error
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response = {
                "error": "Internal Server Error"
            }

            # Print actual error on server console for debugging
            print("Server Error:", e)

            self.wfile.write(json.dumps(response).encode())


server = HTTPServer(("localhost", 8081), ABCHandler)

print("Server started on http://localhost:8081")

server.serve_forever()




#################
# to execute 
# curl -X POST http://localhost:8081 -H "Content-Type: application/json" -d '{"servername":"vishal"}' -> proper output(200)
# curl -X POST http://localhost:8081 -H "Content-Type: application/json" -d '{"servername":"vishal"' -> invalid json(400)
# curl -X POST http://localhost:8081 -H "Content-Type: application/json" -d '{"hostname":"server1"}'  -> key missing (400)
# 
