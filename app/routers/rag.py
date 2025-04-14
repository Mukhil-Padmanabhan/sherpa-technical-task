from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from app.services.gpt_client import GPTClient
from app.models.schemas import RAGSource, RAGResponse, DocumentRequest, RAGRequest
from app.config import settings
from app.dependencies.auth import get_current_user
from app.utils.agentic_fallback import fallback_knowledge_search
from app.utils.logger import logger

router = APIRouter()

@router.post("/ask", response_model=RAGResponse)
def rag_ask(req: RAGRequest, request: Request, user=Depends(get_current_user)):
    user_tenant = user["tenant"]
    user_role = user["role"]
    requested_tenant = req.tenant.strip()
    question = req.question.strip()
    top_k = req.top_k
    logger.info(f"User: {user['sub']} | Role: {user['role']} | Tenant: {requested_tenant}")
    gpt = GPTClient(api_key=settings.AZURE_API_KEY, endpoint=settings.AZURE_ENDPOINT)

    #  RBAC Rules 
    if user_role == "admin":
        requested_tenant = "all"
    elif user_role == "user" and requested_tenant != user_tenant:
        raise HTTPException(status_code=403, detail="Users can only access their own tenant.")
    elif user_role == "guest" or requested_tenant == "public":
        from app.utils.agentic_fallback import duckduckgo_fallback
        fallback_context = duckduckgo_fallback(question)
        
        prompt = f"You are a public-facing AI assistant. Use this info:\n\n{fallback_context}\n\nQuestion: {question}"
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        answer = gpt.generate_answer(messages)
        return RAGResponse(answer=answer, sources=[])
    elif user_role == "guest" and requested_tenant != "public":
        raise HTTPException(status_code=403, detail="Guests can only access public data.")
    
    if requested_tenant not in ["all", "public"] and requested_tenant != user_tenant:
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": question}
        ]
        try:
            answer = gpt.generate_answer(messages)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM fallback failed: {str(e)}")
        return RAGResponse(answer=answer, sources=[])

    # Retrieve Indexed Documents 
    documents = request.app.state.documents.get(requested_tenant)
    indexer = request.app.state.indexers.get(requested_tenant)

    if not documents or not indexer:
        raise HTTPException(status_code=404, detail="Tenant not found or documents not loaded")

    try:
        result = indexer.search(requested_tenant, question, top_k=top_k)
        matches = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        if not matches:
            wiki_context = fallback_knowledge_search(question)
            context_chunks = [wiki_context]
            sources = []
        else:
            sources = []
            context_chunks = []
            for i, text in enumerate(matches):
                meta = metadatas[i]
                sources.append(RAGSource(
                    doc_id=str(meta.get("doc_id", i)),
                    doc_name=meta.get("file_name", "unknown"),
                    snippet=text[:500]
                ))
                context_chunks.append(text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chroma search failed: {str(e)}")

    # Construct RAG Prompt
    prompt = "You are a helpful AI consultant. Use the following context to answer the user's question.\n\n"
    for i, chunk in enumerate(context_chunks):
        prompt += f"Context {i+1}:\n{chunk.strip()}\n\n"
    prompt += f"User Question:\n{question.strip()}"

    try:
        messages = [
            {"role": "system", "content": "You are a helpful consultant trained on internal strategy reports."},
            {"role": "user", "content": prompt}
        ]
        answer = gpt.generate_answer(messages)
        if not isinstance(answer, str):
            raise ValueError("GPTClient should return a string")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM generation failed: {str(e)}")

    # Return Final Answer
    return RAGResponse(answer=answer, sources=sources)

@router.post("/doc-search", response_model=RAGResponse)
def search_within_document(req: DocumentRequest, request: Request, user=Depends(get_current_user)):
    try:
        tenant, index = req.doc_id.split("_")
        index = int(index)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid doc_id format. Expected 'Tenant_Index'.")

    # RBAC check
    user_tenant = user.get("tenant")
    user_role = user.get("role")

    if user_role != "admin" and tenant != user_tenant:
        raise HTTPException(status_code=403, detail="Access denied for this tenant")

    # Fetch document
    docs_map = request.app.state.documents
    if tenant not in docs_map:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    docs = docs_map[tenant]
    if index < 0 or index >= len(docs):
        raise HTTPException(status_code=404, detail="Invalid document ID")
    
    doc = docs[index]

    if req.query.lower() in doc.content.lower():
        snippet = doc.content[:500]
    else:
        snippet = "No relevant content found."

    prompt = f"Answer the following based only on this document content:\n\n{doc.content}\n\nQuestion: {req.query}"
    gpt = GPTClient(api_key=settings.AZURE_API_KEY, endpoint=settings.AZURE_ENDPOINT)

    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant answering based on a single document."},
            {"role": "user", "content": prompt}
        ]
        answer = gpt.generate_answer(messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM failed: {str(e)}")

    return RAGResponse(
        answer=answer,
        sources=[RAGSource(doc_id=doc.id, doc_name=doc.file_name, snippet=snippet)]
    )