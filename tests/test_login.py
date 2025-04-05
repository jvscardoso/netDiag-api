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

def test_list_users_success():
    response = requests.get(f"{BASE_URL}/users", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_users_unauthorized():
    response = requests.get(f"{BASE_URL}/users") 
    assert response.status_code == 401

def test_create_user_success():
    unique_email = f"testeuser_{uuid.uuid4().hex[:6]}@netdiag.io"
    payload = {
        "name": "Usuário Teste",
        "email": unique_email,
        "password": "testepass",
        "role": "user"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=payload, headers=headers)
    print("Create user response:", response.status_code, response.json())
    assert response.status_code == 201

def test_create_user_duplicate_email():
    payload = {
        "name": "Usuário Teste",
        "email": "testeuser@netdiag.io",
        "password": "testepass",
        "role": "user"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=payload, headers=headers)
    assert response.status_code == 400
    assert "error" in response.json()

def test_update_user_success():
    unique_email = f"testupdate_{uuid.uuid4().hex[:6]}@netdiag.io"
    create_payload = {
        "name": "Usuário Original",
        "email": unique_email,
        "password": "testpass123",
        "role": "user"
    }
    create_response = requests.post(f"{BASE_URL}/auth/register", json=create_payload, headers=headers)
    assert create_response.status_code == 201

    list_response = requests.get(f"{BASE_URL}/users", headers=headers)
    assert list_response.status_code == 200
    users = list_response.json()
    created_user = next((u for u in users if u["email"] == unique_email), None)
    assert created_user is not None
    user_id = created_user["id"]

    update_payload = {"name": "Usuário Atualizado"}
    response = requests.patch(f"{BASE_URL}/users/{user_id}", json=update_payload, headers=headers)
    assert response.status_code == 200
    assert "message" in response.json()


def test_update_user_unauthorized():
    payload = {"name": "Tentativa não autorizada"}
    response = requests.patch(f"{BASE_URL}/users/2", json=payload)
    assert response.status_code == 401

def test_delete_user_success():
    response = requests.delete(f"{BASE_URL}/users/2", headers=headers)
    assert response.status_code == 200
    assert "message" in response.json()

def test_delete_user_forbidden():
    payload = {
        "email": "testeuser@netdiag.io",
        "password": "testepass"
    }
    login = requests.post(f"{BASE_URL}/auth/login", json=payload)
    token = login.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {token}"}

    response = requests.delete(f"{BASE_URL}/users/1", headers=user_headers)
    assert response.status_code == 403
