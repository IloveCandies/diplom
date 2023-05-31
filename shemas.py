import datetime
from typing import Union, List, Tuple
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

#как назвать подумать
class OOP(BaseModel):    
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
class Discipline(BaseModel):
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
    

class ShedulePlan(BaseModel):
    code:str
    recruitment_year:datetime.date
    oop: Union[None, OOP] 
    form:Union[Education_form,str] = Education_form.Очная
    period:int
    disciplines:Union[List, List[DisciplinesInShedulePlan]] =[]
    
    class Config:
        orm_mode = True


class ShedulePlanDetail(BaseModel):
    code:str
    recruitment_year:datetime.date
    oop: Union[None, OOP] 
    form:Education_form
    period:int


class ShedulePlanTableRecord(BaseModel):
    code:str
    recruitment_year:datetime.date
    form:Education_form
    period:int

class DisciplinesInStudentEducation(BaseModel):
    id:int
    name:str
    hours:int
    zet: int
    education_form: Education_form


class StudentEducation(BaseModel):
    id:int
    level:Education_level
    oop:OOP
    form:Education_form
    education_end: bool
    date_of_end_education: datetime.date
    disciplines: List[Discipline]

class Region(BaseModel):
    id:int
    number:int
    name:str

class CityTableRecord(BaseModel):
    id:int
    region: int
    name:str = ""

class City(BaseModel):
    region: Union[Region,None] = None
    name:str = ""


class Education(BaseModel):
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

class University(BaseModel):
    id:int
    name: str
    сity: City
    description: Union[str, None] = None
    university_staff: Union[List[UniversityStaff], None] = None
        

class Group(BaseModel):
    name: str
    year_of_recruitment:int
    available_places:int
    potential_places:int
    course:int
    end_year:int
    shedule_plan_id:int


# json учебного плана
class GroupData(BaseModel):
    year_of_recruitment:int
    available_places:int
    potential_places:int
    course:int
    end_year:int


# json учебного плана
class GroupDetail(BaseModel):
    name: str
    year_of_recruitment:int
    available_places:int
    potential_places:int
    course:int
    end_year:int
    shedule_plan:Union[ShedulePlan,None] = None

    class Config:
        orm_mode = True

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




#Переименовать схемы потом
@dataclass
class StudentFavoriteListItem():
    group: GroupDetail
    messge:str = "Вот мой сопроводительный текст: Хочу на бюджет потому что я крутой"

    class Config:
        orm_mode = True

class FavoriteList(BaseModel):
    groups: list[StudentFavoriteListItem]
    
    class Config:
        orm_mode = True

class FavoriteListItem(BaseModel):
    messge:str = "Вот мой сопроводительный текст: Хочу на бюджет потому что я крутой"

    class Config:
        orm_mode = True
    
####
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
    first_name:str = " "
    middle_name:str = " "
    last_name:str = " "
    phone:str = "8-800-555-35-35"
    email:str = "default@mail.com"
    сity: Union[City,None] = None
 

class StudentData(BaseModel):
    first_name:str
    middle_name:str
    last_name:str
    phone:str = ""

class StudentData(BaseModel):
    first_name:str
    middle_name:str
    last_name:str
    phone:str = ""

class Item(BaseModel):
    id: str
    value: str




class Message(BaseModel):
    datetime:datetime.datetime
    message: str
