from sqlalchemy import Enum,Table, Boolean, Date, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.init import Base, metadata, engine
from shemas import Education_level, Education_form


oop_table = Table(
    "OOP",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("code", String, unique=True),
    Column("direction", String),
    Column("eduction_profile", String),
    Column("education_level", Enum(Education_level)),
)



disciplines_table = Table(
    "Disciplines",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, unique=True),
) 

disciplines_in_shedule_plan_table = Table(
    "DisciplineInShedulePlan",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("hours", Integer),
    Column("zet", Integer),
    Column("shedule_plan",Integer, ForeignKey("ShedulePlan.id")),
    Column("discipline",Integer, ForeignKey("Disciplines.id")),
) 

shedule_plan_table = Table(
    "ShedulePlan",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("code", String, unique=True),
    Column("recruitment_year", Date),
    Column("education_form", Enum(Education_form)),
    Column("period", Integer),
    Column("oop",Integer, ForeignKey("OOP.id"))
)

disciplines_in_student_education_table = Table(
    "DisciplinesInStudentEducation",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("hours", Integer),
    Column("zet", Integer),
    Column("education_form", Enum(Education_form))
)

student_education_table = Table(
    "StudentEducation",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("oop_id",Integer, ForeignKey("OOP.id")),
    Column("сourse",Integer),
    Column("education_form", Enum(Education_form)),
    Column("period", Integer)
)

group_table = Table(
    "Group",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name",String, unique = True),
    Column("year_of_recruitment", Integer),
    Column("available_places", Integer,),
    Column("potential_places",Integer),
    Column("course", Integer),
    Column("end_year", Integer),
    Column("shedule_plan",Integer, ForeignKey("ShedulePlan.id")),
)

staff_table = Table(
    "UniversityStaff",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("first_name",String),
    Column("middle_name", String),
    Column("last_name", String),
    Column("phone", String, unique = True),
    Column("email", String, unique = True),
    Column("password", String),
    Column("salt", String),
    Column("api_token", String),
)

student_table = Table(
    "Student",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("first_name",String),
    Column("middle_name", String),
    Column("last_name", String),
    Column("phone", String, unique = True),
    Column("email",String, unique = True),
    Column("password", String),
    Column("salt", String),
    
)

favorites_table = Table(
    "FavoriteList",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("student",Integer, ForeignKey("Student.id"),  unique = True), 
)

favorites_item_table = Table(
    "FavoriteItem",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("favorite_list_id",Integer, ForeignKey("FavoriteList.id")),
    Column("group_id",Integer, ForeignKey("Group.id")),
    Column("message", String),
    
)
#удалить потом на проде
metadata.drop_all(engine)
metadata.create_all(engine)

#Column("password", String),
#Column("password", String),
#Column("password", String),