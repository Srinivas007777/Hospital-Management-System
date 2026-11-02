
def create_test_appointment(client, auth_headers):
    # Create a patient
    patient_response = client.post(
        "/patients",
        headers=auth_headers,
        json={
            "first_name": "Test",
            "last_name": "Patient",
            "age": 30,
            "gender": "Male",
            "contact_number": "9876543210"
        }
    )

    patient_id = patient_response.json()["patient"]["patient_id"]

    # Create a doctor
    doctor_response = client.post(
        "/doctors",
        headers=auth_headers,
        json={
            "first_name": "Test",
            "last_name": "Doctor",
            "specialty": "Cardiology",
            "contact_number": "9876543211"
        }
    )

    doctor_id = doctor_response.json()["doctor"]["doctor_id"]

    # Create appointment
    appointment_response = client.post(
        "/appointments",
        headers=auth_headers,
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_date": "2026-11-15",
            "status": "Scheduled"
        }
    )

    return appointment_response.json()["appointment"]


def test_create_appointment(client, auth_headers):
    appointment = create_test_appointment(client, auth_headers)

    assert appointment["appointment_id"] > 0
    assert appointment["status"] == "Scheduled"


def test_get_appointments(client, auth_headers):
    create_test_appointment(client, auth_headers)

    response = client.get(
        "/appointments",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert "appointments" in response.json()


def test_get_appointment_by_id(client, auth_headers):
    appointment = create_test_appointment(client, auth_headers)

    appointment_id = appointment["appointment_id"]

    response = client.get(
        f"/appointments/{appointment_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["appointment_id"] == appointment_id


def test_update_appointment(client, auth_headers):
    appointment = create_test_appointment(client, auth_headers)

    appointment_id = appointment["appointment_id"]

    response = client.put(
        f"/appointments/{appointment_id}",
        headers=auth_headers,
        json={
            "patient_id": appointment["patient_id"],
            "doctor_id": appointment["doctor_id"],
            "appointment_date": "2026-11-20",
            "status": "Completed"
        }
    )

    assert response.status_code == 200
    assert response.json()["appointment"]["status"] == "Completed"


def test_delete_appointment(client, auth_headers):
    appointment = create_test_appointment(client, auth_headers)

    appointment_id = appointment["appointment_id"]

    response = client.delete(
        f"/appointments/{appointment_id}",
        headers=auth_headers
    )

    assert response.status_code == 200


def test_appointment_not_found(client, auth_headers):
    response = client.get(
        "/appointments/999999",
        headers=auth_headers
    )

    assert response.status_code == 404


def test_appointment_access_without_token(client):
    response = client.get("/appointments")

    assert response.status_code == 401
