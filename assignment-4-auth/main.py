"""
Auth API — handles signup, login, logout, and route protection
using Supabase as the Identity Provider (IdP).
"""
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from database_configA4 import get_supabase
from pydantic import BaseModel
from supabase_auth.errors import AuthApiError

class AuthRequest(BaseModel):
    email: str
    password: str
app = FastAPI(title="Auth API")


@app.on_event("startup")
def startup_event():
    get_supabase()
    print("Server running and connected to Supabase")

@app.post("/auth/signup")
def signup(auth: AuthRequest):
    if not auth.email or not auth.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    supabase = get_supabase()
    try:
        response = supabase.auth.sign_up({
            "email": auth.email,
            "password": auth.password,
        })
    except AuthApiError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return JSONResponse(status_code=201, content={"user": response.user.model_dump(mode="json")})

@app.post("/auth/login")
def login(auth: AuthRequest):
    if not auth.email or not auth.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    supabase = get_supabase()
    try:
        response = supabase.auth.sign_in_with_password({
            "email": auth.email,
            "password": auth.password,
        })
    except AuthApiError:
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
    }