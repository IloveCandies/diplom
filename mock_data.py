import uuid
from shemas import*

Students = [Student.create("john","smith","unknown")]
Students[0].id= "mock_id1212qwqsd2323"
Students[0].password = "qwerty123"
Students[0].email = "testmail.test.com"

Groups = [Group.create(1,"ПИ - 666","2018",1,3,4,2023),Group.create(2,"ПИ - 666","2018",1,3,4,2023),Group.create(2,"ПИ - 666","2018",1,3,4,2023),
          Group.create(14,"ФИ - 233","2018",1,3,4,2023),Group.create(13,"АБОБУС - 666","2018",1,3,4,2023),Group.create(4,"ИиИ - 666","2018",1,3,4,2023),
          Group.create(15,"БИ - 166","2032",4,3,4,2023),Group.create(12,"МАТОБЕС - 666","2018",1,1,4,2023),Group.create(5,"КЕИ - 6626","2018",1,3,4,2023),
          Group.create(16,"ЛЕНЬ - 166","2022",6,7,4,2026),Group.create(11,"ПИ - 666","2018",1,3,4,2023),Group.create(6,"ДвИ - 666","2018",1,3,4,2023)]
FavoriteLists = []
