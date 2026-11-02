
import sqlite3

from fastapi import APIRouter, Depends, HTTPException, status

from models.appointment import (
    Appointment,
    AppointmentResponse,
    AppointmentResponseMessage,
    AppointmentsListResponse,
    MessageResponse
)

from database import (
    insert_appointment,
    fetch_all_appointments,
    fetch_appointment_by_id,
    update_appointment,
    delete_appointment
)

from dependencies import (
    admin_required,
    admin_or_receptionist_required,
    require_role
)

from logging_config import logger


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


# ADMIN, DOCTOR AND RECEPTIONIST CAN VIEW APPOINTMENTS
appointment_view_required = require_role(
    "Admin",
    "Doctor",
    "Receptionist"
)


# CREATE APPOINTMENT
@router.post(
    "",
    response_model=AppointmentResponseMessage,
    status_code=status.HTTP_201_CREATED
)
def create_appointment(
    appointment: Appointment,
    current_user=Depends(admin_or_receptionist_required)
):
    try:
        appointment_id = insert_appointment(
            appointment.model_dump(mode="json")
        )

        new_appointment = fetch_appointment_by_id(appointment_id)

        logger.info(
            "Appointment created successfully: ID %s",
            appointment_id
        )

        return {
            "message": "Appointment created successfully",
            "appointment": dict(new_appointment)
        }

    except sqlite3.IntegrityError:
        logger.exception("Database integrity error while creating appointment")
        raise HTTPException(
            status_code=400,
            detail="Invalid patient ID or doctor ID"
        )

    except sqlite3.Error:
        logger.exception("Database error while creating appointment")
        raise HTTPException(
            status_code=500,
            detail="An internal database error occurred"
        )


# GET ALL APPOINTMENTS
@router.get(
    "",
    response_model=AppointmentsListResponse
)
def get_appointments(
    current_user=Depends(appointment_view_required)
):
    try:
        appointments = fetch_all_appointments()

        logger.info("All appointments retrieved successfully")

        return {
            "message": "Appointments retrieved successfully",
            "appointments": [
                dict(appointment) for appointment in appointments
            ]
        }

    except sqlite3.Error:
        logger.exception("Database error while retrieving appointments")
        raise HTTPException(
            status_code=500,
            detail="An internal database error occurred"
        )


# GET APPOINTMENT BY ID
@router.get(
    "/{appointment_id}",
    response_model=AppointmentResponse
)
def get_appointment(
    appointment_id: int,
    current_user=Depends(appointment_view_required)
):
    try:
        appointment = fetch_appointment_by_id(appointment_id)

        if appointment is None:
            logger.warning(
                "Appointment not found: ID %s",
                appointment_id
            )
            raise HTTPException(
                status_code=404,
                detail="Appointment not found"
            )

        logger.info(
            "Appointment retrieved successfully: ID %s",
            appointment_id
        )

        return dict(appointment)

    except HTTPException:
        raise

    except sqlite3.Error:
        logger.exception(
            "Database error while retrieving appointment ID %s",
            appointment_id
        )
        raise HTTPException(
            status_code=500,
            detail="An internal database error occurred"
        )


# UPDATE APPOINTMENT
@router.put(
    "/{appointment_id}",
    response_model=AppointmentResponseMessage
)
def edit_appointment(
    appointment_id: int,
    appointment: Appointment,
    current_user=Depends(admin_or_receptionist_required)
):
    try:
        existing_appointment = fetch_appointment_by_id(appointment_id)

        if existing_appointment is None:
            logger.warning(
                "Cannot update. Appointment not found: ID %s",
                appointment_id
            )
            raise HTTPException(
                status_code=404,
                detail="Appointment not found"
            )

        update_appointment(
            appointment_id,
            appointment.model_dump(mode="json")
        )

        updated_appointment = fetch_appointment_by_id(appointment_id)

        logger.info(
            "Appointment updated successfully: ID %s",
            appointment_id
        )

        return {
            "message": "Appointment updated successfully",
            "appointment": dict(updated_appointment)
        }

    except HTTPException:
        raise

    except sqlite3.IntegrityError:
        logger.exception(
            "Database integrity error while updating appointment ID %s",
            appointment_id
        )
        raise HTTPException(
            status_code=400,
            detail="Invalid patient ID or doctor ID"
        )

    except sqlite3.Error:
        logger.exception(
            "Database error while updating appointment ID %s",
            appointment_id
        )
        raise HTTPException(
            status_code=500,
            detail="An internal database error occurred"
        )


# DELETE APPOINTMENT
@router.delete(
    "/{appointment_id}",
    response_model=MessageResponse
)
def remove_appointment(
    appointment_id: int,
    current_user=Depends(admin_required)
):
    try:
        existing_appointment = fetch_appointment_by_id(appointment_id)

        if existing_appointment is None:
            logger.warning(
                "Cannot delete. Appointment not found: ID %s",
                appointment_id
            )
            raise HTTPException(
                status_code=404,
                detail="Appointment not found"
            )

        delete_appointment(appointment_id)

        logger.info(
            "Appointment deleted successfully: ID %s",
            appointment_id
        )

        return {
            "message": "Appointment deleted successfully"
        }

    except HTTPException:
        raise

    except sqlite3.IntegrityError:
        logger.exception(
            "Cannot delete appointment ID %s because related prescriptions exist",
            appointment_id
        )
        raise HTTPException(
            status_code=400,
            detail="Cannot delete appointment because related prescriptions exist"
        )

    except sqlite3.Error:
        logger.exception(
            "Database error while deleting appointment ID %s",
            appointment_id
        )
        raise HTTPException(
            status_code=500,
            detail="An internal database error occurred"
        )
