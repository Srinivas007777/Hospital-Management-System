from datetime import date
from pydantic import BaseModel, Field


class Appointment(BaseModel):
    patient_id: int = Field(gt=0)
    doctor_id: int = Field(gt=0)
    appointment_date: date
    status: str = "Scheduled"


class AppointmentResponse(BaseModel):
    appointment_id: int
    patient_id: int
    doctor_id: int
    appointment_date: date
    status: str


class AppointmentResponseMessage(BaseModel):
    message: str
    appointment: AppointmentResponse


class AppointmentsListResponse(BaseModel):
    message: str
    appointments: list[AppointmentResponse]


class MessageResponse(BaseModel):
    message: str