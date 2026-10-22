


import os
import jwt
import time
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from argon2 import PasswordHasher

from src.db.queries.auth import AuthQueries
from src.exceptions import NCPlusOneHTTPException
from src.models.auth import LoginResponse

load_dotenv(".env")

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITHM = "HS256"

def create_access_token(user_id: int) -> str:
    timeout = 1800 # Token expires in 30 minutes
    payload = {
        "sub": user_id,
        "exp": time.time() + timeout
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    invalid_token_exception = NCPlusOneHTTPException(status_code=401, detail="Invalid token")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise invalid_token_exception

        return user_id
    
    except jwt.ExpiredSignatureError:
        raise NCPlusOneHTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise invalid_token_exception

@router.post("/login", response_model=LoginResponse)
async def login(request: OAuth2PasswordRequestForm = Depends()):
    ph = PasswordHasher()
    login_exception = NCPlusOneHTTPException(status_code=401, detail="Invalid username or password")
    
    user = await AuthQueries.get_user_by_email(request.username)
        
    if not user:
        raise login_exception
    
    try:
        ph.verify(user["password"], request.password)
    except Exception:
        raise login_exception

    access_token = create_access_token(user["id"])
    return {"access_token": access_token, "token_type": "bearer"}
