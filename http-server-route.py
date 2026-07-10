[root@vishal work]# cat myserver.py 
from http.server import HTTPServer, BaseHTTPRequestHandler

class abchandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print("GET Request Received with path")
        print(self.path)

        if self.path == "/":
          self.send_response(200)
          self.send_header("Content-Type","text/plain")
          self.end_headers()
          self.wfile.write(b"welcome to the default root route")
        
        elif self.path == "/app":
          self.send_response(200)
          self.send_header("Content-Type","text/plain")
          self.end_headers()
          self.wfile.write(b"welcome to the app route")


        elif self.path == "/backend":
          self.send_response(200)
          self.send_header("Content-Type","text/plain")
          self.end_headers()
          self.wfile.write(b"welcome to the backend route")

        else:
          self.send_response(404)
          self.end_headers()
          self.wfile.write(b"Page Not Found")


    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)          # data sent by client
        print("POST Request Received:", body)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"POST received: " + body)

server=HTTPServer(("localhost",8081),abchandler)
print("server started on localhost:8081")

server.serve_forever()
