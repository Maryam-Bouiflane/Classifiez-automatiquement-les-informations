def test_employee_not_found(client):
    response = client.get("/employee/999999999")

    assert response.status_code == 404