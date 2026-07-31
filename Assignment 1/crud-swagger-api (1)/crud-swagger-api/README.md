# Task CRUD API (Express + Swagger)

A simple, fully-working CRUD REST API for managing "tasks", built with Node.js and Express,
and documented with Swagger (OpenAPI 3.0) via `swagger-jsdoc` + `swagger-ui-express`.

Data is stored in memory (resets on server restart) so you can run it immediately with no
database setup. Swap `models/taskModel.js` for a real database layer later without touching
the routes.

## Project structure

```
crud-swagger-api/
├── config/
│   └── swagger.js       # OpenAPI definition + schema components
├── models/
│   └── taskModel.js      # In-memory data store (swap for a DB later)
├── routes/
│   └── tasks.js           # CRUD routes with Swagger JSDoc annotations
├── server.js               # Express app entry point
└── package.json
```

## Setup

```bash
npm install
npm start
```

The API runs at **http://localhost:3000** by default (set `PORT` env var to change it).

For auto-restart on file changes during development:

```bash
npm run dev
```

## Swagger / API docs

- Interactive Swagger UI: **http://localhost:3000/api-docs**
- Raw OpenAPI JSON spec: **http://localhost:3000/api-docs.json** (importable into Postman, Insomnia, etc.)

## Endpoints

| Method | Path         | Description                     |
|--------|--------------|----------------------------------|
| GET    | /tasks       | List all tasks (optional `?done=true/false` and `?search=<text>` filters, combinable) |
| GET    | /tasks/:id   | Get a single task by ID          |
| POST   | /tasks       | Create a new task                |
| PUT    | /tasks/:id   | Update an existing task          |
| DELETE | /tasks/:id   | Delete a task                    |

### Filtering

| Query    | Example              | Effect                                  |
|----------|----------------------|-------------------------------------------|
| `done`   | `?done=true`         | Only finished tasks                       |
| `done`   | `?done=false`        | Only open tasks                           |
| `search` | `?search=milk`       | Title contains the word (case-insensitive) |

Filters can be combined: `?done=false&search=book`

### Example requests

**Create a task**
```bash
curl -X POST http://localhost:3000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

**Get all tasks**
```bash
curl http://localhost:3000/tasks
curl "http://localhost:3000/tasks?done=true"
curl "http://localhost:3000/tasks?search=milk"
```

**Update a task**
```bash
curl -X PUT http://localhost:3000/tasks/<id> \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
```

**Delete a task**
```bash
curl -X DELETE http://localhost:3000/tasks/<id>
```

## Task schema

```json
{
  "id": "integer (auto-incrementing, starts at 1)",
  "title": "string (required)",
  "description": "string",
  "done": "boolean",
  "createdAt": "ISO date-time",
  "updatedAt": "ISO date-time"
}
```

