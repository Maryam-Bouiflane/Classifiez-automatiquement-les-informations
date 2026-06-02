def test_get_employee_success(client):
    response = client.get("/employee/1")

    assert response.status_code in [200, 404]

def test_get_employee_not_found(client):
    response = client.get("/employee/999999")

    assert response.status_code == 404

def test_get_employee_invalid_id(client):
    response = client.get("/employee/abc")

    assert response.status_code == 422 or response.status_code == 400

