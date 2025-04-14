# import pytest
# from httpx import AsyncClient
# from httpx import ASGITransport
# from app.main import app

# @pytest.mark.asyncio
# async def test_list_documents():
#     token = await login_and_get_token()
#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url="http://test") as client:
#         res = await client.get("/api/summary/list", headers={
#             "Authorization": f"Bearer {token}"
#         })
#         assert res.status_code in [200, 404]


# @pytest.mark.asyncio
# async def test_fetch_summary():
#     token = await login_and_get_token()
#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url="http://test") as client:
#         res = await client.get("/api/summary/Bain_0", headers={
#             "Authorization": f"Bearer {token}"
#         })
#         assert res.status_code in [200, 404]


# async def login_and_get_token():
#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url="http://test") as client:
#         res = await client.post("/api/auth/login", json={
#             "email": "testuser@example.com",
#             "password": "test123"
#         })
#         if res.status_code != 200:
#             await client.post("/api/auth/register", json={
#                 "email": "testuser@example.com",
#                 "password": "test123",
#                 "role": "user",
#                 "tenant": "Bain"
#             })
#             res = await client.post("/api/auth/login", json={
#                 "email": "testuser@example.com",
#                 "password": "test123"
#             })

#         return res.json()["access_token"]
