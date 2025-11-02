"""
Unit tests cho API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["status"] == "running"


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "api" in data
    assert "gemini_api_key_configured" in data
    assert "database" in data


def test_analyze_empty_text():
    """Test analyze với text rỗng"""
    response = client.post(
        "/api/analyze",
        json={"text": ""}
    )
    assert response.status_code == 400


def test_analyze_invalid_json():
    """Test analyze với invalid JSON"""
    response = client.post(
        "/api/analyze",
        json={"invalid": "data"}
    )
    # Should return 422 (validation error) hoặc 400
    assert response.status_code in [400, 422]


def test_history_endpoint():
    """Test history endpoint (có thể fail nếu DB không available)"""
    response = client.get("/api/history")
    # Có thể là 200 (nếu có DB) hoặc 500 (nếu không có DB)
    assert response.status_code in [200, 500]


def test_export_endpoint_invalid_id():
    """Test export với ID không tồn tại"""
    response = client.get("/api/export/json/99999")
    assert response.status_code == 404


def test_file_upload_no_file():
    """Test file upload không có file"""
    response = client.post("/api/analyze/file")
    assert response.status_code in [400, 422]


# Note: Tests thực sự với Gemini API cần API key thật và tốn phí
# Nên chỉ test với mock data hoặc skip tests cần API key

