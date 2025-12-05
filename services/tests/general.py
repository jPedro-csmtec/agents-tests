from typing import Any
from gateway.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwQ0JDNjg4Qy0yMTg0LTQ0QTktOTM1Ni03RTcxRTMwQjBBRUIiLCJleHAiOjE4NTMzNDk1NjJ9.7OHwy1KWxJd8PdYYAgAor3ARyE_A9lYZcFNcfrIUfYE"
}

def request_base(url: str, input: dict[str, Any]):
    return client.post(f"/api/v1/{url}", json=input, headers=headers)

def get_return_data(response: Any):
    return response.json()["data"]["result"].lower()
