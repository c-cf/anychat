from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
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

async def register_user(data: dict):
    # Simulate registration: normally, save to DB.
    # For now, return the data as user.
    return {"id": "2", "username": data["username"], "email": data["email"]}

async def login_user(data: dict):
    # Simulate login: if username == "testuser" and password=="password" then return jwt tokens.
    if data.get("username") != "testuser" or data.get("password") != "password":
         raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=15)
    access_token = jwt.encode({"sub": data["username"], "exp": datetime.utcnow() + access_token_expires}, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    refresh_token_str = "dummy_refresh_token"
    return {"access_token": access_token, "refresh_token": refresh_token_str}

async def refresh_token(refresh_token: str):
    # Simulate refresh: check dummy token
    if refresh_token != "dummy_refresh_token":
         raise HTTPException(status_code=400, detail="Invalid refresh token")
    access_token_expires = timedelta(minutes=15)
    access_token = jwt.encode({"sub": "testuser", "exp": datetime.utcnow() + access_token_expires}, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return access_token

async def request_password_reset(email: str):
    # Simulate generating a reset token.
    return "dummy_reset_token"

async def reset_password(reset_token: str, new_password: str):
    if reset_token != "dummy_reset_token":
         raise HTTPException(status_code=400, detail="Invalid reset token")
    # Simulate updating password.
    return

async def verify_email_token(token: str):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid token")
        
        # 更新資料庫中的 is_verified 欄位
        await db.execute(
            "UPDATE users SET is_verified = 1 WHERE id = :user_id",
            {"user_id": user_id}
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

async def google_oauth_login():
    # Simulate google oauth login.
    return {"access_token": "google_dummy_access_token", "refresh_token": "google_dummy_refresh_token"}

async def setup_mfa(current_user):
    # Simulate MFA secret generation
    return "dummy_mfa_secret"

async def verify_mfa(current_user, code: str):
    # Simulate TOTP verification; in real code, check with pyotp.TOTP(current_user.mfa_secret)
    return code == "123456"

# 新增方法：生成驗證 Token
async def generate_email_verification_token(user_id: str) -> str:
    expiration = datetime.utcnow() + timedelta(hours=24)  # Token 有效期 24 小時
    payload = {"sub": user_id, "exp": expiration}
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return token
