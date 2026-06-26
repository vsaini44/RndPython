import socket

# The only paths that return 200 OK
VALID_PATHS = ['/', '/hello', '/about']

HOST = 'localhost'
PORT = 8000


def parse_request(raw_request):
    """Pull out the method, path, and User-Agent from a raw HTTP request."""
    lines = raw_request.split('\r\n')

    # First line is like: GET /hello HTTP/1.1
    request_line = lines[0].split(' ')
    method = request_line[0]
    path   = request_line[1]

    # Search the remaining lines for the User-Agent header
    user_agent = 'Unknown'
    for line in lines[1:]:
        if line.lower().startswith('user-agent:'):
            user_agent = line.split(':', 1)[1].strip()
            break

    return method, path, user_agent


def build_200(method, path, user_agent):
    """Build a 200 OK response showing the request details."""
    body = f"""<html>
<body>
    <h1>Request Info</h1>
    <p><strong>Method:</strong> {method}</p>
    <p><strong>Path:</strong> {path}</p>
    <p><strong>Browser:</strong> {user_agent}</p>
</body>
</html>"""

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
        + body
    )
    return response


def build_404():
    """Build a simple 404 Not Found response."""
    body = """<html>
<body>
    <h1>404 Not Found</h1>
    <p>The page you requested does not exist.</p>
</body>
</html>"""

    response = (
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
        + body
    )
    return response


def run():
    # Create a TCP socket and start listening
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse port quickly after restart
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server running at http://{HOST}:{PORT}  (Ctrl+C to stop)")

    while True:
        client_socket, client_address = server.accept()
        print(f"\nConnection from {client_address}")

        # Receive the raw request (4096 bytes is plenty for headers)
        raw_request = client_socket.recv(4096).decode('utf-8', errors='ignore')

        if not raw_request:
            client_socket.close()
            continue

        # Parse it
        method, path, user_agent = parse_request(raw_request)
        print(f"  {method} {path}")

        # Pick the right response
        if path in VALID_PATHS:
            response = build_200(method, path, user_agent)
        else:
            response = build_404()

        # Send and close
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()


if __name__ == '__main__':
    run()
