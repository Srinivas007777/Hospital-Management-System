from pydantic import BaseModel, Field


class Doctor(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    specialty: str = Field(min_length=2, max_length=100)
    contact_number: str | None = Field(
        default=None,
        min_length=10,
        max_length=10
    )


class DoctorResponse(BaseModel):
    doctor_id: int
    first_name: str
    last_name: str
    specialty: str
    contact_number: str | None = None


class DoctorResponseMessage(BaseModel):
    message: str
    doctor: DoctorResponse

class DoctorsListResponse(BaseModel):
    message: str
    doctors: list[DoctorResponse]