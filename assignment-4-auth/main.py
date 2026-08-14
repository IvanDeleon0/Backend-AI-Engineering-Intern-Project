"""
Auth API — handles signup, login, logout, and route protection
using Supabase as the Identity Provider (IdP).
"""
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Header, Depends, Response
from database_configA4 import get_supabase, get_supabase_admin
from pydantic import BaseModel
from supabase_auth.errors import AuthApiError

class AuthRequest(BaseModel):
    email: str
    password: str
app = FastAPI(title="Auth API")

def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Access token required")

    token = authorization.removeprefix("Bearer ")
    #return {"message": "Token received", "token_preview": token[:10] + "..."}
    supabase = get_supabase()

    try:
        response = supabase.auth.get_user(token)
    except AuthApiError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return response.user
    

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

@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}

@app.get("/protected/profile")
def get_protected_profile(user=Depends(get_current_user)):
    return{
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at.isoformat(),
    }

@app.post("/auth/logout")
def logout(authorization: str = Header(None), user = Depends(get_current_user)):
    token = authorization.removeprefix("Bearer ")

    supabase_admin = get_supabase_admin()
    supabase_admin.auth.admin.sign_out(token)

    return Response(status_code=204)

@app.get("/protected/dashboard")
def protected_dashboard(user = Depends(get_current_user)):
    return {"message": f"Welcome to your dashboard, {user.email}"}