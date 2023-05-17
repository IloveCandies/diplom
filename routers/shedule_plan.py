from asyncpg import exceptions
from fastapi import APIRouter
from shemas import *
from db.models import shedule_plan_table, oop_table,disciplines_table,disciplines_in_shedule_plan_table
from db.init import database
from fastapi.responses import JSONResponse


shedule_plan_router = APIRouter( responses={404: {"description": "Not found"}})


#переписать
@shedule_plan_router.post("/shedule/plan/create/", summary="Создать новый учебный план")
async def add_shedule_plan(item:ShedulePlanTableRecord) -> ShedulePlanTableRecord:
    query = """INSERT INTO "ShedulePlan" (code, recruitment_year, education_form, period,oop) 
    SELECT :code, :recruitment_year, :education_form, :period, :oop
    WHERE
    NOT EXISTS (
    SELECT CAST(:code AS VARCHAR) FROM "ShedulePlan" WHERE code = :code) 
    RETURNING  id"""
    values = {"code":item.code,"recruitment_year":item.recruitment_year, 
    "education_form":item.form.name,"period":item.period}
    
    shedule_plan_id =  await database.execute(query=query, values=values)
    if shedule_plan_id == None:
        query = shedule_plan_table.select().where(shedule_plan_table.c.code == item.code)
        shedule_plan = await database.fetch_one(query)
        shedule_plan_id = tuple(shedule_plan.values())[0]
    print(shedule_plan_id)

    return item

@shedule_plan_router.post("/shedule/plan/add/discipline/", summary="Добавить в учебный план дисциплину")
async def add_dicsipline_to_plan(item:DisciplinesInShedulePlan, shedule_plan_id:int) -> ShedulePlan:
    
    query = disciplines_table.select().where(disciplines_table.c.name == item.name)
    discipline = await database.fetch_one(query)
    
    if discipline == None:
        return JSONResponse(status_code=422, content = {"description": "Дисциплина не существует чтобы создать дисциплину воспользуйтесь методом /disciplines/create/"})
    discipline_id = int(tuple(discipline.values())[0])

    query = disciplines_in_shedule_plan_table.select().where(
        disciplines_in_shedule_plan_table.c.shedule_plan == shedule_plan_id,
        disciplines_in_shedule_plan_table.c.discipline == discipline_id,)
    discipline = await database.fetch_one(query)

    if discipline == None:
        query = disciplines_in_shedule_plan_table.insert().values(
            hours = item.hours,
            zet = item.zet,
            shedule_plan = shedule_plan_id,
            discipline = discipline_id,
        )
 
    try:
        discipline_id = await database.execute(query=query)
    except (exceptions.UniqueViolationError):
        return JSONResponse(status_code=422, content = {"description": "Дисциплина с такими значениями уже существует в учебном плане"})

    query = disciplines_in_shedule_plan_table.select().where(disciplines_in_shedule_plan_table.c.shedule_plan == shedule_plan_id)


    disciplines_in_plan = [ tuple(item.values())[0:3] for item  in await database.fetch_all(query)]
    print(disciplines_in_plan)
    query = shedule_plan_table.select().where(shedule_plan_table.c.id == shedule_plan_id)
    shedule_plan = await database.fetch_one(query)

    return ShedulePlan( code = shedule_plan.code,
                        recruitment_year = shedule_plan.recruitment_year,
                        form = Education_form [shedule_plan.education_form],
                        period = shedule_plan.period,oop = shedule_plan.oop,disciplines = disciplines_in_plan)


@shedule_plan_router.get("/shedule/plan/", summary="Получить данные конкретного плана")
async def get_shedule_plan(shedule_plan_id: int) -> ShedulePlan:
    query = disciplines_in_shedule_plan_table.select().where(disciplines_in_shedule_plan_table.c.shedule_plan == shedule_plan_id)

    disciplines_in_plan = [ tuple(item.values())[0:3] for item  in await database.fetch_all(query)]
    print(disciplines_in_plan)
    query = shedule_plan_table.select().where(shedule_plan_table.c.id == shedule_plan_id)
    shedule_plan = await database.fetch_one(query)

    return ShedulePlan( code = shedule_plan.code,
                        recruitment_year = shedule_plan.recruitment_year,
                        form = Education_form [shedule_plan.education_form],
                        period = shedule_plan.period,oop = shedule_plan.oop,disciplines = disciplines_in_plan)
  
