from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from services.document_service import DocumentService
from services.auth_service import get_current_user
from services.permission_service import PermissionService

router = APIRouter()

@router.post("/documents")
async def add_document(
    content: str,
    metadata: Dict,
    document_service: DocumentService = Depends(),
    permission_service: PermissionService = Depends(),
    current_user = Depends(get_current_user)
):
    try:
        if not permission_service.check_permission(current_user.id, "add_document"):
            raise HTTPException(status_code=403, detail="Permission denied")
        document_id = await document_service.add_document(content, metadata, current_user.id)
        return {"document_id": document_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/{document_id}")
async def get_document(
    document_id: str,
    document_service: DocumentService = Depends(),
    current_user = Depends(get_current_user)
):
    try:
        document = await document_service.get_document(document_id, current_user.id)
        if document is None:
            raise HTTPException(status_code=404, detail="Document not found")
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents")
async def list_documents(
    document_service: DocumentService = Depends(),
    permission_service: PermissionService = Depends(),
    current_user = Depends(get_current_user)
):
    try:
        if not permission_service.check_permission(current_user.id, "get_document"):
            raise HTTPException(status_code=403, detail="Permission denied")
        documents = await document_service.list_documents(current_user.id)
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/documents/{document_id}")
async def update_document(
    document_id: str,
    content: str,
    metadata: Dict,
    document_service: DocumentService = Depends(),
    permission_service: PermissionService = Depends(),
    current_user = Depends(get_current_user)
):
    try:
        if not permission_service.check_permission(current_user.id, "update_document"):
            raise HTTPException(status_code=403, detail="Permission denied")
        await document_service.update_document(document_id, content, metadata, current_user.id)
        return {"message": "Document updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: str,
    document_service: DocumentService = Depends(),
    permission_service: PermissionService = Depends(),
    current_user = Depends(get_current_user)
):
    try:
        if not permission_service.check_permission(current_user.id, "delete_document"):
            raise HTTPException(status_code=403, detail="Permission denied")
        await document_service.delete_document(document_id, current_user.id)
        return {"message": "Document deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
