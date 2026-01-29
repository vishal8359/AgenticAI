from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import date


@app.post("/appointments/", response_model=AppointmentOut)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):
    # Check patient exists
    patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Check same date appointment
    existing_same_date = (
        db.query(Appointment)
        .filter(
            Appointment.patient_id == appointment.patient_id,
            Appointment.scheduled_at == appointment.scheduled_at
        )
        .first()
    )
    if existing_same_date:
        raise HTTPException(
            status_code=409,
            detail="Appointment already scheduled for this date"
        )

    # Check if any other appointment exists
    existing_appointment = (
        db.query(Appointment)
        .filter(Appointment.patient_id == appointment.patient_id)
        .first()
    )

    try:
        if existing_appointment:
            existing_appointment.scheduled_at = appointment.scheduled_at
            existing_appointment.reason = appointment.reason
            if not existing_appointment.status:
                existing_appointment.status = "scheduled"
            db.commit()
            db.refresh(existing_appointment)
            return existing_appointment
        else:
            new_appointment = Appointment(
                patient_id=appointment.patient_id,
                scheduled_at=appointment.scheduled_at,
                reason=appointment.reason,
                status="scheduled"
            )
            db.add(new_appointment)
            db.commit()
            db.refresh(new_appointment)
            return new_appointment

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Appointment conflict")


@app.get("/appointments/", response_model=List[AppointmentOut])
def list_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()
