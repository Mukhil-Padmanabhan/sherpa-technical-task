from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from app.config import settings
from app.routers import summary, rag, auth
from app.services.tenant_loader import initialize_all_tenants
from app.middleware.logging import LoggingMiddleware
import threading
from pymongo.errors import ServerSelectionTimeoutError


limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="Sherpa RAG API",
    description="Summarize and search consulting PDFs securely across multiple tenants.",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(HTTP_429_TOO_MANY_REQUESTS, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("Starting up backend services...")
    app.state.mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
    app.state.mongo_db = app.state.mongo_client[settings.MONGO_DB]
    print("Mongo connected")
    threading.Thread(target=load_tenants_async, args=(app,), daemon=True).start()

def load_tenants_async(app):
    tenant_docs, tenant_indexers = initialize_all_tenants()
    app.state.documents = tenant_docs
    app.state.indexers = tenant_indexers
    print("Tenants loaded in background")

@app.on_event("shutdown")
async def shutdown_event():
    app.state.mongo_client.close()

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(summary.router, prefix="/api/summary", tags=["Summarization"])
app.include_router(rag.router, prefix="/api/rag", tags=["RAG"])

@app.middleware("http")
async def log_requests(request: Request, call_next):
    from app.utils.logger import logger
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code} for {request.url}")
    return response

@app.get("/")
@limiter.limit("10/minute")
def root(request: Request):
    return {"status": "Sherpa RAG backend is running."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
