
import sqlite3

from fastapi import APIRouter, Depends, HTTPException, status

from models.prescription import (
    Prescription,
    PrescriptionResponse,
    PrescriptionResponseMessage,
    PrescriptionsListResponse
)

from database import (
    insert_prescription,
    fetch_all_prescriptions,
    fetch_prescription_by_id,
    update_prescription,
    delete_prescription
)

from dependencies import (
    admin_or_doctor_required,
    admin_required
)

from logging_config import logger


router = APIRouter(
    prefix="/prescriptions",
    tags=["Prescriptions"]
)


# CREATE PRESCRIPTION - ADMIN AND DOCTOR
@router.post(
    "",
    response_model=PrescriptionResponseMessage,
    status_code=status.HTTP_201_CREATED
)
def create_prescription(
    prescription: Prescription,
    current_user=Depends(admin_or_doctor_required)
):
    try:
        prescription_id = insert_prescription(
            prescription.model_dump()
        )

        new_prescription = fetch_prescription_by_id(prescription_id)

        logger.info(
            "Prescription created successfully: ID %s",
            prescription_id
        )

        return {
            "message": "Prescription created successfully",
            "prescription": dict(new_prescription)
        }

    except sqlite3.IntegrityError:
        logger.exception("Database integrity error while creating prescription")
        raise HTTPException(
            status_code=400,
            detail="Invalid appointment ID"
        )

    except sqlite3.Error:
        logger.exception("Database error while creating prescription")
        raise HTTPException(
            status_code=500,
            detail="An internal database error occurred"
        )


# GET ALL PRESCRIPTIONS - ADMIN AND DOCTOR
@router.get(
    "",
    response_model=PrescriptionsListResponse
)
def get_prescriptions(
    current_user=Depends(admin_or_doctor_required)
):
    try:
        prescriptions = fetch_all_prescriptions()

        logger.info("All prescriptions retrieved successfully")

        return {
            "message": "Prescriptions retrieved successfully",
            "prescriptions": [
                dict(prescription) for prescription in prescriptions
            ]
        }

    except sqlite3.Error:
        logger.exception("Database error while retrieving prescriptions")
        raise HTTPException(
            status_code=500,
            detail="An internal database error occurred"
        )


# GET PRESCRIPTION BY ID - ADMIN AND DOCTOR
@router.get(
    "/{prescription_id}",
    response_model=PrescriptionResponse
)
def get_prescription(
    prescription_id: int,
    current_user=Depends(admin_or_doctor_required)
):
    try:
        prescription = fetch_prescription_by_id(prescription_id)

        if prescription is None:
            logger.warning(
                "Prescription not found: ID %s",
                prescription_id
            )
            raise HTTPException(
                status_code=404,
                detail="Prescription not found"
            )

        logger.info(
            "Prescription retrieved successfully: ID %s",
            prescription_id
        )

        return dict(prescription)

    except HTTPException:
        raise

    except sqlite3.Error:
        logger.exception(
            "Database error while retrieving prescription ID %s",
            prescription_id
        )
        raise HTTPException(
            status_code=500,
            detail="An internal database error occurred"
        )


# UPDATE PRESCRIPTION - ADMIN AND DOCTOR
@router.put(
    "/{prescription_id}",
    response_model=PrescriptionResponseMessage
)
def edit_prescription(
    prescription_id: int,
    prescription: Prescription,
    current_user=Depends(admin_or_doctor_required)
):
    try:
        existing_prescription = fetch_prescription_by_id(prescription_id)

        if existing_prescription is None:
            logger.warning(
                "Cannot update. Prescription not found: ID %s",
                prescription_id
            )
            raise HTTPException(
                status_code=404,
                detail="Prescription not found"
            )

        update_prescription(
            prescription_id,
            prescription.model_dump()
        )

        updated_prescription = fetch_prescription_by_id(prescription_id)

        logger.info(
            "Prescription updated successfully: ID %s",
            prescription_id
        )

        return {
            "message": "Prescription updated successfully",
            "prescription": dict(updated_prescription)
        }

    except HTTPException:
        raise

    except sqlite3.IntegrityError:
        logger.exception(
            "Database integrity error while updating prescription ID %s",
            prescription_id
        )
        raise HTTPException(
            status_code=400,
            detail="Invalid appointment ID"
        )

    except sqlite3.Error:
        logger.exception(
            "Database error while updating prescription ID %s",
            prescription_id
        )
        raise HTTPException(
            status_code=500,
            detail="An internal database error occurred"
        )


# DELETE PRESCRIPTION - ADMIN ONLY
@router.delete("/{prescription_id}")
def remove_prescription(
    prescription_id: int,
    current_user=Depends(admin_required)
):
    try:
        existing_prescription = fetch_prescription_by_id(prescription_id)

        if existing_prescription is None:
            logger.warning(
                "Cannot delete. Prescription not found: ID %s",
                prescription_id
            )
            raise HTTPException(
                status_code=404,
                detail="Prescription not found"
            )

        delete_prescription(prescription_id)

        logger.info(
            "Prescription deleted successfully: ID %s",
            prescription_id
        )

        return {
            "message": "Prescription deleted successfully"
        }

    except HTTPException:
        raise

    except sqlite3.IntegrityError:
        logger.exception(
            "Database integrity error while deleting prescription ID %s",
            prescription_id
        )
        raise HTTPException(
            status_code=400,
            detail="Unable to delete prescription"
        )

    except sqlite3.Error:
        logger.exception(
            "Database error while deleting prescription ID %s",
            prescription_id
        )
        raise HTTPException(
            status_code=500,
            detail="An internal database error occurred"
        )
