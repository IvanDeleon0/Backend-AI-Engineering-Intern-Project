const http = require("http");

// Create a basic HTTP server (built-in Node module, no Express needed)
http.createServer((req, res) => {
  // All responses will be JSON
  res.setHeader("Content-Type", "application/json");

  if (req.url === "/api/hello") {
    // GET /api/hello -> returns a static greeting message
    res.end(JSON.stringify({ message: "Hello, world!" }));

  } else if (req.url === "/api/time") {
    // GET /api/time -> returns the current server timestamp (ISO 8601 format)
    res.end(JSON.stringify({ now: new Date().toISOString() }));

  } else {
    // Any other route -> 404 Not Found with a JSON error body
    res.statusCode = 404;
    res.end(JSON.stringify({ error: "Not found" }));
  }
})
// Start listening on port 3000
.listen(3000, () => console.log("Server running at http://localhost:3000"));
