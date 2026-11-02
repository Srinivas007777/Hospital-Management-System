from pydantic import BaseModel, Field


class Patient(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    age: int = Field(gt=0, lt=120)
    gender: str
    contact_number: str | None = Field(
        default=None,
        min_length=10,
        max_length=10
    )
class PatientResponse(BaseModel):
    patient_id: int
    first_name: str
    last_name: str
    age:int
    gender: str
    contact_number: str | None = None

class PatientResponseMessage(BaseModel):
    message: str
    patient: PatientResponse

class PatientsListResponse(BaseModel):
    message: str
    patients: list[PatientResponse]

class MessageResponse(BaseModel):
    message: str