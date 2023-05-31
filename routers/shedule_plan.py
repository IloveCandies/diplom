from asyncpg import exceptions
from fastapi import APIRouter
from shemas import *
from db.models import shedule_plan_table, oop_table,disciplines_table,disciplines_in_shedule_plan_table, group_table
from db.init import database
from fastapi.responses import JSONResponse
from asyncpg.exceptions import UniqueViolationError
from sqlite3 import IntegrityError

shedule_plan_router = APIRouter( responses={404: {"description": "Not found"}})


async def get_shedule_plan_by_id(shedule_plan_id: int) -> Union[ShedulePlan,None]:
    query = disciplines_in_shedule_plan_table.select().where(disciplines_in_shedule_plan_table.c.shedule_plan == shedule_plan_id)

    disciplines_in_plan = [ tuple(item.values())[0:3] for item  in await database.fetch_all(query)]
    query = shedule_plan_table.select().where(shedule_plan_table.c.id == shedule_plan_id)
    shedule_plan = await database.fetch_one(query)
    
    if shedule_plan == None:
        return None
    else:
        print(shedule_plan.education_form)
        query = oop_table.select().where(oop_table.c.id == shedule_plan.oop)   
        oop_detail = await database.fetch_one(query)
        print(shedule_plan.education_form)
        return ShedulePlan( code = shedule_plan.code,
                        recruitment_year = shedule_plan.recruitment_year,
                        form = shedule_plan.education_form,
                        period = shedule_plan.period,
                        oop = OOP(code=oop_detail["code"],direction=oop_detail["direction"],
                                eduction_profile=oop_detail["eduction_profile"],
                                education_level=oop_detail["education_level"])
                        ,disciplines = disciplines_in_plan)


#переписать
@shedule_plan_router.post("/shedule/plan/create/", summary="Создать новый учебный план")
async def add_shedule_plan(item:ShedulePlanTableRecord):
    query = """INSERT INTO "ShedulePlan" (code, recruitment_year, education_form, period) 
               SELECT :code, :recruitment_year, :education_form, :period
               RETURNING  id"""
    values = {"code":item.code,"recruitment_year":item.recruitment_year, "education_form":item.form.name,"period":item.period}
   
    try:
        await database.execute(query=query, values=values)
    except IntegrityError:
        return JSONResponse(status_code=409, content = {"detail":{"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                                                        "msg": "Учебный план с таким кодом или почтой уже существует"}})
    except UniqueViolationError:
        return  JSONResponse(status_code=409, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Учебный план с таким кодом или почтой уже существует"}})
    return True

@shedule_plan_router.post("/shedule/plan/add/discipline/", summary="Переделать")
async def add_dicsipline_to_plan(discipline_name:str, shedule_plan_code:str,discipline_zet:int, discipline_hours:int ) -> bool:
    
    query = disciplines_table.select().where(disciplines_table.c.name == discipline_name)
    discipline = await database.fetch_one(query)
    if discipline == None:
         return JSONResponse(status_code=409, content = {"detail":{"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                                                        "msg": "Дисциплина не существует"}})
    query = shedule_plan_table.select().where(shedule_plan_table.c.code == shedule_plan_code)
    shedule_plan = await database.fetch_one(query)
    if shedule_plan == None:
         return JSONResponse(status_code=409, content = {"detail":{"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                                                        "msg": "Учебный план не существует"}})
                                                        
    query = disciplines_in_shedule_plan_table.insert().values( zet = discipline_zet, hours = discipline_hours, 
                                                               shedule_plan = shedule_plan.id, discipline = discipline.id)
    await database.execute(query)
    return True

@shedule_plan_router.post("/shedule/plan/add/oop/", summary="Добавить в учебный план ООП")
async def add_oop_to_plan(shedule_plan_code:str, oop_code:str) -> bool:
    query = oop_table.select().where(oop_table.c.code == oop_code)
    oop = await database.fetch_one(query)
    if oop == None:
        return JSONResponse(status_code=422, content = {"description": "ООП не существует"})
    print(oop)
    query = shedule_plan_table.select().where(shedule_plan_table.c.code == shedule_plan_code)
    shedule_plan  = await database.fetch_one(query)
    
    if shedule_plan == None:
        return JSONResponse(status_code=422, content = {"description": "Учебный план не существует"})
    await database.execute(query)

    query = shedule_plan_table.update().values(oop = oop["id"]).where(shedule_plan_table.c.code == shedule_plan_code)
    await database.execute(query)
    return True


  
@shedule_plan_router.get("/shedule/plan/disciplines", summary="Получить данные дисциплин учебного плана")
async def get_shedule_plans(shedule_plan_code:str): 
    query = shedule_plan_table.select().where(shedule_plan_table.c.code == shedule_plan_code)
    shedule_plan  = await database.fetch_one(query)
    if shedule_plan == None:
        return JSONResponse(status_code=422, content = {"description": "Учебный план не существует"}) 
    query = disciplines_in_shedule_plan_table.select().where(disciplines_in_shedule_plan_table.c.shedule_plan == shedule_plan["id"])
    disciplines = await database.fetch_all(query)

    _disciplines_ = []
 
    for discipline in disciplines:
        query = disciplines_table.select().where(disciplines_table.c.id == discipline["discipline"])
        _discipline_ = await database.fetch_one(query)
        _disciplines_.append(DisciplinesInShedulePlan(name=_discipline_["name"],hours=discipline["hours"],zet=discipline["zet"]))
    return _disciplines_

'''#Подумать над тем нужжно ли редактировать внутри дисциплины в одном запросе?
@shedule_plan_router.patch("/shedule/plan/path/", summary="Обновить данные учебного плана НЕ ДОДЕЛАННО")
async def path_shedule_plan(shedule_plan_id: int) -> ShedulePlan: 
    return ShedulePlan

@shedule_plan_router.delete("/shedule/plan/delete/", summary="Удалить план НЕ ДОДЕЛАННО")
async def delete_shedule_plan(shedule_plan_id: int) -> ShedulePlan: 
    return ShedulePlan
'''
