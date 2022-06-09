from msilib.schema import Class
from time import strftime
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()

class Survey(BaseModel):
    name: str
    desc: Optional[str] = None
    published: bool = True
 
my_surveys = [{"name": "survey #1", "desc": "survey #1 description", "id": 1},
              {"name": "survey #2", "desc": "survey #2 description", "id": 2}]

def find_survey(id):
    return next((item for item in my_surveys if item["id"] == id), None)

def find_index_survey(id):
    return next((index for (index, s) in enumerate(my_surveys) if s["id"] == id), None)

@app.get("/")
def root():
    return {"message": "Hello WRLD!"}

@app.get("/surveys")
def get_surveys():
    return {"data": my_surveys}

@app.get("/surveys/{id}")
def get_surveys(id: int):
    # print(id)
    survey = find_survey(id)
    if not survey:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f'Survey with id: {id} was not found')
    return {"survey_detail": survey}

@app.post("/surveys", status_code=status.HTTP_201_CREATED)
def create_surveys(survey: Survey):
    dict_survey = survey.dict()
    dict_survey["id"] = randrange(0, 999999999)
    my_surveys.append(dict_survey)
    return {"data": dict_survey}

@app.delete("/surveys/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_survey(id: int):
    index = find_index_survey(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f'Survey with id: {id} was not found')
    my_surveys.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/surveys/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_survey(id: int, survey: Survey):
    index = find_index_survey(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f'Survey with id: {id} was not found')
    survey_dict = survey.dict()
    survey_dict['id'] = id
    my_surveys[index] = survey_dict
    # s = my_surveys.index(index)
    # s = survey
    print (survey)

    return {"data": survey_dict}