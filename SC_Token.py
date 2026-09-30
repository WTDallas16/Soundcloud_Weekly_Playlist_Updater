import os, sys, requests
from dotenv import load_dotenv

load_dotenv("secrets.env")

TOKEN_URL = "https://secure.soundcloud.com/oauth/token"
CLIENT_ID = os.environ["SC_CLIENT_ID"]
CLIENT_SECRET = os.environ["SC_CLIENT_SECRET"]

if len(sys.argv) != 3:
    print("Usage: python SC_Token.py <code> <code_verifier>")
    sys.exit(1)

code, code_verifier = sys.argv[1], sys.argv[2]

resp = requests.post(
    TOKEN_URL,
    data={
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": "http://127.0.0.1:8000/auth-callback",
        "code": code,
        "code_verifier": code_verifier,
    },
    timeout=30,
)
resp.raise_for_status()
tok = resp.json()
print(tok)  # access_token, refresh_token, expires_in, token_type=bearer
