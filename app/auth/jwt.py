from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.config import settings
from app.models.schemas import TokenData

def create_token(data: dict, expires_in: int = settings.JWT_EXPIRES_IN) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=expires_in)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")

def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return TokenData(**payload)
    except JWTError:
        raise ValueError("Invalid or expired token")
