
def test_create_doctor(client, auth_headers):
    response = client.post(
        "/doctors",
        headers=auth_headers,
        json={
            "first_name": "David",
            "last_name": "Miller",
            "specialty": "Cardiology",
            "contact_number": "9876543210"
        }
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Doctor registered successfully"


def test_get_doctors(client, auth_headers):
    response = client.get("/doctors", headers=auth_headers)

    assert response.status_code == 200
    assert "doctors" in response.json()


def test_get_doctor_by_id(client, auth_headers):
    create_response = client.post(
        "/doctors",
        headers=auth_headers,
        json={
            "first_name": "John",
            "last_name": "Smith",
            "specialty": "Neurology",
            "contact_number": "9876543211"
        }
    )

    doctor_id = create_response.json()["doctor"]["doctor_id"]

    response = client.get(
        f"/doctors/{doctor_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["doctor_id"] == doctor_id


def test_update_doctor(client, auth_headers):
    create_response = client.post(
        "/doctors",
        headers=auth_headers,
        json={
            "first_name": "Robert",
            "last_name": "Brown",
            "specialty": "Dermatology",
            "contact_number": "9876543212"
        }
    )

    doctor_id = create_response.json()["doctor"]["doctor_id"]

    response = client.put(
        f"/doctors/{doctor_id}",
        headers=auth_headers,
        json={
            "first_name": "Robert",
            "last_name": "Brown",
            "specialty": "Pediatrics",
            "contact_number": "9876543212"
        }
    )

    assert response.status_code == 200
    assert response.json()["doctor"]["specialty"] == "Pediatrics"


def test_delete_doctor(client, auth_headers):
    create_response = client.post(
        "/doctors",
        headers=auth_headers,
        json={
            "first_name": "Alex",
            "last_name": "Taylor",
            "specialty": "Orthopedics",
            "contact_number": "9876543213"
        }
    )

    doctor_id = create_response.json()["doctor"]["doctor_id"]

    response = client.delete(
        f"/doctors/{doctor_id}",
        headers=auth_headers
    )

    assert response.status_code == 200


def test_doctor_not_found(client, auth_headers):
    response = client.get(
        "/doctors/999999",
        headers=auth_headers
    )

    assert response.status_code == 404


def test_doctor_access_without_token(client):
    response = client.get("/doctors")

    assert response.status_code == 401
