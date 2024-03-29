# импортируем pymongo
import pymongo
 
# соединяемся с сервером базы данных 
# (по умолчанию подключение осуществляется на localhost:27017)
conn = pymongo.Connection()
 
# подключаемся к другому серверу, на другой порт
conn = pymongo.Connection('localhost', 27017)
 
# выбираем базу данных
db = conn.mydb
 
# БД можно выбрать и так
db = conn['mydb']
 
# выбираем коллекцию документов
coll = db.mycoll
 
# альтернативный выбор коллекции документов
coll = db['mycoll']
 
# осуществляем добавление документа в коллекцию,
# который содержит поля name и surname - имя и фамилия
doc = {"name":"Иван", "surname":"Иванов"}
coll.save(doc)
 
# альтернативное добавление документа
coll.save({"name":"Петр", "surname":"Петров"})
 
# выводим все документы из коллекции coll
for men in coll.find():
    print men
 
# выводим фамилии людей с именем Петр
for men in coll.find({"name": "Петр"})
    print men["surname"]
 
# подсчет количества людей с именем Петр
print coll.find({"name": "Петр"}).count()
 
# добавляем ко всем документам новое поле sex - пол
coll.update({}, {"$set":{"sex": "мужской"}})
 
# всем Петрам делаем фамилию Новосельцев и возраст 25 лет
coll.update({"name": "Петр"}, {"surname": "Новосельцев", "age": 25})
 
# увеличиваем всем Петрам возраст на 5 лет
coll.update({"name": "Петр"}, {"$inc": {"age": 5}})
 
# сбрасываем у всех документов поле name
coll.update({}, {"$unset": {"name": 1}})
 
# удаляем людей с возрастом более 20 лет
# другие условия $gt - больше, $lt - меньше, 
# $lte - меньше или равно, $gte - больше или равно, $ne - не равно
coll.remove({"age": {"$gt": 20}})
 
# удаляем все документы коллекции
coll.remove({})


