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
    Column("hours", Integer),
    Column("zet", Integer),
    Column("education_form", Enum(Education_form)),
) 

disciplines_in_shedule_plan_table = Table(
    "DisciplineInShedulePlan",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("shedule_plan",Integer, ForeignKey("ShedulePlan.id")),
    Column("discipline",Integer, ForeignKey("Disciplines.id")),
) 

shedule_plan_table = Table(
    "ShedulePlan",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
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
    Column("education_form", Enum(Education_form)),
    Column("period", Integer)
)


metadata.create_all(engine)
