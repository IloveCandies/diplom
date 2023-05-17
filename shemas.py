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
#как назвать подумать
class OOP():    
    code: str
    direction: str
    eduction_profile: str
    education_level:Education_level

@dataclass
#как назвать подумать
class OOPTableRecord():
    id:int    
    code: str
    direction: str
    eduction_profile: str
    education_level:Education_level

@dataclass
class Discipline():
    name:str

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
class DisciplinesInShedulePlan():
    name:str
    hours:int
    zet: int
    

@dataclass
class ShedulePlan():
    code:str
    recruitment_year:datetime.date
    oop: Union[None, OOP] 
    form:Education_form
    period:int
    disciplines: List[DisciplinesInShedulePlan]

@dataclass
class ShedulePlanTableRecord():
    code:str
    recruitment_year:datetime.date
    form:Education_form
    period:int

@dataclass
class DisciplinesInStudentEducation():
    id:int
    name:str
    hours:int
    zet: int
    education_form: Education_form

@dataclass
class StudentEducation():
    id:int
    level:Education_level
    oop:OOP
    form:Education_form
    education_end: bool
    date_of_end_education: datetime.date
    disciplines: List[Discipline]

@dataclass
class Region():
    id:int
    number:int
    name:str

@dataclass
class Sity():
    id:int
    region: Region
    name:str

@dataclass
class Education():
    id:int
    level:Education_level
    oop:OOP
    form:Education_form
    education_end: bool
    date_of_end_education: datetime.date
    

class LoginData(BaseModel):
    first_name:str = "Default"
    middle_name:str  ="Default"
    last_name:str  = "Default"
    phone:str = "8-800-555-35-35"
    email:str = "default@mail.com"
    password:str  = ""

class UniversityStaff(BaseModel):
    first_name:str = "Default"
    middle_name:str  ="Default"
    last_name:str  = "Default"
    phone:str = "8-800-555-35-35"
    email:str = "default@mail.com"
    password:str  =""
    api_token:str =""

class UniversityStaffRecord(BaseModel):
    id:int
    first_name:str
    middle_name:str
    last_name:str
    phone:str = "8-800-555-35-35"
    email:str = "default@mail.com"
    password:str
    api_token:str

@dataclass
class University(BaseModel):
    id:int
    name: str
    sity: Sity
    description: Union[str, None] = None
    university_staff: Union[List[UniversityStaff], None] = None
        
@dataclass
class Group():
    name: str
    year_of_recruitment:int
    available_places:int
    potential_places:int
    course:int
    end_year:int

# json учебного плана
@dataclass
class GroupDetail():
    name: str
    year_of_recruitment:int
    available_places:int
    potential_places:int
    course:int
    end_year:int
    shedule_plan:ShedulePlan

#схема соответующая модели бд
@dataclass
class GroupTableRecord():
    id:int
    name: str
    year_of_recruitment:int
    available_places:int
    potential_places:int
    course:int
    end_year:int
    shedule_plan:int

    
class FavoriteList(BaseModel):
    last_update:Union[str, None] = None
    groups: list[Group] = []
    comment:Union[str, None] = None
    
    def create(self,last_update):
        self.last_update = last_update


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

class Student(BaseModel):
    first_name:str
    middle_name:str
    last_name:str
    phone:str = "8-800-555-35-35"
    email:str = "default@mail.com"
    password:str
    sity: Union[Sity,None] = None
    education:Union[List[StudentEducation],None] = None
    favorite_list: Union[FavoriteList,None] = None 
    
 