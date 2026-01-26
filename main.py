from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI is running"}

@app.get("/home")
def home():
    return {"message": "Home founded"}

@app.post("/add-photo")
def add_photo():
    return {"status":"photo added successfully"}