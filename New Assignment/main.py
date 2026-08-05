from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sqlite3
from datetime import datetime, timezone

app = FastAPI(title="Task CRUD API")   


@app.get("/")
def gets():
    return {"name" : "Task API",
            "version" : "1.0",
            "endpoints" : ["/tasks"]
            }
@app.get("/health")
def health_status():
    return {"status" : "ok"}