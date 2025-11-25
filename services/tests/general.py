from typing import Any
from gateway.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwQ0JDNjg4Qy0yMTg0LTQ0QTktOTM1Ni03RTcxRTMwQjBBRUIiLCJleHAiOjE4NTMzNDk1NjJ9.7OHwy1KWxJd8PdYYAgAor3ARyE_A9lYZcFNcfrIUfYE"
}

url_base = "/api/v1"

def request_base(url: str, data: dict[str, Any]):
    return client.post(url, json=data, headers=headers)
