from pydantic import BaseModel, Field


class Prescription(BaseModel):
    appointment_id: int = Field(gt=0)
    medication: str = Field(min_length=2, max_length=100)
    dosage: str = Field(min_length=1, max_length=100)
    instructions: str = Field(min_length=2, max_length=500)


class PrescriptionResponse(BaseModel):
    prescription_id: int
    appointment_id: int
    medication: str
    dosage: str
    instructions: str


class PrescriptionResponseMessage(BaseModel):
    message: str
    prescription: PrescriptionResponse


class PrescriptionsListResponse(BaseModel):
    message: str
    prescriptions: list[PrescriptionResponse]