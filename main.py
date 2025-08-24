from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def hello():
    return("messange from backend :Hello")