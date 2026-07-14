from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class abchandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length)          # data sent by client
        
        data = json.loads(body)
        response = {
            "message": "hello " + data["servername"]
        }
         
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())

server=HTTPServer(("localhost",8081),abchandler)
print("server started on localhost:8081")

server.serve_forever()



#######################
#### to call
# curl -X POST http://localhost:8081 -H "Content-Type: application/json" -d '{"servername":"vishal"}'
