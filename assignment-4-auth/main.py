"""
Auth API — handles signup, login, logout, and route protection
using Supabase as the Identity Provider (IdP).
"""
from fastapi import FastAPI
from database_configA4 import get_supabase

app = FastAPI(title="Auth API")


@app.on_event("startup")
def startup_event():
    get_supabase()
    print("Server running and connected to Supabase")