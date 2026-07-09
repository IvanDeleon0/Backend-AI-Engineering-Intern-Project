from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime, timezone

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        if self.path == "/api/hello":
            data = {"message": "Hello, world!"}
        elif self.path == "/api/time":
            data = {"now": datetime.now(timezone.utc).isoformat("DD HH:mm a")}
        else:
            self.send_response(404)
            data = {"error": "Not found"}

        self.wfile.write(json.dumps(data).encode())

if __name__ == "__main__":
    server = HTTPServer(("localhost", 3000), Handler)
    print("Server running at http://localhost:3000")
    server.serve_forever()