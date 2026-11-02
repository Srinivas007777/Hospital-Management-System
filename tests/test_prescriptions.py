
def create_test_prescription(client, auth_headers):
    # Create patient
    patient_response = client.post(
        "/patients",
        headers=auth_headers,
        json={
            "first_name": "Test",
            "last_name": "Patient",
            "age": 35,
            "gender": "Male",
            "contact_number": "9876543210"
        }
    )

    patient_id = patient_response.json()["patient"]["patient_id"]

    # Create doctor
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

    appointment_id = appointment_response.json()["appointment"]["appointment_id"]

    # Create prescription
    prescription_response = client.post(
        "/prescriptions",
        headers=auth_headers,
        json={
            "appointment_id": appointment_id,
            "medication": "Paracetamol",
            "dosage": "500mg",
            "instructions": "Take twice daily after food"
        }
    )

    return prescription_response.json()["prescription"]


def test_create_prescription(client, auth_headers):
    prescription = create_test_prescription(client, auth_headers)

    assert prescription["prescription_id"] > 0
    assert prescription["medication"] == "Paracetamol"


def test_get_prescriptions(client, auth_headers):
    create_test_prescription(client, auth_headers)

    response = client.get(
        "/prescriptions",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert "prescriptions" in response.json()


def test_get_prescription_by_id(client, auth_headers):
    prescription = create_test_prescription(client, auth_headers)

    prescription_id = prescription["prescription_id"]

    response = client.get(
        f"/prescriptions/{prescription_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["prescription_id"] == prescription_id


def test_update_prescription(client, auth_headers):
    prescription = create_test_prescription(client, auth_headers)

    prescription_id = prescription["prescription_id"]

    response = client.put(
        f"/prescriptions/{prescription_id}",
        headers=auth_headers,
        json={
            "appointment_id": prescription["appointment_id"],
            "medication": "Ibuprofen",
            "dosage": "200mg",
            "instructions": "Take after meals"
        }
    )

    assert response.status_code == 200
    assert response.json()["prescription"]["medication"] == "Ibuprofen"


def test_delete_prescription(client, auth_headers):
    prescription = create_test_prescription(client, auth_headers)

    prescription_id = prescription["prescription_id"]

    response = client.delete(
        f"/prescriptions/{prescription_id}",
        headers=auth_headers
    )

    assert response.status_code == 200


def test_prescription_not_found(client, auth_headers):
    response = client.get(
        "/prescriptions/999999",
        headers=auth_headers
    )

    assert response.status_code == 404


def test_prescription_access_without_token(client):
    response = client.get("/prescriptions")

    assert response.status_code == 401
