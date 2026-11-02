
import sqlite3

from fastapi import APIRouter, Depends, HTTPException, status

from models.doctor import (
    Doctor,
    DoctorResponse,
    DoctorResponseMessage
)

from database import (
    insert_doctor,
    fetch_all_doctors,
    fetch_doctor_by_id,
    update_doctor,
    delete_doctor
)

from dependencies import admin_required, admin_or_doctor_required

from logging_config import logger


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


# CREATE DOCTOR - ADMIN ONLY
@router.post(
    "",
    response_model=DoctorResponseMessage,
    status_code=status.HTTP_201_CREATED
)
def create_doctor(
    doctor: Doctor,
    current_user=Depends(admin_required)
):
    try:
        doctor_id = insert_doctor(doctor.model_dump())
        new_doctor = fetch_doctor_by_id(doctor_id)

        logger.info("Doctor created successfully: ID %s", doctor_id)

        return {
            "message": "Doctor registered successfully",
            "doctor": dict(new_doctor)
        }

    except sqlite3.IntegrityError:
        logger.exception("Database integrity error while creating doctor")
        raise HTTPException(
            status_code=400,
            detail="Unable to create doctor"
        )

    except sqlite3.Error:
        logger.exception("Database error while creating doctor")
        raise HTTPException(
            status_code=500,
            detail="An internal database error occurred"
        )


# GET ALL DOCTORS - ADMIN AND DOCTOR
@router.get("")
def get_doctors(
    current_user=Depends(admin_or_doctor_required)
):
    try:
        doctors = fetch_all_doctors()

        logger.info("All doctors retrieved successfully")

        return {
            "message": "Doctors retrieved successfully",
            "doctors": [dict(doctor) for doctor in doctors]
        }

    except sqlite3.Error:
        logger.exception("Database error while retrieving doctors")
        raise HTTPException(
            status_code=500,
            detail="An internal database error occurred"
        )


# GET DOCTOR BY ID - ADMIN AND DOCTOR
@router.get(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def get_doctor(
    doctor_id: int,
    current_user=Depends(admin_or_doctor_required)
):
    try:
        doctor = fetch_doctor_by_id(doctor_id)

        if doctor is None:
            logger.warning("Doctor not found: ID %s", doctor_id)
            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )

        logger.info("Doctor retrieved successfully: ID %s", doctor_id)

        return dict(doctor)

    except HTTPException:
        raise

    except sqlite3.Error:
        logger.exception("Database error while retrieving doctor ID %s", doctor_id)
        raise HTTPException(
            status_code=500,
            detail="An internal database error occurred"
        )


# UPDATE DOCTOR - ADMIN ONLY
@router.put(
    "/{doctor_id}",
    response_model=DoctorResponseMessage
)
def edit_doctor(
    doctor_id: int,
    doctor: Doctor,
    current_user=Depends(admin_required)
):
    try:
        existing_doctor = fetch_doctor_by_id(doctor_id)

        if existing_doctor is None:
            logger.warning("Cannot update. Doctor not found: ID %s", doctor_id)
            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )

        update_doctor(doctor_id, doctor.model_dump())
        updated_doctor = fetch_doctor_by_id(doctor_id)

        logger.info("Doctor updated successfully: ID %s", doctor_id)

        return {
            "message": "Doctor updated successfully",
            "doctor": dict(updated_doctor)
        }

    except HTTPException:
        raise

    except sqlite3.IntegrityError:
        logger.exception("Database integrity error while updating doctor ID %s", doctor_id)
        raise HTTPException(
            status_code=400,
            detail="Unable to update doctor"
        )

    except sqlite3.Error:
        logger.exception("Database error while updating doctor ID %s", doctor_id)
        raise HTTPException(
            status_code=500,
            detail="An internal database error occurred"
        )


# DELETE DOCTOR - ADMIN ONLY
@router.delete("/{doctor_id}")
def remove_doctor(
    doctor_id: int,
    current_user=Depends(admin_required)
):
    try:
        existing_doctor = fetch_doctor_by_id(doctor_id)

        if existing_doctor is None:
            logger.warning("Cannot delete. Doctor not found: ID %s", doctor_id)
            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )

        delete_doctor(doctor_id)

        logger.info("Doctor deleted successfully: ID %s", doctor_id)

        return {
            "message": "Doctor deleted successfully"
        }

    except HTTPException:
        raise

    except sqlite3.IntegrityError:
        logger.exception(
            "Cannot delete doctor ID %s because related appointments exist",
            doctor_id
        )
        raise HTTPException(
            status_code=400,
            detail="Cannot delete doctor because related appointments exist"
        )

    except sqlite3.Error:
        logger.exception("Database error while deleting doctor ID %s", doctor_id)
        raise HTTPException(
            status_code=500,
            detail="An internal database error occurred"
        )
