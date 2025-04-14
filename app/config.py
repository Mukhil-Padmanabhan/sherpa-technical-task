import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
    MONGO_DB = os.getenv("MONGO_DB", "sherpa_db")
    CHROMA_HOST = os.getenv("CHROMA_HOST", "chroma")
    CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "sherpa_docs")
    AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_GPT_MODEL = os.getenv("AZURE_GPT_MODEL", "gpt-4o-technical-task")
    AZURE_GPT_VERSION = os.getenv("AZURE_GPT_VERSION", "2024-05-01-preview")
    AZURE_EMBED_MODEL = os.getenv("AZURE_EMBED_MODEL", "text-embedding-3-small")
    AZURE_EMBED_VERSION = os.getenv("AZURE_EMBED_VERSION", "2024-02-01")
    JWT_SECRET = os.getenv("JWT_SECRET", "sherpasecret")
    JWT_ALGO: str = "HS256"
    JWT_EXPIRY = int(os.getenv("JWT_EXPIRY_MINUTES", 3600))
    FALLBACK_LLM = os.getenv("FALLBACK_LLM", "google/flan-t5-base")

settings = Settings()
