from fastapi import FastAPI,HTTPException
import json


app=FastAPI()

@app.get("/")
def hello():
    return("messange from backend :Hello")

def load_data():
    with open("patients.json","r") as f:
        data=json.load(f)
    return data 

 
@app.get("/patients")
def patients():
    data=load_data()
    return data   

@app.get("/patient/{patient_id}")
def patients(patient_id:str):
    data=load_data()

    if patient_id in data :
        return data[patient_id] 
    raise HTTPException(status_code=404, detail="Patient not found")