from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from database_config import get_connection, init_db

app = FastAPI(title="Task CRUD API")


class Task(BaseModel):
    title: str
    done: Optional[bool] = False


@app.on_event("startup")
def on_startup():
    # Creates the tasks table if missing, seeds 3 example tasks on first run
    init_db()


@app.get("/")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
def health_status():
    return {"status": "ok"}


@app.get("/tasks")
def display_tasks():
    """Returns all tasks from the database."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return [ {"id": row["id"], "title": row["title"], "done": bool(row["done"])} for row in rows ]


@app.get("/tasks/{id}")
def get_task_by_ID(id: int):
    """Returns a single task by its ID, or 404 if it doesn't exist."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (id,)).fetchone()
    conn.close()
  
    if row is None:
        raise HTTPException(status_code=404, detail={"error": f"Task {id} not found"})
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}


@app.post("/tasks", status_code=201)
def add_task(task: Task):
    """Creates a new task and inserts it into the database."""
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Task title cannot be empty")

    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title, task.done)
    )
    conn.commit()
    new_id = cursor.lastrowid  # SQLite tells us the id it just assigned
    conn.close()

    return {"id": new_id, "title": task.title, "done": task.done}


@app.put("/tasks/{id}")
def update_task(id: int, task: Task):
    """Updates a task's title and done status by its ID."""
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Task title is invalid or empty")

    conn = get_connection()
    existing = conn.execute("SELECT * FROM tasks WHERE id = ?", (id,)).fetchone()
    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail={"error": f"Task {id} not found"})

    conn.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (task.title, task.done, id)
    )
    conn.commit()
    conn.close()

    return {"id": id, "title": task.title, "done": task.done}


@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    """Deletes a task by its ID."""
    conn = get_connection()
    existing = conn.execute("SELECT * FROM tasks WHERE id = ?", (id,)).fetchone()
    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail={"error": f"Task {id} not found"})

    conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
