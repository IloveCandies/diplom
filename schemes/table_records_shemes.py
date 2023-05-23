import datetime
from typing import Union, List
from uuid import uuid4
from enum import Enum
from pydantic.dataclasses import dataclass
from datetime import date
from pydantic import BaseModel


@dataclass
class DisciplineTableRecord():
    id:int
    name:str

@dataclass
class DisciplinesInShedulePlanTablerecord():
    id:int
    hours:int
    zet: int

@dataclass
class ShedulePlanTableRecord():
    code:str
    recruitment_year:datetime.date
    form:Education_form
    period:int

@dataclass
class RegionTableRecord():
    id:int
    number:int
    name:str

@dataclass
class SityTableRecord():
    id:int
    region: Region
    name:str

#схема соответующая модели бд
class GroupTableRecord(BaseModel):
    id:int
    name: str
    year_of_recruitment:int
    available_places:int
    potential_places:int
    course:int
    end_year:int
    shedule_plan:int

class StudentTableRecord(BaseModel):
    id:int
    first_name:str
    middle_name:str
    last_name:str
    phone:str = "8-800-555-35-35"
    email:str = "default@mail.com"
    password:str
    sity: int
    favorite_list: int

class UniversityStaffRecord(BaseModel):
    id:int
    first_name:str
    middle_name:str
    last_name:str
    phone:str = "8-800-555-35-35"
    email:str = "default@mail.com"
    password:str
    api_token:str