from http.server import HTTPServer, BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        print("\nIncoming Request")
        print("Path :", self.path)

        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type","text/plain")
            self.end_headers()
            self.wfile.write(b"Welcome to Route API")

        elif self.path == "/routes":

            self.send_response(200)
            self.send_header("Content-Type","text/plain")
            self.end_headers()

            self.wfile.write(b"Showing all routes")

        elif self.path.startswith("/routes/"):

            try:
                route_id=int(self.path.split("/")[2])

                self.send_response(200)
                self.send_header("Content-Type","text/plain")
                self.end_headers()

                self.wfile.write(
                    f"Showing Route {route_id}".encode()
                )

            except:

                self.send_response(400)
                self.end_headers()

                self.wfile.write(b"Invalid Route ID")

        else:

            self.send_response(404)
            self.end_headers()

            self.wfile.write(b"Page Not Found")


server=HTTPServer(("localhost",8000),MyHandler)

print("Server Running on http://localhost:8000")

server.serve_forever()
