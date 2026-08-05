from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sqlite3
from datetime import datetime, timezone

app = FastAPI(title="Task CRUD API")   

tasks = [{"id" : 1, "title": "Task 1", "done" : False},
         {"id" : 2, "title": "Task 2", "done" : True},
         {"id" : 3, "title": "Task 3", "done" : False}]

#This class is used to validate the data sent in the request body when creating or updating a task.
class Task(BaseModel):
    title: str
    done: Optional[bool] = False

@app.get("/")
def root():
    return {"name" : "Task API",
            "version" : "1.0",
            "endpoints" : ["/tasks"]
            }
@app.get("/health")
def health_status():
    return {"status" : "ok"}

#this endpoint returns all the tasks in the list
@app.get("/tasks")
def display_tasks():
    """ Returns all the list of tasks """
    return tasks


# GET method is used to retrieve a resource, in this case a task.
@app.get("/tasks/{id}")
def get_task_by_ID(id:int):
    """ Returns a task by its ID """
    for task in tasks:
        if task["id"] == id:
            return task
    raise HTTPException(status_code=404, detail={"error" : f"Task {id} not found"})


# POST method is used to create a new resource, in this case a task.
@app.post("/tasks", status_code=201)
def add_task(task: Task):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400,
                             detail="Task title cannot be empty")
    """Create a new task and add it to the list of tasks"""
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": task.done
    }
    tasks.append(new_task)
    return new_task


#PUT method is used to update a resource, in this case a task.
@app.put("/tasks/{id}")
def update_task(id: int, task: Task):
    """Update a task by its ID"""
    for t in tasks:
        if t["id"] == id:
            if not task.title or not task.title.strip():
                raise HTTPException(status_code=400,
                                    detail="Task title is invalid or empty")
            t["title"] = task.title
            t["done"] = task.done
            return t
    raise HTTPException(status_code=404, detail={"error" : f"Task {id} not found"})


# status_code=204 means no content or confirmation sent back to the client 
# but its a successful operation

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    """Delete a task by its ID"""
    for t in tasks:
        if t["id"] == id:
            tasks.remove(t)
            return
    raise HTTPException(
        status_code=404, 
        detail={"error" : f"Task {id} not found"})