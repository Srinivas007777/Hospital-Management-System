
def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_create_patient(client, auth_headers):
    response = client.post(
        "/patients",
        headers=auth_headers,
        json={
            "first_name": "John",
            "last_name": "Smith",
            "age": 30,
            "gender": "Male",
            "contact_number": "9876543210"
        }
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Patient registered successfully"


def test_get_patients(client, auth_headers):
    response = client.get("/patients", headers=auth_headers)

    assert response.status_code == 200
    assert "patients" in response.json()


def test_get_patient_by_id(client, auth_headers):
    create_response = client.post(
        "/patients",
        headers=auth_headers,
        json={
            "first_name": "David",
            "last_name": "Brown",
            "age": 28,
            "gender": "Male",
            "contact_number": "9876543211"
        }
    )

    patient_id = create_response.json()["patient"]["patient_id"]

    response = client.get(
        f"/patients/{patient_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["patient_id"] == patient_id


def test_update_patient(client, auth_headers):
    create_response = client.post(
        "/patients",
        headers=auth_headers,
        json={
            "first_name": "Sam",
            "last_name": "Wilson",
            "age": 25,
            "gender": "Male",
            "contact_number": "9876543212"
        }
    )

    patient_id = create_response.json()["patient"]["patient_id"]

    response = client.put(
        f"/patients/{patient_id}",
        headers=auth_headers,
        json={
            "first_name": "Samuel",
            "last_name": "Wilson",
            "age": 26,
            "gender": "Male",
            "contact_number": "9876543212"
        }
    )

    assert response.status_code == 200
    assert response.json()["patient"]["first_name"] == "Samuel"


def test_delete_patient(client, auth_headers):
    create_response = client.post(
        "/patients",
        headers=auth_headers,
        json={
            "first_name": "Alex",
            "last_name": "Taylor",
            "age": 32,
            "gender": "Male",
            "contact_number": "9876543213"
        }
    )

    patient_id = create_response.json()["patient"]["patient_id"]

    response = client.delete(
        f"/patients/{patient_id}",
        headers=auth_headers
    )

    assert response.status_code == 200


def test_patient_not_found(client, auth_headers):
    response = client.get(
        "/patients/999999",
        headers=auth_headers
    )

    assert response.status_code == 404


def test_patient_access_without_token(client):
    response = client.get("/patients")

    assert response.status_code == 401
