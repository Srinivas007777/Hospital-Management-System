
import sqlite3

from fastapi import APIRouter, Depends, HTTPException, status

from models.patient import (
    Patient,
    PatientResponse,
    PatientResponseMessage,
    PatientsListResponse,
    MessageResponse
)

from database import (
    insert_patient,
    fetch_all_patients,
    fetch_patient_by_id,
    update_patient,
    delete_patient
)

from dependencies import (
    admin_required,
    admin_or_doctor_required,
    admin_or_receptionist_required
)

from logging_config import logger


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


# CREATE PATIENT - ADMIN OR RECEPTIONIST
@router.post(
    "",
    response_model=PatientResponseMessage,
    status_code=status.HTTP_201_CREATED
)
def create_patient(
    patient: Patient,
    current_user=Depends(admin_or_receptionist_required)
):
    try:
        patient_id = insert_patient(patient.model_dump())
        new_patient = fetch_patient_by_id(patient_id)

        logger.info("Patient created successfully: ID %s", patient_id)

        return {
            "message": "Patient registered successfully",
            "patient": dict(new_patient)
        }

    except sqlite3.IntegrityError:
        logger.exception("Database integrity error while creating patient")
        raise HTTPException(
            status_code=400,
            detail="Unable to create patient"
        )

    except sqlite3.Error:
        logger.exception("Database error while creating patient")
        raise HTTPException(
            status_code=500,
            detail="An internal database error occurred"
        )


# GET ALL PATIENTS - ADMIN OR DOCTOR
@router.get(
    "",
    response_model=PatientsListResponse
)
def get_patients(
    current_user=Depends(admin_or_doctor_required)
):
    try:
        patients = fetch_all_patients()

        logger.info("All patients retrieved successfully")

        return {
            "message": "Patients retrieved successfully",
            "patients": [dict(patient) for patient in patients]
        }

    except sqlite3.Error:
        logger.exception("Database error while retrieving patients")
        raise HTTPException(
            status_code=500,
            detail="An internal database error occurred"
        )


# GET PATIENT BY ID - ADMIN OR DOCTOR
@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
def get_patient(
    patient_id: int,
    current_user=Depends(admin_or_doctor_required)
):
    try:
        patient = fetch_patient_by_id(patient_id)

        if patient is None:
            logger.warning("Patient not found: ID %s", patient_id)
            raise HTTPException(
                status_code=404,
                detail="Patient not found"
            )

        logger.info("Patient retrieved successfully: ID %s", patient_id)

        return dict(patient)

    except HTTPException:
        raise

    except sqlite3.Error:
        logger.exception("Database error while retrieving patient ID %s", patient_id)
        raise HTTPException(
            status_code=500,
            detail="An internal database error occurred"
        )


# UPDATE PATIENT - ADMIN ONLY
@router.put(
    "/{patient_id}",
    response_model=PatientResponseMessage
)
def edit_patient(
    patient_id: int,
    patient: Patient,
    current_user=Depends(admin_required)
):
    try:
        existing_patient = fetch_patient_by_id(patient_id)

        if existing_patient is None:
            logger.warning("Cannot update. Patient not found: ID %s", patient_id)
            raise HTTPException(
                status_code=404,
                detail="Patient not found"
            )

        update_patient(patient_id, patient.model_dump())
        updated_patient = fetch_patient_by_id(patient_id)

        logger.info("Patient updated successfully: ID %s", patient_id)

        return {
            "message": "Patient updated successfully",
            "patient": dict(updated_patient)
        }

    except HTTPException:
        raise

    except sqlite3.IntegrityError:
        logger.exception("Database integrity error while updating patient ID %s", patient_id)
        raise HTTPException(
            status_code=400,
            detail="Unable to update patient"
        )

    except sqlite3.Error:
        logger.exception("Database error while updating patient ID %s", patient_id)
        raise HTTPException(
            status_code=500,
            detail="An internal database error occurred"
        )


# DELETE PATIENT - ADMIN ONLY
@router.delete(
    "/{patient_id}",
    response_model=MessageResponse
)
def remove_patient(
    patient_id: int,
    current_user=Depends(admin_required)
):
    try:
        existing_patient = fetch_patient_by_id(patient_id)

        if existing_patient is None:
            logger.warning("Cannot delete. Patient not found: ID %s", patient_id)
            raise HTTPException(
                status_code=404,
                detail="Patient not found"
            )

        delete_patient(patient_id)

        logger.info("Patient deleted successfully: ID %s", patient_id)

        return {
            "message": "Patient deleted successfully"
        }

    except HTTPException:
        raise

    except sqlite3.IntegrityError:
        logger.exception("Cannot delete patient ID %s because related records exist", patient_id)
        raise HTTPException(
            status_code=400,
            detail="Cannot delete patient because related records exist"
        )

    except sqlite3.Error:
        logger.exception("Database error while deleting patient ID %s", patient_id)
        raise HTTPException(
            status_code=500,
            detail="An internal database error occurred"
        )
