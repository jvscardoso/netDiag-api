import requests
import uuid

BASE_URL = "http://localhost:5000"

def get_admin_token():
    payload = {
        "email": "admin@netdiag.io",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    return response.json()["access_token"]

headers = {"Authorization": f"Bearer {get_admin_token()}"}

def test_get_diagnostics_basic_pagination():
    params = {"page": 1, "limit": 5}
    response = requests.get(f"{BASE_URL}/diagnostics", params=params, headers=headers)
    assert response.status_code == 200
    diagnostics = response.json()
    assert isinstance(diagnostics, list)
    assert len(diagnostics) <= 5


def test_get_diagnostics_with_filters():
    params = {
        "page": 1,
        "limit": 10,
        "city": "São Paulo",
        "state": "SP"
    }
    response = requests.get(f"{BASE_URL}/diagnostics", params=params, headers=headers)
    assert response.status_code == 200
    diagnostics = response.json()
    assert all(d["city"] == "São Paulo" and d["state"] == "SP" for d in diagnostics)

def test_get_diagnostics_aggregated_without_filters():
    response = requests.get(f"{BASE_URL}/diagnostics/grouped", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
    if data:
        row = data[0]
        assert "day" in row
        assert "avg_latency" in row
        assert "avg_packet_loss" in row
        assert "avg_quality_of_service" in row
        assert "total" in row


def test_get_diagnostics_aggregated_with_filters():
    response = requests.get(f"{BASE_URL}/diagnostics/grouped?state=SP", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    if data:
        row = data[0]
        assert "day" in row
        assert "avg_latency" in row
        assert "avg_packet_loss" in row
        assert "avg_quality_of_service" in row
        assert "total" in row

def test_get_diagnostics_aggregated_with_multiple_filters():
    params = {
        "state": "BA",
        "city": "Feira de Santana"
    }
    response = requests.get(f"{BASE_URL}/diagnostics/grouped", params=params, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        row = data[0]
        assert "day" in row
        assert "avg_latency" in row
        assert "avg_packet_loss" in row
        assert "avg_quality_of_service" in row
        assert "total" in row


def test_get_diagnostics_aggregated_with_invalid_filter_key():
    params = {
        "nonexistent": "value"
    }
    response = requests.get(f"{BASE_URL}/diagnostics/grouped", params=params, headers=headers)
    assert response.status_code == 400

    data = response.json()
    assert "error" in data
    assert data["error"] == "Filtro inválido: nonexistent"


def test_get_diagnostics_aggregated_with_invalid_filter_value():
    params = {
        "state": "UX" 
    }
    response = requests.get(f"{BASE_URL}/diagnostics/grouped", params=params, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0 
