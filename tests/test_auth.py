# import pytest
# from httpx import AsyncClient
# from httpx import ASGITransport
# from app.main import app

# @pytest.mark.asyncio
# async def test_register_user():
#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url="http://test") as client:
#         res = await client.post("/api/auth/register", json={
#             "email": "testuser@example.com",
#             "password": "test123",
#             "role": "user",
#             "tenant": "Bain"
#         })
#         assert res.status_code in [200, 201]


# @pytest.mark.asyncio
# async def test_login_user():
#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url="http://test") as client:
#         res = await client.post("/api/auth/login", json={
#             "email": "testuser@example.com",
#             "password": "test123"
#         })
#         assert res.status_code == 200
#         assert "access_token" in res.json()
