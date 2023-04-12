import datetime
from typing import Union, List
from uuid import uuid4
from enum import Enum
from pydantic.dataclasses import dataclass
from datetime import date
from pydantic import BaseModel

class Education_level(Enum):
    Специалитет = 1
    Бакалавриат = 2
    Магистратура =3

class Education_form(Enum):
    Очная = 1
    Заочная = 2
    Очно_заочная = 3


@dataclass
class Discipline(BaseModel):
    name:str

@dataclass
#как назвать подумать
class OOP(BaseModel):
    id:str
    code: str
    direction: str
    eduction_profile: str
    education_level:Education_level
    
@dataclass
class DisciplinesInShedulePlan(BaseModel):
    id:str
    name:str
    hours:int
    zet: int
    education_form: Education_form

@dataclass
class ShedulePlan(BaseModel):
    id:str
    recruitment_year:datetime.date
    oop:OOP
    form:Education_form
    period:int
    disciplines: List[DisciplinesInShedulePlan]
  
@dataclass
class DisciplinesInStudentEducation(BaseModel):
    id:str
    hours:int
    zet: int
    education_form: Education_form

@dataclass
class StudentEducation(BaseModel):
    id:str
    level:Education_level
    oop:OOP
    form:Education_form
    education_end: bool
    date_of_end_education: datetime.date
    disciplines: List[Discipline]

@dataclass
class Region():
    id:str
    number:int
    name:str

@dataclass
class Sity():
    id:str
    region: Region
    name:str

@dataclass
class Education(BaseModel):
    id:str
    level:Education_level
    oop:OOP
    form:Education_form
    education_end: bool
    date_of_end_education: datetime.date
    


@dataclass
class UniversityStaff(BaseModel):
    id:str
    first_name:str
    middle_name:str
    last_name:str
    phone:str = "8-800-555-35-35"
    email:str = "default@mail.com"
    password:str
    api_token:str


@dataclass
class University(BaseModel):
    id:str
    name: str
    sity: Sity
    description: Union[str, None] = None
    university_staff: Union[List[UniversityStaff], None] = None
        

class Group(BaseModel):
    id:str
    name: str
    year_of_recruitment:int
    available_places:int
    potential_places:int
    course:int
    end_year:int
    shedule_plan:ShedulePlan

    def create(id,name,year_of_recruitment,available_places,potential_places,course,end_year,shedule_plan):
        return(Group(id = id,name=name,year_of_recruitment=year_of_recruitment,
                     available_places = available_places,potential_places=potential_places,
                     course=course,end_year=end_year,
                     shedule_plan = shedule_plan))
    
class FavoriteList(BaseModel):
    last_update:Union[str, None] = None
    groups: list[Group] = []
    comment:Union[str, None] = None
    
    def create(self,last_update):
        self.last_update = last_update


class Student(BaseModel):
    id:str
    first_name:str
    middle_name:str
    last_name:str
    phone:str = "8-800-555-35-35"
    email:str = "default@mail.com"
    password:str
    sity:Sity
    education:Union[List[StudentEducation],None] = None
    favorite_list: FavoriteList = FavoriteList(last_update=date.today().strftime('%Y-%m-%d'),comment="dddd")
    
    def create(first_name,middle_name,last_name):
        return Student(first_name=first_name,middle_name=middle_name,last_name=last_name, password="None",sity=Sity(region=Region(number=1,name="default_region"),name="default_sity"))
