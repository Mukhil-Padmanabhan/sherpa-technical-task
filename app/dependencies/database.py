from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends, Request

async def get_db(request: Request):
    return request.app.state.mongo_db
