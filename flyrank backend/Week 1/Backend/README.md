# Simple Node.js API Server

A minimal HTTP server built with Node's core `http` module (no dependencies).

## Endpoints

| Method | Route        | Description                          |
|--------|--------------|---------------------------------------|
| GET    | `/api/hello` | Returns `{ "message": "Hello, world!" }` |
| GET    | `/api/time`  | Returns `{ "now": "<current ISO timestamp>" }` |
| *      | any other    | Returns 404 `{ "error": "Not found" }` |

## Running

\```bash
node server.js
\```

Server starts at `http://localhost:3000`.

## Example

\```bash
curl http://localhost:3000/api/hello
# {"message":"Hello, world!"}
\```
