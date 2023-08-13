import jwt
import os
from dotenv import load_dotenv
from fastapi import HTTPException, Request
from jwt import DecodeError

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def verify_token(request: Request):
    """
    Function to verify the JWT token from the Authorization header of a request.
    Returns the payload if the token is valid.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")
    
    try:
        # Extract the token from the Authorization header
        token_prefix, token = auth_header.split(" ")
        if token_prefix != "Bearer":
            raise HTTPException(status_code=401, detail="Invalid Authorization Header")
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")

