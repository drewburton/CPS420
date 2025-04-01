import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import httpx
import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated # Use Annotated for Python 3.9+ clarity

# JWT / Security imports
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets # For generating secret key if needed

# Pydantic models for data validation
from pydantic import BaseModel

# --- Configuration ---
# Secret key to sign JWT tokens. KEEP THIS SECRET in production!
# Generate using: openssl rand -hex 32
SECRET_KEY = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# App 2 connection details (same as before)
APP2_HOST = os.getenv("APP2_HOST", "localhost")
APP2_PORT = 14124
APP2_DATA_ENDPOINT = f"http://{APP2_HOST}:{APP2_PORT}/provide-data"
# --- ---

# --- Pydantic Models ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# User model (as stored in DB - includes hashed password)
class UserInDB(BaseModel):
    username: str
    hashed_password: str
    disabled: Optional[bool] = None

# User model (returned by API - excludes password)
class User(BaseModel):
    username: str
    disabled: Optional[bool] = None
# --- ---

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
# --- ---

# --- Simulated User Database ---
# In a real app, this would be a database query.
# Generate hash for 'testpass':
# python -c 'from passlib.context import CryptContext; pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto"); print(pwd_context.hash("testpass"))'
# Replace the hashed_password below with the generated hash
fake_users_db = {
    "testuser": {
        "username": "testuser",
        # Replace with your generated hash: e.g., "$2b$12$Eixza..."
        "hashed_password": "$2b$12$axQPJ7gGflDp5Rjw9yhCpehFuwKz4DHjAe/jFUDMA.XsfdXa.314y", # Example Hash for 'testpass'
        "disabled": False,
    }
}

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None
# --- ---

# --- Authentication Functions ---
# Authenticate based on username/password (used by /token endpoint)
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user or user.disabled:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Create JWT access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Default expiry time if not provided
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
# --- ---

# --- OAuth2 Setup ---
# tokenUrl points to the relative path of the token endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get current user from token
async def get_current_active_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") # 'sub' is standard claim for subject (username)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        # If token is invalid or expired
        raise credentials_exception

    # Get user from our 'DB'
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    # Return the User model (without password)
    return User(username=user.username, disabled=user.disabled)
# --- ---


# --- FastAPI App Instance ---
app = FastAPI(title="App 1 - Caller (OAuth2)")
# --- ---

# --- Endpoints ---
@app.get("/")
async def read_root_app1():
    """Provides basic info about App 1."""
    return {"message": "Hello from App 1. Use /token to login, then /call-app2 or /users/me."}

# Token endpoint (OAuth2 Password Flow)
@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """Handles user login and issues JWT access token."""
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Create token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Example protected endpoint to check current user
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """Returns details of the currently authenticated user."""
    return current_user

# Protected endpoint that calls App 2
@app.get("/call-app2")
async def call_app2_endpoint(
    # Inject dependency to ensure user is authenticated via token
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Calls App 2's /provide-data endpoint and returns the result.
    Requires OAuth2 Bearer token authentication.
    """
    print(f"Authenticated user '{current_user.username}' requesting to call App 2.")
    print(f"App 1 attempting to call App 2 at: {APP2_DATA_ENDPOINT}")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(APP2_DATA_ENDPOINT)
            response.raise_for_status()
            data_from_app2 = response.json()
            print(f"App 1 received data from App 2: {data_from_app2}")
            return {
                "message": f"Successfully fetched data from App 2 (requested by {current_user.username})",
                "data_received": data_from_app2
            }
    # ... (Error handling remains the same as previous example) ...
    except httpx.ConnectError as e:
        print(f"Error connecting to App 2: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to App 2 at {APP2_DATA_ENDPOINT}. Is it running and accessible?"
        )
    except httpx.TimeoutException as e:
        print(f"Timeout connecting to App 2: {e}")
        raise HTTPException(
            status_code=504,
            detail=f"Request to App 2 at {APP2_DATA_ENDPOINT} timed out."
        )
    except httpx.HTTPStatusError as e:
        print(f"App 2 returned an error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"App 2 returned an error: {e.response.text}"
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred while trying to reach App 2: {str(e)}"
        )

# --- ---

if __name__ == "__main__":
    print("Starting App 1 (OAuth2) on http://0.0.0.0:8000")
    print("⚠️ Ensure you have generated a password hash for 'testpass' and updated fake_users_db.")
    print(f"⚠️ Using SECRET_KEY: {SECRET_KEY[:4]}...{SECRET_KEY[-4:]}. Use environment variables for production.")
    uvicorn.run("app1:app", host="0.0.0.0", port=8000, reload=True)