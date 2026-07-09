const http = require("http");

http.createServer((req, res) => {
  res.setHeader("Content-Type", "application/json");
  if (req.url === "/api/hello") {
    res.end(JSON.stringify({ message: "Hello, world!" }));
  } else if (req.url === "/api/time") {
    res.end(JSON.stringify({ now: new Date().toISOString() }));
  } else {
    res.statusCode = 404;
    res.end(JSON.stringify({ error: "Not found" }));
  }
}).listen(3000, () => console.log("Server running at http://localhost:3000"));