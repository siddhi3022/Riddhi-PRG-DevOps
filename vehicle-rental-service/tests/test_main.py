from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["version"] == "v1.0.0"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "python_info" in response.text or "process_" in response.text


def test_vehicle_crud():
    payload = {"registration_no": "MH01AB1234", "make": "Toyota", "model": "Innova", "vehicle_type": "SUV", "daily_rate": 2500, "available": True}
    response = client.post("/vehicles", json=payload)
    assert response.status_code == 201
    vehicle_id = response.json()["id"]
    assert client.get(f"/vehicles/{vehicle_id}").status_code == 200
    payload["daily_rate"] = 2800
    assert client.put(f"/vehicles/{vehicle_id}", json=payload).status_code == 200
    assert client.delete(f"/vehicles/{vehicle_id}").status_code == 200


def test_customer_crud():
    payload = {"name": "Alice Smith", "email": "alice@example.com", "phone": "9876543210"}
    response = client.post("/customers", json=payload)
    assert response.status_code == 201
    customer_id = response.json()["id"]
    assert client.get(f"/customers/{customer_id}").status_code == 200
    assert client.delete(f"/customers/{customer_id}").status_code == 200


def test_booking_requires_vehicle_and_customer():
    payload = {"vehicle_id": 9999, "customer_id": 9999, "start_date": "2026-10-01", "end_date": "2026-10-03", "total_amount": 5000}
    response = client.post("/bookings", json=payload)
    assert response.status_code == 404
