"""
Supabase client setup for the Auth API.

Handles the connection to Supabase, which acts as our Identity
Provider (IdP) — it manages user accounts and issues/verifies JWTs
for us. This is the only file that should initialize the Supabase
client; main.py and any route/dependency files import get_supabase()
from here rather than creating their own client instances.
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]


def get_supabase() -> Client:
    """
    Return a Supabase client configured with this project's URL and
    anon key. Called fresh wherever it's needed (routes, dependencies)
    rather than shared as a global — the client itself is lightweight,
    and this avoids any surprises around shared state between requests.
    """
    return create_client(SUPABASE_URL, SUPABASE_KEY)