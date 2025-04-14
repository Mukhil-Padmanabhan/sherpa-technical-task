from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class TokenData(BaseModel):
    user_id: str
    email: str
    exp: int

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Document(BaseModel):
    id: int
    tenant: str
    file_name: str
    content: str
    summary: Optional[str] = None

class RAGQuery(BaseModel):
    question: str
    tenant: str = "all"
    top_k: int = 5

class RAGSource(BaseModel):
    doc_id: str
    doc_name: str
    snippet: str

class RAGAnswer(BaseModel):
    answer: str
    sources: List[RAGSource]

class RAGResponse(BaseModel):
    answer: str
    sources: List[RAGSource]
        
class DocumentListItem(BaseModel):
    doc_id: str
    doc_name: str
    
class DocumentSummary(DocumentListItem):
    summary: Optional[str] = None
    
class RAGRequest(BaseModel):
    question: str
    tenant: str = "all"
    top_k: int = 5

class DocumentRequest(BaseModel):
    query: str
    doc_id: str