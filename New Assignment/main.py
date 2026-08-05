from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sqlite3
from datetime import datetime, timezone

app = FastAPI(title="Task CRUD API")   

@app.get("/")
def hello():
    return {"message": "Hello, World!",
            "status_code": 200}