#дописать возвращение в json списка элементов

#переписать
@shedule_plan_router.post("/shedule/plan/export/", summary="Загрузить учебный план из json НЕ ДОДЕЛАННО")
async def add_shedule_plan(item:ShedulePlan) -> ShedulePlan: 

    query = """INSERT INTO "OOP" (code, direction, eduction_profile,education_level) 
    SELECT :code, :direction, :eduction_profile, :education_level
    WHERE
    NOT EXISTS (
    SELECT CAST(:code AS VARCHAR) FROM "OOP" WHERE code = :code) 
    RETURNING  id """
    values = {"code":item.oop.code,"direction":item.oop.direction, 
    "eduction_profile":item.oop.eduction_profile,"education_level":item.oop.education_level.name}

    oop_id =  await database.execute(query=query, values=values)
    print(oop_id)
    if oop_id == None:
        query = oop_table.select().where(oop_table.c.code == item.oop.code)
        oop = await database.fetch_one(query)
        oop_id = tuple(oop.values())[0]
    print(oop_id)

    query = """INSERT INTO "ShedulePlan" (code, recruitment_year, education_form, period,oop) 
    SELECT :code, :recruitment_year, :education_form, :period, :oop
    WHERE
    NOT EXISTS (
    SELECT CAST(:code AS VARCHAR) FROM "ShedulePlan" WHERE code = :code) 
    RETURNING  id """
    values = {"code":item.code,"recruitment_year":item.recruitment_year, 
    "education_form":item.form.name,"period":item.period ,"oop":oop_id}
    
    shedule_plan_id =  await database.execute(query=query, values=values)
    if shedule_plan_id == None:
        query = shedule_plan_table.select().where(shedule_plan_table.c.code == item.code)
        shedule_plan = await database.fetch_one(query)
        shedule_plan_id = tuple(shedule_plan.values())[0]
    print(shedule_plan_id)

    for discipline in item.disciplines:
        query = """INSERT INTO "Disciplines" (name) 
        SELECT :name,
        WHERE
        NOT EXISTS (
        SELECT CAST(:name AS VARCHAR) FROM "Disciplines" WHERE name = :name) 
        RETURNING  id """
        values = {"name":discipline.name}
        discipline_id =  await database.execute(query=query, values=values)

        if discipline_id == None:
            query = disciplines_table.select().where(disciplines_table.c.name == discipline.name)
            discipline = await database.fetch_one(query)
            discipline_id = tuple(discipline.values())[0]
        print(discipline_id)

        query = """INSERT INTO "DisciplineInShedulePlan" (shedule_plan, discipline) 
        SELECT :shedule_plan, :discipline 
        RETURNING  id """
        values = {"shedule_plan":shedule_plan_id,"discipline":discipline_id}
        await database.execute(query=query, values=values)

        print(discipline_id)
      
    return item

@shedule_plan_router.get("/shedule/plans/", summary="Получить данные всех учебных планов НЕ ДОДЕЛАННО")
async def get_shedule_plans() -> List[ShedulePlan]: 
    query = shedule_plan_table.select()
    return await database.fetch_all(query)

#Подумать над тем нужжно ли редактировать внутри дисциплины в одном запросе?
@shedule_plan_router.patch("/shedule/plan/path/", summary="Обновить данные учебного плана НЕ ДОДЕЛАННО")
async def path_shedule_plan(shedule_plan_id: int) -> ShedulePlan: 
    return ShedulePlan

@shedule_plan_router.delete("/shedule/plan/delete/", summary="Удалить план НЕ ДОДЕЛАННО")
async def delete_shedule_plan(shedule_plan_id: int) -> ShedulePlan: 
    return ShedulePlan

