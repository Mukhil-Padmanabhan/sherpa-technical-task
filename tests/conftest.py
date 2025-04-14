# import pytest
# from fastapi.testclient import TestClient
# from app.main import app
# from unittest.mock import patch
# from fastapi import Depends
# import mongomock

# @pytest.fixture(scope="module")
# def client():
#     with patch("motor.motor_asyncio.AsyncIOMotorClient") as mock_client:
#         mock_db_client = mongomock.MongoClient()
#         mock_db = mock_db_client["sherpa_test"]

#         app.state.mongo_client = mock_db_client
#         app.state.mongo_db = mock_db

#         yield TestClient(app)
