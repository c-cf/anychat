from fastapi import APIRouter, HTTPException, Depends
from services.permission_service import PermissionService
from services.auth_service import get_current_user

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