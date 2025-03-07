from fastapi import APIRouter, HTTPException, Depends
from services.permission_service import PermissionService
from services.auth_service import (
    get_current_user,
    register_user,
    login_user,
    refresh_token,
    request_password_reset,
    reset_password,
    verify_email_token,
    google_oauth_login,
    setup_mfa,
    verify_mfa
)

router = APIRouter()

@router.post("/roles/{user_id}")
async def assign_role(
    user_id: str,
    role: str,
    permission_service: PermissionService = Depends(),
    current_user = Depends(get_current_user)
):
    try:
        if not permission_service.check_permission(current_user.id, "assign_role"):
            raise HTTPException(status_code=403, detail="Permission denied")
        permission_service.assign_role(user_id, role)
        return {"message": "Role assigned successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/roles")
async def add_role(
    role: str,
    permissions: list[str],
    permission_service: PermissionService = Depends(),
    current_user = Depends(get_current_user)
):
    try:
        if not permission_service.check_permission(current_user.id, "add_role"):
            raise HTTPException(status_code=403, detail="Permission denied")
        permission_service.add_role(role, permissions)
        return {"message": "Role added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register")
async def register(data: dict):
    user = await register_user(data)
    return user

@router.post("/login")
async def login(data: dict):
    result = await login_user(data)
    return result

@router.post("/token/refresh")
async def token_refresh(data: dict):
    new_access_token = await refresh_token(data["refresh_token"])
    return {"access_token": new_access_token}

@router.post("/password-reset-request")
async def password_reset_request(data: dict):
    reset_token = await request_password_reset(data["email"])
    return {"reset_token": reset_token}

@router.post("/password-reset")
async def password_reset(data: dict):
    await reset_password(data["reset_token"], data["new_password"])
    return {"message": "Password reset successfully"}

@router.get("/verify-email")
async def verify_email(token: str):
    await verify_email_token(token)
    return {"message": "Email verified"}

@router.get("/login/google")
async def login_google():
    result = await google_oauth_login()
    return result

@router.post("/mfa/setup")
async def mfa_setup(current_user=Depends(get_current_user)):
    mfa_secret = await setup_mfa(current_user)
    return {"mfa_secret": mfa_secret}

@router.post("/mfa/verify")
async def mfa_verify(data: dict, current_user=Depends(get_current_user)):
    valid = await verify_mfa(current_user, data["code"])
    if not valid:
        raise HTTPException(status_code=400, detail="Invalid MFA code")
    return {"message": "MFA verified successfully"}
