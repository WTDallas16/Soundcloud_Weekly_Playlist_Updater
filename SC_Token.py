import os, requests
from dotenv import load_dotenv

load_dotenv("secrets.env")

TOKEN_URL = "https://secure.soundcloud.com/oauth/token"
CLIENT_ID = os.environ["SC_CLIENT_ID"]
CLIENT_SECRET = os.environ["SC_CLIENT_SECRET"]

resp = requests.post(
    TOKEN_URL,
    data={
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": "http://127.0.0.1:8000/auth-callback",
        "code": "eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiQTI1NktXIn0.1yMcoCWwpN31CyUFOxX7DjtmHYM8Nw-4GaoH_mwL6oRn7PgwLo0O7Q.8i8pi4Mo7XzpEfG_A-fjMg.VOaLz184IJXLm2GQKRBQI9yukb5sX-cn01e5RIN6XB6r7eCMZDYY7UeFaY-UAVmQR_q-nQaFzQjsjzxD9vBm8gkZcu4MHdkUVjIUTgmaPRtYXcyOoSNtrDtwknvouWTbMUiIGUBKG3g9JK3n5Q5QD4svDGJHpxlDGuSiZwIB7Z1PR_rlLqDNKe2X6Ux1y881hWxGtAHI7GO3srOSUzHcTi-27D83io1AN_kTNAHk7hxMwBWBbbYpDbOw1zqoiOU-.MYYb3T6GN4JM1dKB9ky5Yg",
        "code_verifier": "KwrXtuXUb4TPwJgKXNFulZxoWIPpXGnBZhE7hHjdwfHm00uq2PRvqA",
    },
    timeout=30,
)
# print("status:", resp.status_code)
# print("body:", resp.text)     # <- look here first for 'error' / 'error_description'
resp.raise_for_status()
tok = resp.json()
print(tok)  # access_token, refresh_token, expires_in, token_type=bearer



# # # importing os module  
# import os 
  
# # Get the list of user's 
# os.environ["SC_CLIENT_ID"] = "my client"
# os.environ["SC_CLIENT_SECRET"] = "my secret"
  
# # Print the list of user's 
# print("SC_CLIENT_ID:", os.environ["SC_CLIENT_ID"])
# print("SC_CLIENT_SECRET:", os.environ["SC_CLIENT_SECRET"])

# # importing os module  
# import os 
# import pprint 
  
# # Get the list of user's 
# env_var = os.environ 
  
# # Print the list of user's 
# print("User's Environment variable:") 
# pprint.pprint(dict(env_var), width = 1)