from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200

def test_create_product():
    response = client.post(
        "/products",
        json={
            "name": "Wireless Mouse",
            "price": 29.99,
            "stock": 50
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Wireless Mouse"

def test_list_products():
    response = client.get("/products")

    assert response.status_code == 200

def test_get_nonexistent_product():
    response = client.get("/products/99999")

    assert response.status_code == 404

def test_invalid_product_price():
    response = client.post(
        "/products",
        json={
            "name": "Wireless Mouse",
            "price": -10,
            "stock": 50
        }
    )

    assert response.status_code == 422
