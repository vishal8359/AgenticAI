from sqlalchemy import Column, Integer, String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    dob = Column(Date, nullable=False)
    notes = Column(String(1000))

    appointments = relationship("Appointment", back_populates="patient")

    __table_args__ = (
        UniqueConstraint("first_name", "last_name", "dob", name="uq_patient"),
    )


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    scheduled_at = Column(Date, nullable=False)
    reason = Column(String(255))
    status = Column(String(50), default="scheduled")

    patient = relationship("Patient", back_populates="appointments")

    __table_args__ = (
        UniqueConstraint("patient_id", "scheduled_at", name="uq_patient_date"),
    )
