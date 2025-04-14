# Sherpa

An end-to-end AI-powered document search and summarization platform built with FastAPI, React, ChromaDB, and OpenAI embeddings.

## Overview

Sherpa is a multi-tenant AI-powered document search and summarization app tailored for consulting firms. It allows users to securely upload, summarize, and query business documents using LLMs and vector search across tenant-specific or global contexts.

## Features
**Backend**
- **User Authentication**: JWT-based login and registration
- **Document Summarization**: Generate summaries for uploaded documents
- **RAG (Retrieval-Augmented Generation)**: Answer questions based on document content
- **Embedding Caching**: Utilize ChromaDB to cache embeddings and avoid redundant computations

**Frontend**
- **Search Interface**: Input questions and display answers with sources
- **Document List**: View and summarize uploaded documents
- **Authentication**: Login and registration forms
- **Role-Based Access**: Adjust tenant selection based on user role


## Tech Stack
- FastAPI (Python)
- MongoDB (via Motor)
- JWT Authentication
- ChromaDB
- Azure OpenAI or Hugging Face
- Pydantic
- DuckDuckGo Search API (fallback)
- React/Vite

### DevOps
- Docker & Docker Compose for containerization
- MongoDB for data persistence

## Getting Started

### Prerequisites
- Docker and Docker Compose (for containerized deployment)

### Clone repo
```
git clone https://github.com/Charter-AI/sherpa-technical-task.git
cd sherpa-technical-task
```

### Running the application

1. **Using Docker Compose**
   ```
   docker compose up --build
   ```
   
   This will build and start the MongoDB database, FastAPI, ChromaDB and frontend container.

2. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## API Documentation

Access the automatically generated API docs at:
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

### Main Endpoints

- **Authentication**
  - POST `/api/auth/register` - Register a new user
  - POST `/api/auth/login` - Login a user

- **Summarization**
  - GET `/api/summary/list` - Get all documents
  - GET `/api/summary/{doc_id}` - Get document summary

- **RAG**
  - POST `/api/rag/ask` - rag ask
  - POST `/api/rag/doc-search` - Search within document

- **Default**
    - GET `/` - Health check

## Future Improvements
- Refresh Tokens with Rotation & Revocation Lists
- Multi-Factor Authentication (MFA)
- IP Whitelisting
- Per-Chunk Embedding Versioning & Expiry
- Chunk Metadata Tagging
- RAG Pipelines with LangGraph
- Hallucination Grading & Filtering
- Feedback Loop Storage
- Multiple Model Support
- Multilingual Support 
- Prometheus + Grafana Dashboards
- Centralized Logging (ELK or Loki)
- Retry Queues for Indexing Failures
- Redis Caching
- Unit + Integration Tests
- End-to-End Testing with Cypress
- Chat History & Prompt Management

## License

MIT

## Author
Mukhil Padmanabhan
