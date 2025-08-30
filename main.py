from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated
import os

app = FastAPI()

# File path for storing patient data
DATA_FILE = "patients.json"

# Ensure the file exists before accessing it
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

# ------------------ Pydantic Model ------------------ #
class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Unique ID of the patient", examples=["p001"])]
    name: str
    city: str
    age: int
    gender: str
    height: Annotated[float, Field(..., gt=0, description="Height in meters")]
    weight: Annotated[float, Field(..., gt=0, description="Weight in kg")]

    # Calculate BMI
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    # Verdict based on BMI
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "underweight"
        elif 18.5 <= self.bmi < 25:
            return "normal"
        elif 25 <= self.bmi < 30:
            return "overweight"
        else:
            return "obese"

# ------------------ Helper Functions ------------------ #
def load_data():
    """Load patient data from JSON file"""
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    """Save patient data to JSON file"""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ------------------ API Endpoints ------------------ #
@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    data[patient.id] = patient.model_dump(exclude={"id"})
    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})

@app.get("/")
def hello():
    return {"message": "Message from backend: Hello"}

@app.get("/patients")
def get_patients():
    return load_data()

@app.get("/patient/{patient_id}")
def get_patient(patient_id: str):
    data = load_data()

    if patient_id in data:
        return data[patient_id]

    raise HTTPException(status_code=404, detail="Patient not found")
