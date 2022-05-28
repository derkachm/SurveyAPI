from msilib.schema import Class
from time import strftime
from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Survey(BaseModel):
    name: str
    desc: Optional[str] = None
    published: bool = True
 

@app.get("/")
def root():
    return {"message": "Hello WRLD!"}

@app.get("/surveys")
def get_surveys():
    return {"data": "This is your surveys"}

@app.post("/createsurveys")
def create_surveys(survey: Survey):
    print(survey)
    return {"data": "Survey have been created"}