from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date


class PatientCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    dob: date
    notes: Optional[str] = Field(None, max_length=1000)


class PatientOut(PatientCreate):
    id: int

    model_config = {"from_attributes": True}


class AppointmentCreate(BaseModel):
    patient_id: int
    scheduled_at: date
    reason: Optional[str]

    @field_validator("scheduled_at")
    @classmethod
    def scheduled_not_in_past(cls, date_value: date):
        if date_value < date.today():
            raise ValueError("scheduled_at cannot be in the past")
        return date_value


class AppointmentOut(AppointmentCreate):
    id: int
    status: Optional[str]

    model_config = {"from_attributes": True}
