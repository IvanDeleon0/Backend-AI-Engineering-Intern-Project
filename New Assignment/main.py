from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sqlite3
from datetime import datetime, timezone

app = FastAPI(title="Task CRUD API")   

tasks = [{"id" : 1, "title": "Task 1", "done" : False},
         {"id" : 2, "title": "Task 2", "done" : True},
         {"id" : 3, "title": "Task 3", "done" : False}]

@app.get("/")
def root():
    return {"name" : "Task API",
            "version" : "1.0",
            "endpoints" : ["/tasks"]
            }
@app.get("/health")
def health_status():
    return {"status" : "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{id}")
def get_task(id:int):
    for task in tasks:
        if task["id"] == id:
            return task
    raise HTTPException(status_code=404, detail={"error" : f"Task {id} not found"})