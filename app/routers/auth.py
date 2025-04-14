from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.dependencies.database import get_db
from app.utils.jwt import create_access_token, verify_password, hash_password
from app.config import settings

router = APIRouter()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    tenant: str
    role: str = "user"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
async def register_user(user: RegisterRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=409, detail="User already exists.")

    hashed = hash_password(user.password)
    user_dict = {
        "email": user.email,
        "hashed_password": hashed,
        "tenant": user.tenant,
        "role": user.role
    }
    await db.users.insert_one(user_dict)
    return {"message": "User registered successfully."}

@router.post("/login")
async def login_user(user: LoginRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    token_data = {
        "sub": db_user["email"],
        "tenant": db_user["tenant"],
        "role": db_user["role"]
    }
    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}
