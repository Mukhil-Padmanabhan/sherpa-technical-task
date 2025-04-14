from fastapi import APIRouter, Request, HTTPException, Depends
from typing import List
from app.models.schemas import DocumentSummary, DocumentListItem
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.get("/list", response_model=List[DocumentListItem])
def list_documents(request: Request, user=Depends(get_current_user)):
    """
    Return all documents for the user's tenant.
    Admins receive all tenant documents.
    """
    tenant_docs = request.app.state.documents
    user_role = user.get("role")
    user_tenant = user.get("tenant")

    if not tenant_docs:
        raise HTTPException(status_code=500, detail="📂 Document store is not initialized.")

    docs = []

    if user_role == "admin":
        for tenant, doc_list in tenant_docs.items():
            if tenant != "all":
                docs.extend(doc_list)
    else:
        if user_tenant not in tenant_docs:
            raise HTTPException(status_code=404, detail="Tenant not found.")
        docs = tenant_docs[user_tenant]

    return [
        DocumentListItem(
            doc_id=doc.id,
            doc_name=doc.file_name
        ) for doc in docs
    ]

@router.get("/{doc_id}", response_model=DocumentSummary, tags=["Summarization"])
def get_summary(
    doc_id: str,
    request: Request,
    user=Depends(get_current_user)
):
    """
    Retrieve a document summary using global doc_id format like 'Bain_0'.
    RBAC enforced.
    """
    try:
        tenant, index = doc_id.split("_")
        index = int(index)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid doc_id format. Expected 'Tenant_Index'.")

    user_role = user.get("role")
    user_tenant = user.get("tenant")

    if user_role != "admin" and tenant != user_tenant:
        raise HTTPException(status_code=403, detail="Access denied for this tenant")

    docs_map = request.app.state.documents
    if tenant not in docs_map:
        raise HTTPException(status_code=404, detail="Tenant not found")

    docs = docs_map[tenant]
    if index < 0 or index >= len(docs):
        raise HTTPException(status_code=404, detail="Invalid document ID")

    doc = docs[index]
    return DocumentSummary(
        doc_id=doc.id,
        doc_name=doc.file_name,
        summary=doc.summary
    )