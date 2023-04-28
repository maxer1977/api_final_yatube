### **Описание:**

Проект **api_final_yatube** создан в учебных целях и демонстрирует
возможности создания программного интерфейса **API** с использованием
одного из актуальных и востребованных подходов — это архитектура *REST*
или *REpresentational State Transfer*.
Разработанный **API-интерфейс** позволяет наладить взаимодействие со
сторонними приложениями и/или устройствами, подддерживающим передачу данных
в формате *json*.

По своей сути **yatube** - это мини-социальная сеть, позволяющая пользователям
создавать, редактировать, удалять и комментировать сообщения пользователей.
Для пользователей действует система аутентификации и разграничения прав
доступа к отдельным ресурсам проекта.
Для этого в проекте созданы следующие логически (и программно) связанные блоки:
1. *Post* - сообщения (дата, автор, текст, изображение, тематическая группа)
2. *Comment* - комментарии к сообщениям (дата, пользователь, текст)
3. *Follow* - подписки пользователя на избранных авторов (пользователь, автор).
4. *Group* - тематические группы (название, описание, slug)


### **Установка:**

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/yandex-praktikum/kittygram.git

cd kittygram
```

2. Cоздать и активировать виртуальное окружение:

```
python -m venv env

source env/bin/activate
```

3. Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

4. Выполнить миграции:

```
python manage.py migrate
```

5. Запустить проект:

```
python manage.py runserver
```

### **Синтаксис API-запросов:**

Проект **api_final_yatube** поддерживает следующие запросы:

**1. *Сообщения (Post)***

Тип запроса|End-point|Параметры запроса|Код ответа|
------- | -------------|-------|---|
GET (список)| /api/v1/posts/|---| 200
GET (сообщение)| /api/v1/posts/{id}/|---| 200, 404
POST (создание)| /api/v1/posts/|***text**, image, group* | 201, 400, 401
PUT (редактирование)| /api/v1/posts/{id}/ | ***text**, image, group* | 201, 400, 401, 403, 404
DELETE (удаление)| /api/v1/posts/{id}/ | --- | 204, 401, 403, 404

**2. *Комментарии (Comment)***

Тип запроса|End-point|Параметры запроса|Код ответа|
------- | -------------|-------|---|
GET (список)| /api/v1/posts/{post_id}/comments/|---| 200, 404
GET (комментарий)| /api/v1/posts/{post_id}/comments/{id}/|---| 200, 404
POST (создание)| /api/v1/posts/{post_id}/comments/|***text***| 201, 400, 401, 404
PUT (редактирование)| /api/v1/posts/{post_id}/comments/{id}/|***text***| 200, 400, 401, 403, 404
DELETE (удаление)| /api/v1/posts/{post_id}/comments/{id}/|---| 204, 401, 403, 404

**3. *Тематические группы (Group)***

Тип запроса|End-point|Параметры запроса|Код ответа|
------- | -------------|-------|---|
GET (список)| /api/v1/groups/|---| 200, 404
GET (группа)| /api/v1/groups/{id}/|---| 200, 404

**4. *Подписки (Follow)***

Тип запроса|End-point|Параметры запроса|Код ответа|
------- | -------------|-------|---|
GET (список)| /api/v1/follow/|---| 200, 401
POST (создание)| /api/v1/follow/|***following***| 201, 400, 401

**5. *Получение JWT-токена***

Тип запроса|End-point|Параметры запроса|Код ответа|
------- | -------------|-------|---|
POST (создание)| /api/v1/jwt/create/|***user, password***| 200, 400, 401
