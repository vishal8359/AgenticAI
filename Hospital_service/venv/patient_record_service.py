@app.put("/patients/{patient_id}", response_model=PatientOut)
def update_patient(
    patient_id: int,
    patient: PatientCreate,
    db: Session = Depends(get_db)
):
    ptn = db.query(Patient).filter(Patient.id == patient_id).first()

    if not ptn:
        raise HTTPException(status_code=404, detail="Patient not found")

    try:
        ptn.first_name = patient.first_name
        ptn.last_name = patient.last_name
        ptn.dob = patient.dob
        ptn.notes = patient.notes

        db.commit()
        db.refresh(ptn)
        return ptn

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Patient with same name and dob already exists"
        )
