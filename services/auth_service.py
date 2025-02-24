from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from pydantic import BaseModel
from typing import Optional
from main import Config
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    id: str
    username: str
    email: str

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    # Assume you have a function get_user_by_username to fetch user from the database
    user = await get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_user_by_username(username: str) -> Optional[User]:
    # This should be the logic to fetch user from the database
    # Using mock data as an example
    if username == "testuser":
        return User(id="1", username="testuser", email="testuser@example.com")
    return None